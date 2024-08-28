import maya.cmds as cmds 
import maya.mel as mel 
import os
import json
import subprocess
import datetime

class MayaAPI():
    def __init__(self):
        pass
    
    def get_file_name(self):
        """현재 열려있는 마야 파일 이름 가져오는 메서드"""
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        return filename

    def get_selected_objects(self):
        """선택한 오브젝트 리스트 가져오는 메서드"""
        return cmds.ls(sl=True)

    def export_alemibc(self, path):
        """
        알렘빅이 저장될 경로를(디렉토리) 이용
        """
        assets = self.get_selected_objects()    # 선택된 object 리스트 : ['pSphere1', 'pCube1', 'pCylinder1', 'pCone1']
        start_frame = int(cmds.playbackOptions(query=True, min=True))
        last_frame = int(cmds.playbackOptions(query=True, max=True))

        for asset in assets:
            abc_cache_path = f"/home/rapa/show/{asset}.abc"
            alembic_args = ["-renderableOnly", "-writeFaceSets", "-uvWrite", "-worldSpace", "-eulerFilter"]

            alembic_args.append(f"-fr {start_frame} {last_frame}")
            alembic_args.append(f"-file '{abc_cache_path}'")
            alembic_args.append(f"-root {asset}")
            abc_export_cmd = 'AbcExport -j "%s"' % " ".join(alembic_args)
            mel.eval(abc_export_cmd)
    
    def export_shader(self, export_path):
        """
        maya에서 오브젝트에 어싸인된 셰이더들을 ma 파일로 익스포트하고,
        그 정보들을 json 파일로 익스포트 하는 함수이다.
        """

        shader_dictionary = self.collect_shader_assignments()

        for shader, _ in shader_dictionary.items():
            cmds.select(shader, add=True)    

        ma_file_path = f"{export_path}/shader.ma"
        json_file_path = f"{export_path}/shader.json"

        cmds.file(ma_file_path, exportSelected=True, type="mayaAscii")
        with open(json_file_path, 'w') as f:
            json.dump(shader_dictionary, f)

        cmds.select(clear=True)
    
    def collect_shader_assignments(self):
        """
        셰이더와 오브젝트들을 컬렉션하는 함수.
        """
        shader_dictionary = {}
        shading_groups = cmds.ls(type="shadingEngine")
        for shading_group in shading_groups:
            shader = cmds.ls(cmds.listConnections(shading_group + ".surfaceShader"), materials=True)    
            if not shader:
                continue
            objects = cmds.sets(shading_group, q=True)
            shader_name = shader[0]
            if objects:
                if shader_name not in shader_dictionary:
                    shader_dictionary[shader_name] = []
                shader_dictionary[shader_name].extend(objects)
        return shader_dictionary

    def save_file(self, path):
        """마야 파일 저장하는 메서드"""
        file_path, name = os.path.split(path)
        print (file_path, name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        cmds.file(rename=file_path)
        cmds.file(save=True)
    
    def get_current_path(self):
        return cmds.file(query=True, sceneName=True)
    
    def make_playblast(self, image_path):
        """
        마야의 플레이 블라스트 기능을 이용해서 뷰포트를 이미지로 렌더링하고,
        슬레이트 정보를 삽입하여 동영상을 인코딩한다.
        image : jpg
        mov codec : h264
        """
        proxy_path = "/home/rapa/show/baked/AST/Character/Apple/MOD/dev/data/proxy"
        proxy_format = "jpg"
        image_path = f"{proxy_path}/proxy.%04d.{proxy_format}"
        # mov_path = f"{proxy_path}/MOD_Apple_v001.mov"

        # start_frame = int(cmds.playbackOptions(query=True, min=True))
        # last_frame = int(cmds.playbackOptions(query=True, max=True))
        start_frame = 1001
        last_frame = 1230
        render_width = 1920
        render_height = 1080

        # PLAYBLAST MAYA API
        # 플레이블라스트 옵션을 이미지로 설정하고 jpg 로 렌더링을 한다.
        """
        percent는 현재 뷰포트 크기의 백분율을 의미함. 100은 현재 뷰포트 크기를 전부 사용하여 렌더링을 하겠다를 의미
        showOrnament는 뷰포트상의(axis 라던가..)등의 표시 여부를 설정합니다.
        widthHeight는 렌더링 이미지의 해상도를 설정합니다.
        quality = 이미지 렌더링시 압축 품질에 대한 값을 설정합니다. 100이 좋은거임.
        forceOverwrite = 렌더링시 덮어씌우기 여부를 설정합니다.
        startTime, endTime = 프레임 레인지 셋팅
        viewer = 렌더링 완료시 플레이어로 재생할지를 설정하는데.. False 하셈
        offScreen = 테스트중
        """
        
        cmds.playblast(filename=proxy_path, format='image', compression=proxy_format,
                        startTime=start_frame, endTime=last_frame, forceOverwrite=True,
                        widthHeight=(render_width, render_height), percent=100,
                        showOrnaments=True, framePadding=4, quality=100, viewer=False)
        return start_frame, last_frame, image_path
        
    def ffmpeg(self, start_frame, last_frame, image_path, mov_path):
        ## 플레이블라스트로 렌더링한 이미지를 FFMPEG 라이브러리를 이용해서 동영상을 인코딩한다.
        first = 1001
        frame_rate = 24 
        # 사운드가 있는 경우 23.976 으로 합니다.
        # 이 경우 ffmpeg에 사운드 파일을 추가하는 설정이 필요합니다.
        ffmpeg = "ffmpeg"
        slate_size = 60
        font_path = "/home/rapa/문서/font/waltographUI.ttf"
        font_size = 40
        frame_count = last_frame - start_frame
        text_x_padding = 10
        text_y_padding = 20

        # top_left = cmds.file(query=True, sn=True, shn=True)
        top_left = os.path.splitext(mov_path)[0].split('/')[-1]
        top_center = "Baked"
        top_right = datetime.date.today().strftime("%Y/%m/%d")
        bot_left = "SIZE : 1920x1080"
        bot_center = ""

        frame_cmd = "'Frame \: %{eif\:n+"
        frame_cmd += "%s\:d}' (%s)"  % (first, frame_count+1)
        bot_right = frame_cmd

        cmd = '%s -framerate %s -y -start_number %s ' % (ffmpeg, frame_rate, first)
        cmd += '-i %s' % (image_path)
        cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
        cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
        cmd += '"'
        # cmd += ' -c:v libx264 %s' % mov_path
        cmd += ' -c:v prores_ks -profile:v 3 -colorspace bt709 %s' % mov_path

        os.system(cmd)
        return mov_path