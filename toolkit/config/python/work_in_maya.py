try:
    import maya.cmds as cmds 
    import maya.mel as mel 
except:
    pass
import os
import json
import subprocess
import datetime
import ffmpeg
import glob

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
    
    def save_file(self, path):
        
        # 현재 씬의 이름과 경로를 output_path로 설정
        cmds.file(rename=path)
        # Maya Binary 형식으로 씬 저장
        cmds.file(save=True, type='mayaBinary')

        print(f"Model saved as Maya Binary file to: {path}")
    
########################### Modeling #####################################3

    @staticmethod
    def modeling_publish_set(self):
        # 1. 에셋 스케일 고정 (Freeze Transformations)
        selected_objects = cmds.ls(selection=True)
        if selected_objects:
            cmds.makeIdentity(selected_objects, apply=True, scale=True)
            print("선택된 오브젝트의 Scale이 1로 고정되었습니다.")
        else:
            print("선택된 오브젝트가 없습니다. Scale 고정 작업을 건너뜁니다.")

        # 2. 히스토리 삭제 (Delete History) Edit → Delete by Type → History
        if selected_objects:
            cmds.delete(selected_objects, constructionHistory=True)
            print("선택된 오브젝트의 히스토리가 삭제되었습니다.")
        else:
            print("선택된 오브젝트가 없습니다. 히스토리 삭제 작업을 건너뜁니다.")

        # 3. 사용되지 않는 쉐이더 삭제 (Delete Unused Shaders) Rendering editor → hypershade
        all_shaders = cmds.ls(materials=True)
        used_shaders = cmds.ls(cmds.listConnections(cmds.ls(geometry=True)), materials=True)

        unused_shaders = list(set(all_shaders) - set(used_shaders))

        if unused_shaders:
            cmds.delete(unused_shaders)
            print(f"{len(unused_shaders)}개의 필요없는 쉐이더가 삭제되었습니다.")
        else:
            print("삭제할 필요없는 쉐이더가 없습니다.")
    
    def set_single_renderable_camera(self, camera_name):
        """
        지정된 카메라만 렌더러블 상태로 유지하고, 다른 모든 카메라는 비활성화합니다.
        
        Args:
        camera_name (str): 렌더러블 상태로 유지할 카메라의 이름.
        """
        all_cameras = cmds.ls(type='camera')
        for cam in all_cameras:
            cmds.setAttr(f"{cam}.renderable", cam == camera_name)

    def render_turntable(self, output_path_template, start_frame=1001, end_frame=1096, width=1920, height=1080, distance = 30 ):
        # 턴테이블 애니메이션을 위한 설정

        ext = os.path.splitext(output_path_template)[1]
        self.set_image_format(ext)
        cmds.setAttr("defaultResolution.width", width)
        cmds.setAttr("defaultResolution.height", height)

        # 기존 턴테이블 카메라가 있는지 확인
        camera_transform = None
        camera_name = "turntable_camera#"

        existing_cameras = cmds.ls(type="camera")
        for cam_shape in existing_cameras:
            transform_node = cmds.listRelatives(cam_shape, parent=True)[0]
            if camera_name in transform_node:
                camera_transform = transform_node
                break

        # 카메라가 존재하지 않으면 새로 생성
        if camera_transform is None:
            camera_transform, camera_shape = cmds.camera(name=camera_name)
            cmds.viewFit(camera_transform)  # 자동으로 카메라 위치 세팅
            cmds.setAttr(camera_transform + ".translateZ", distance)  # 카메라 거리를 설정

            # 카메라 그룹 생성 및 그룹에 카메라 추가
            turntable_grp = cmds.group(empty=True, name='turntable_camera_grp')
            cmds.parent(camera_transform, turntable_grp)
        else:
            # 기존 카메라 그룹 찾기
            turntable_grp = cmds.listRelatives(camera_transform, parent=True)[0]

        # 애니메이션 키프레임 설정
        start_frame = int(cmds.playbackOptions(query=True, minTime=True))  # 시작 프레임 읽기
        end_frame = int(cmds.playbackOptions(query=True, maxTime=True))    # 끝 프레임 읽기
        cmds.setKeyframe(turntable_grp, attribute="rotateY", time=start_frame, value=0)
        cmds.setKeyframe(turntable_grp, attribute="rotateY", time=end_frame, value=360)

        # 키프레임을 선형으로 설정
        cmds.keyTangent(turntable_grp, attribute="rotateY", inTangentType="linear", outTangentType="linear")

        # 턴테이블 렌더링 수행
        for frame in range(start_frame, end_frame + 1):
            output_path = output_path_template % frame
            cmds.currentTime(frame)
            cmds.render(camera_transform, x=width, y=height)
            cmds.renderWindowEditor("renderView", e=True, writeImage=output_path)


####################### Animation #################################################33

    def export_alemibc(self, abc_cache_path, asset):
        """
        알렘빅이 저장될 경로를(디렉토리) 이용
        """
        print ("*******************")
        print (asset, abc_cache_path)
        print ("*******************")

         # 선택된 object 리스트 : ['pSphere1', 'pCube1', 'pCylinder1', 'pCone1']
        start_frame = int(cmds.playbackOptions(query=True, min=True)) - 10
        last_frame = int(cmds.playbackOptions(query=True, max=True)) + 10

        alembic_args = ["-renderableOnly", "-writeFaceSets", "-uvWrite", "-worldSpace", "-eulerFilter"]

        alembic_args.append(f"-fr {start_frame} {last_frame}")
        alembic_args.append(f"-file '{abc_cache_path}'")
        alembic_args.append(f"-root {asset}")
        abc_export_cmd = 'AbcExport -j "%s"' % " ".join(alembic_args)
        mel.eval(abc_export_cmd)
    

################### 플레이블라스트, 렌더, ffmpeg ########################################
    
    def make_playblast(self, image_path):
        """
        마야의 플레이 블라스트 기능을 이용해서 뷰포트를 이미지로 렌더링하고,
        슬레이트 정보를 삽입하여 동영상을 인코딩한다.
        image : jpg
        mov codec : h264
        """
        proxy_path = ''.join(image_path.split('.')[0])
        _, proxy_format = os.path.splitext(image_path)
        proxy_format = proxy_format[1:]
        print (f"image path {image_path}")
        print (f"proxy path :{proxy_path}")
        print (f"proxy format :{proxy_format}")

        # start_frame = int(cmds.playbackOptions(query=True, min=True))
        # last_frame = int(cmds.playbackOptions(query=True, max=True))
        start_frame = 1001
        last_frame = 1096
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
        
        return start_frame, last_frame
    
    def make_ffmpeg(self, start_frame, last_frame, input_path, output_path, project_name):
        ## 플레이블라스트로 렌더링한 이미지를 FFMPEG 라이브러리를 이용해서 동영상을 인코딩한다.
        first = 1001
        frame_rate = 24 
        # 사운드가 있는 경우 23.976 으로 합니다.
        # 이 경우 ffmpeg에 사운드 파일을 추가하는 설정이 필요합니다.
        ffmpeg = "ffmpeg"
        slate_size = 60
        font_path = "/home/rapa/문서/font/waltographUI.ttf"
        frame_count = int(last_frame) - int(start_frame)
        # frame_count = 10
        font_size = 40
        text_x_padding = 10
        text_y_padding = 20

        # top_left = cmds.file(query=True, sn=True, shn=True)
        top_left, _ = os.path.splitext(os.path.basename(output_path))
        top_center = project_name
        top_right = datetime.date.today().strftime("%Y/%m/%d")
        bot_left = "1920x1080"
        bot_center = ""

        frame_cmd = "'Frame \: %{eif\:n+"
        frame_cmd += "%s\:d}' (%s)"  % (first, frame_count+1)
        bot_right = frame_cmd

        if last_frame == 1:
            return
            # import test_ffmpeg
            # bot_right = "Frame1"
            # output_path = output_path.replace('.mov', '.jpg')
            # self.slate = test_ffmpeg.MakeSlate()
            # self.slate.make_ffmpeg_jpg(top_left, top_center, top_right, bot_left, bot_center, bot_right, input_path, output_path)
            # print("캡쳐라서 jpg 메서드로")
            # print ("!!!", input_path, output_path)
            # print (top_left, top_center, top_right, bot_left, bot_center, bot_right, input_path, output_path)
            # self.make_ffmpeg_jpg(top_left, top_center, top_right, bot_left, bot_center, bot_right, input_path, output_path)

        cmd = '%s -framerate %s -y -start_number %s ' % (ffmpeg, frame_rate, first)
        cmd += '-i %s' % (input_path)
        cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
        cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
        cmd += '"'
        # cmd += ' -c:v libx264 %s' % output_path
        cmd += ' -c:v prores_ks -profile:v 3 -colorspace bt709 %s' % output_path
        os.system(cmd)
        return output_path
    
    def make_ffmpeg_jpg(self, top_left, top_center, top_right, bot_left, bot_center, bot_right, input_path, output_path):
        
        self.find_frame(input_path)
        # self.input_jpg_slate(top_left, top_center, top_right, bot_left, bot_center, bot_right)
        
        self.gamma = "eq=gamma=1.4,"
        self.render_jpg_slate(top_left, top_center, top_right, bot_left, bot_center, bot_right, input_path, output_path)
        
    def find_frame(self, input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
        self.width = int(video_stream['width'])
        self.height = int(video_stream['height'])

    
    def render_jpg_slate(self, top_left, top_center, top_right, bot_left, bot_center, bot_right, input, output):
        font_size = self.height / 18 - 5
        box_size = self.height / 18
        fontfile = "/home/rapa/문서/font/waltographUI.ttf"
        
        # drawtext 필터를 위한 문자열 구성
        top_left_text = f"drawtext=fontfile={fontfile}:text='{top_left}':x=5:y=2:fontcolor=white@0.7:fontsize={font_size}"
        top_center_text = f"drawtext=fontfile={fontfile}:text='{top_center}':x=(w-tw)/2:y=2:fontcolor=white@0.7:fontsize={font_size}"
        top_right_text = f"drawtext=fontfile={fontfile}:text='{top_right}':x=w-tw-5:y=2:fontcolor=white@0.7:fontsize={font_size}"
        bot_left_text = f"drawtext=fontfile={fontfile}:text='{bot_left}':x=5:y=h-th:fontcolor=white@0.7:fontsize={font_size}"
        bot_center_text = f"drawtext=fontfile={fontfile}:text='{bot_center}':x=(w-tw)/2:y=h-th:fontcolor=white@0.7:fontsize={font_size}"
        bot_right_text = f"drawtext=fontfile={fontfile}:text='{bot_right}':x=w-tw-5:y=h-th:fontcolor=white@0.7:fontsize={font_size}"
        
        # drawbox 필터를 위한 문자열 구성
        box_filter = (
            f"drawbox=x=0:y=0:w={self.width}:h={box_size}:color=black@1:t=fill,"
            f"drawbox=x=0:y={self.height-box_size}:w={self.width}:h={box_size}:color=black@1:t=fill"
        )
        
        # 전체 필터 문자열 구성
        vf_filter = f"{box_filter},{top_left_text},{top_center_text},{top_right_text},{bot_left_text},{bot_center_text},{bot_right_text}"

        # ffmpeg 명령어 문자열 구성
        cmd = f'ffmpeg -i {input} -vf "{vf_filter}" -y {output}'
        
        # ffmpeg 명령어 실행
        os.system(cmd)
            
        # (
        #     ffmpeg
        #     .input(input)    
        #     .output(output,vf=f"{self.box}"f"{self.gamma}"f"{self.top_Left},{self.top_Middel},{self.top_Right},{self.bot_Left},{self.bot_Middle},{self.bot_Right}")
        #     .overwrite_output()
        #     .run()
        # )  

    def input_jpg_slate(self, top_left, top_center, top_right, bot_left, bot_center, bot_right):
        
        font_size = self.height/18 - 5
        box_size = self.height/18
        fontfile = "/home/rapa/문서/font/waltographUI.ttf"
        self.top_Left = f"drawtext=fontfile={fontfile}:text   = {top_left}: : x=5:y=2           :fontcolor=white@0.7:fontsize={font_size}"
        self.top_Middel = f"drawtext=fontfile={fontfile}:text = {top_center}: : x=(w-tw)/2:y=2   :fontcolor=white@0.7:fontsize={font_size}"
        self.top_Right = f"drawtext=fontfile={fontfile}:text  = {top_right}: : x=w-tw-5:y=2      :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Left = f"drawtext=fontfile={fontfile}:text   = {bot_left}: : x=5:y=h-th        :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Middle = f"drawtext=fontfile={fontfile}:text = {bot_center}: : x=(w-tw)/2:y=h-th :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Right = f"drawtext=fontfile={fontfile}: text = {bot_right}:start_number = 1001 : x=w-tw-5:y=h-th     :fontcolor=white@0.7:fontsize={font_size}"
        self.box = f"drawbox = x=0: y=0: w={self.width}: h={box_size}: color = black: t=fill,drawbox = x=0: y={self.height-box_size}: w={self.width}: h={self.height}: color = black: t=fill,"


################################## 매치무브 ###################################3

    def get_undistortion_size(self):
        width = cmds.getAttr('defualtResolution.width')
        height = cmds.getAttr('defaultResolution.height')
        return width, height
    

##################################################################################33


    def render_to_multiple_formats(self, output_path, width=1920, height=1080):

        # 공통 렌더링 설정
        cmds.setAttr("defaultResolution.width", width)
        cmds.setAttr("defaultResolution.height", height)
        
        # 현재 뷰의 카메라 가져오기
        current_camera = cmds.modelPanel(cmds.getPanel(withFocus=True), q=True, camera=True)
        
        # 렌더링
        ext = os.path.splitext(output_path)[1]
        self.set_image_format(ext)
        cmds.render(current_camera, x=width, y=height, f=output_path)

    def set_image_format(self, format_name):
        """이미지 형식을 설정하는 함수"""
        format_dict = {
            ".jpg": 8,
            ".jpeg": 8,
            ".exr": 51,
            ".png": 32,
            ".tiff": 3,
            ".tif": 3,
            }
        
        if format_name.lower() in format_dict:
            cmds.setAttr("defaultRenderGlobals.imageFormat", format_dict[format_name.lower()])
        else:
            raise ValueError(f"지원되지 않는 이미지 형식: {format_name}")

    def render_file(self, outpath):
        output_dir = f"{os.path.dirname(outpath)}/"  # 렌더링 이미지가 저장될 경로
        print (outpath, output_dir)
        filename_template = "<Scene>"
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", output_dir + filename_template, type="string") ### 경로 설정해주기
        cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)
        cmds.setAttr("defaultRenderGlobals.animation", 1)
        cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
        cmds.arnoldRender(batch=True)
        thumbnail_path = self.convert_exr_into_jpg(outpath)
        return thumbnail_path
        
    def convert_exr_into_jpg(self, input_file):
        output_file = input_file.replace(".%04d.exr", ".jpg")
        files = glob.glob(f"{os.path.dirname(output_file)}/*")
        input_file = max(files, key=os.path.getmtime)
        print (input_file, output_file)
        try:
            # FFmpeg 명령어 구성
            command = [
                'ffmpeg',
                '-i', input_file,   # 입력 파일 (EXR)
                '-q:v', "2",  # 품질 설정
                output_file          # 출력 파일 (JPG)
            ]
        
            # FFmpeg 명령 실행
            subprocess.run(command, check=True)
            print(f"변환 성공: {output_file}")
    
        except subprocess.CalledProcessError as e:
            print(f"변환 실패: {e}")
        
        return output_file
            
###### 쉐이더 ###################################################################

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

    def export_shader(self, ma_file_path):
        """
        maya에서 오브젝트에 어싸인된 셰이더들을 ma 파일로 익스포트하고,
        그 정보들을 json 파일로 익스포트 하는 함수이다.
        """

        shader_dictionary = self.collect_shader_assignments()
        ma_file_dir_path = os.path.dirname(ma_file_path)
        json_file_name = os.path.basename(ma_file_path).replace(".ma", ".json")
        json_file_path = f"{ma_file_dir_path}/{json_file_name}"
        print(json_file_path)

        for shader, _ in shader_dictionary.items():
            cmds.select(shader, add=True)    
        
        cmds.file(ma_file_path, exportSelected=True, type="mayaAscii")
        with open(json_file_path, 'w') as f:
            json.dump(shader_dictionary, f)

        cmds.select(clear=True)
        
        # 결과 출력
        print(f"Shaders exported to: {ma_file_path}") # ma 파일 경로
        print(f"Shader assignment data exported to: {json_file_path}") # json 파일 경로
        print("Shader Dictionary:")
        for shader, objects in shader_dictionary.items():
            print(f"  Shader: {shader} -> Objects: {objects}")

        return json_file_name, json_file_path

    
    def get_custom_shader_list(self):
        """
        Maya 씬에서 기본 쉐이더를 제외한 사용자 정의 쉐이더 목록을 가져옵니다.
        
        Returns:
        list: 사용자 정의 쉐이더 이름들의 리스트
        """
        # 기본 쉐이더 목록 (제외할 쉐이더)
        default_shaders = {'lambert1', 'particleCloud1', 'shaderGlow1'}

        # 씬에 있는 모든 쉐이더를 가져옵니다.
        shaders = cmds.ls(materials=True)

        # 사용자 정의 쉐이더만 필터링
        custom_shaders = [shader for shader in shaders if shader not in default_shaders]

        # 사용자 정의 쉐이더 목록 출력
        print("Custom Shader List:", custom_shaders)
        
        return custom_shaders
    
    def get_texture_list(self):
        """
        Maya 씬에서 사용된 텍스처 파일들의 이름을 가져옵니다.
        
        Returns:
        list: 텍스처 파일 이름들의 리스트
        """
        textures = []
        file_nodes = cmds.ls(type="file")
        for node in file_nodes:
            # 텍스처 파일 경로를 가져옴
            file_path = cmds.getAttr(f"{node}.fileTextureName")
            # 파일 이름만 추출
            file_name = os.path.basename(file_path)
            textures.append(file_name)
        
        textures = textures.remove("")
        print("텍스처 파일 이름 목록:", textures)
        return textures

    # def make_ffmpeg(self, input_path, output_path, project_name, start_frame=None, last_frame=None):
    #     print ("**********************************************************************************")
    #     print (input_path, output_path, project_name, start_frame, last_frame)
    #     ## 플레이블라스트로 렌더링한 이미지를 FFMPEG 라이브러리를 이용해서 동영상을 인코딩한다.
    #     first = 1001
    #     frame_rate = 24 
    #     # 사운드가 있는 경우 23.976 으로 합니다.
    #     # 이 경우 ffmpeg에 사운드 파일을 추가하는 설정이 필요합니다.
    #     ffmpeg = "ffmpeg"
    #     slate_size = 60
    #     font_path = "/home/rapa/문서/font/waltographUI.ttf"
    #     font_size = 40
    #     text_x_padding = 10
    #     text_y_padding = 20

    #     # top_left = cmds.file(query=True, sn=True, shn=True)
    #     top_left = os.path.splitext(output_path)[0].split('/')[-1]
    #     top_center = project_name
    #     top_right = datetime.date.today().strftime("%Y/%m/%d")
    #     bot_left = "SIZE : 1920x1080"
    #     bot_center = ""

    #     cmd = f'{ffmpeg}'
    #     bot_right = "Frame 1"
    #     cmd += ' -i %s ' % (input_path)

    #     if last_frame is None:
    #         bot_right = "Frame 1"
    #         cmd = f'{ffmpeg}'
    #         cmd += ' -i %s ' % (input_path)
    #         cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
        #     cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
        #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
        #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
        #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
        #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
        #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
        #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
        #     cmd += '"'`
        #     cmd += f' -frames:v 1 {output_path.replace(".mov", ".jpg")}
        #     os.system(cmd)
        #     return output_path.replace('.mov', '.jpg')
    

              
    #     else:
    #         frame_count = int(last_frame) - int(start_frame)
    #         frame_cmd = "'Frame \: %{eif\:n+"
    #         frame_cmd += "%s\:d}' (%s)"  % (first, frame_count+1)
    #         bot_right = frame_cmd
    #         cmd += ' -framerate %s -y -start_number %s ' % (frame_rate, first)
        
    #     cmd += '-i %s' % (input_path)
    #     cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
    #     cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
    #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
    #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
    #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
    #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
    #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
    #     cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
    #     cmd += '"'
    #     # cmd += ' -c:v libx264 %s' % output_path
    #     if last_frame:
    #         cmd += ' -c:v prores_ks -profile:v 3 -colorspace bt709 %s' % output_path
    #     elif last_frame == None:
    #         cmd += f' -frames:v 1 {output_path.replace(".mov", ".jpg")}'
    #     try:
    #         os.system(cmd)
    #     except:
    #         print ("Ffmpeg doesn't work")
    #     if last_frame:
    #         return output_path
    #     else:
    #         return output_path.replace('.mov', '.jpg')
    
    
    def render_exr_sequence(self, output_path):
        """
        'anicam' 또는 'mmcam' 카메라를 사용하여 여러 프레임을 .exr 형식으로 렌더링합니다.
        
        Args:
        output_dir (str): 렌더링된 이미지가 저장될 디렉토리.
        output_file_name (str): 렌더링된 이미지 파일의 이름.
        start_frame (int): 렌더링 시작 프레임.
        end_frame (int): 렌더링 종료 프레임.
        """

        camera_name = None
        if cmds.objExists("anicam"):
            camera_name = "anicam"
        elif cmds.objExists("mmcam"):
            camera_name = "mmcam"
        
        if not camera_name:
            print("Error: Neither 'anicam' nor 'mmcam' exists in the scene.")
            return
        
        print(f"Using camera: {camera_name}")
        
        # 지정된 카메라만 렌더러블 상태로 유지
        self.set_single_renderable_camera(camera_name)

        # 프레임 가져오기
        start_frame = cmds.playbackOptions(q=True, min=True)
        last_frame = cmds.playbackOptions(q=True, max=True)

        
        # 렌더 설정
        cmds.setAttr("defaultRenderGlobals.imageFormat", 51)  # 51: OpenEXR 형식
        cmds.setAttr("defaultRenderGlobals.imfkey", "exr", type="string")
        cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
        
        # 프레임 범위에 따라 렌더링 수행
        for frame in range(start_frame, last_frame + 1):
            cmds.currentTime(frame)  # 현재 프레임 설정
            cmds.setAttr("defaultRenderGlobals.imageFilePrefix", output_path, type="string")
            cmds.arnoldRender(cam=camera_name, width=1920, height=1080)
            print(f"Rendered frame {frame} saved as {output_path}")

    def get_texture_list(self):
        """
        Maya 씬에서 사용된 텍스처 파일들의 이름을 가져옵니다.
        
        Returns:
        list: 텍스처 파일 이름들의 리스트
        """
        textures = []
        file_nodes = cmds.ls(type="file")
        for node in file_nodes:
            # 텍스처 파일 경로를 가져옴
            file_path = cmds.getAttr(f"{node}.fileTextureName")
            # 파일 이름만 추출
            file_name = os.path.basename(file_path)
            textures.append(file_name)
        
        print("텍스처 파일 이름 목록:", textures)
        return textures

    def get_custom_shader_list():
        """
        Maya에서 새로 생성된 쉐이더 목록을 가져옵니다.
        
        Returns:
        list: 새로 생성된 쉐이더 이름들의 리스트
        """
        # 기본적으로 Maya 씬에 포함된 쉐이더들의 목록
        default_shaders = {'lambert1', 'particleCloud1', 'standardSurface1', 'shaderGlow1'}
        
        # 씬에서 모든 쉐이더(materials=True)를 가져옴
        all_shaders = cmds.ls(materials=True)
        
        # 새로 생성된 쉐이더만 필터링
        custom_shaders = [shader for shader in all_shaders if shader not in default_shaders]
        
        print("새로 생성된 쉐이더 목록:", custom_shaders)
        return custom_shaders


    def publish_shader(output_path, shaders=None):
        """
        쉐이더를 .ma 파일로 퍼블리시하는 함수.

        :param output_path: 퍼블리시할 .ma 파일의 경로
        :param shaders: 퍼블리시할 쉐이의 목록 (None이면 현재 선택된 쉐이더 사용)
        """
        # 만약 쉐이더가 None이면 현재 선택된 쉐이더 사용
        if shaders is None:
            shaders = cmds.ls(sl=True, dag=True, s=True)

        # 쉐이더 목록을 선택하여 퍼블리시
        if shaders:
            cmds.select(shaders)
            cmds.file(output_path, type='mayaAscii', exportSelected=True, force=True)
        else:
            print("선택된 쉐이더가 없습니다. 퍼블리시할 수 없습니다.")

        def get_custom_shader_list():
            # 기본 쉐이더 목록 정의
            default_shaders = ['lambert1', 'particleCloud1', 'shaderGlow1', 'initialShadingGroup', 'initialParticleSE']
            
            # 씬에서 모든 쉐이더 가져오기
            all_shaders = cmds.ls(materials=True)
            
            # 기본 쉐이더를 제외한 사용자 정의 쉐이더만 필터링
            custom_shaders = [shader for shader in all_shaders if shader not in default_shaders]
            
            return custom_shaders


    def publish_shaders_as_ma(shader_list, output_path):
        """
        선택된 쉐이더들을 .ma 파일로 저장하는 함수.
        
        Args:
        shader_list (list): 퍼블리시할 쉐이더들의 목록.
        output_path (str): 저장할 .ma 파일의 경로.
        """
        # 새로운 씬을 생성하여 쉐이더만 내보내기 위해 기존 씬을 클리어
        cmds.file(new=True, force=True)

        # 쉐이더를 선택하여 씬에 가져오기
        for shader in shader_list:
            shading_groups = cmds.listConnections(shader, type='shadingEngine')
            if shading_groups:
                for sg in shading_groups:
                    cmds.select(sg, add=True)

        # .ma 파일 형식으로 저장
        cmds.file(rename=output_path)
        cmds.file(save=True, type='mayaAscii')

        print(f"Shaders saved as Maya ASCII (.ma) file to: {output_path}")

    def export_camera_cache(self, output_path, camera_name):
        """
        'anicam' 또는 'mmcam'이라는 이름의 카메라 애니메이션을 Alembic 캐시 파일로 내보내고,
        지정된 경로에 저장합니다. 'anicam'이 존재하면 이 카메라를 사용하고,
        존재하지 않으면 'mmcam'을 사용합니다.
        
        Args:
        cache_directory (str): Alembic 캐시 파일을 저장할 경로
        """
        
        # 우선적으로 'anicam' 카메라를 찾고, 없으면 'mmcam'을 찾음
        camera_name = None
        if 'aniCam'in camera_name:
            camera = camera_name
        elif "mmCam" in camera_name:
            camera = camera_name
        
        if not camera:
            print("Error: Neither 'anicam' nor 'mmcam' exists in the scene.")
            return

        self.export_alemibc(output_path, camera)

    def _get_lighting_layers(self):
        all_layers = cmds.ls(type="renderLayer")
        return all_layers
    
    def render_all_layers_to_exr(self, layer, publish_dict):
        """
        모든 렌더 레이어를 EXR 형식으로 렌더링하고, 지정된 경로에 저장하는 함수.
        
        Args:
            output_dir (str): 렌더링된 이미지가 저장될 디렉토리 경로.
        """
        path = publish_dict[layer]["path"]
        output_dir = '/'.join(path.split('/')[:-1])

        # 렌더 레이어 변경
        cmds.editRenderLayerGlobals(currentRenderLayer=layer)

        
        # 파일 이름 접두사 설정
        file_prefix = f"{output_dir}/{layer}/{layer}"
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", file_prefix, type="string")
        print (publish_dict)
        
        # 배치 렌더링 수행
        cmds.arnoldRender(batch=True)
        print(f"{layer} 레이어의 EXR 렌더링이 {file_prefix}.####.exr 경로에 완료되었습니다.")
        publish_dict[layer]["path"] = f"{file_prefix}.####.exr"

        return publish_dict
    
    def _render_lighting_layers(self, render_path):
        print ("@@", render_path)
        dir_path = '/'.join(render_path.split('/')[:-1])
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", dir_path, type="string")
        # 렌더 레이어 선택 및 렌더링
        all_layers = cmds.ls(type="renderLayer")
        for layer in all_layers:
            # 렌더 레이어 변경
            cmds.editRenderLayerGlobals(currentRenderLayer=layer)
            
            # 배치 렌더링 수행
            cmds.arnoldRender(batch=True)
            print(f"{layer} 레이어의 EXR 렌더링이 완료되었습니다.")
    
        # import nuke
        # import os

        # path = "/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/images/ABC_0010_CMP_v001/ABC_0010_CMP_v001.####.exr"
        # first_frame = 1001
        # last_frame = 1096


        # def make_mov_with_slate_data(path, first_frame, last_frame):
        #     """nuke? lighting? """
        #     read_node = nuke.nodes.Read()
        #     read_node.knob("file").setValue(path)
        #     read_node.knob("first").setValue(first_frame)
        #     read_node.knob("last").setValue(last_frame)
            
        #     slate_node = nuke.createNode("slate_baked")
        #     slate_node.setInput(0, read_node)
        #     slate_node.knob("top_center").setValue("BAKED") # 후에 Shotgrid에서 가져온 데이터로 수정
        #     slate_node.knob("bottom_center").setValue("추예린")

        #     dirname = os.path.dirname(path)
        #     basename = os.path.basename(path)
        #     file_name = basename.split('.')[0] + ".mov"
        #     new_path = f"/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/mov/"
        #     if not os.path.exists(new_path):
        #         os.makedirs(new_path)
        #     new_path += file_name
        #     print(new_path)

        #     write_node = nuke.createNode("Write")
        #     write_node.setInput(0, slate_node)
        #     write_node.knob("file_type").setValue("mov")
        #     write_node.knob("file").setValue(new_path)

        #     nuke.execute(write_node, start=first_frame, end=last_frame, incr=1)
        


        # make_mov_with_slate_data(path, first_frame, last_frame)


# {'input path': '/home/rapa/baked/show/baked/AST/Environment/Tree/RIG/pub/maya/images/jpg/Tree_RIG_v001/Tree_RIG_v001.%04d.jpg', 'start frame': 1, 'last frame': 96, 'output_path': '/home/rapa/baked/show/baked/AST/Environment/Tree/RIG/pub/maya/movies/ffmpeg/Tree_RIG_v001_slate.mov', 'output_path_jpg': '/home/rapa/baked/show/baked/AST/Environment/Tree/RIG/pub/maya/movies/ffmpeg/Tree_RIG_v001_slate.jpg'}
# p = MayaAPI()
# p.make_ffmpeg(1001, 1096, '/home/rapa/baked/show/baked/AST/Environment/Tree/RIG/pub/maya/images/jpg/Tree_RIG_v001/Tree_RIG_v001.%04d.jpg', '/home/rapa/baked/show/baked/AST/Environment/Tree/RIG/pub/maya/movies/ffmpeg/Tree_RIG_v001_slate.mov', "baked")

# m = MayaAPI()
# m.make_ffmpeg(1001, 1096, "/home/rapa/baked/show/baked/AST/Environment/Tree/LKD/pub/maya/images/exr/Tree_LKD_v001/Tree_LKD_v001.%04d.exr", "/home/rapa/again_again_test.mov", "baked")