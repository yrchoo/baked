import ffmpeg, os

class MakeSlate():
    def make_ffmpeg_jpg(self, top_left, top_center, top_right, bot_left, bot_center, bot_right, input_path, output_path):
        
        self.find_frame(input_path)
        input_path = input_path.replace('jpg', 'jpeg')
        output_path = output_path.replace('jpg', 'jpeg')
        print ("ffmepg", input_path, output_path)
        # self.input_jpg_slate(top_left, top_center, top_right, bot_left, bot_center, bot_right)
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
        cmd = f'ffmpeg -f image2 -c:v mjpeg -fflags +discardcorrupt -analyzeduration 100M -probesize 100M -i {input} -frames:v 1 -vf "{vf_filter}" -y {output}'
        
        # ffmpeg 명령어 실행
        os.system(cmd)


# p = MakeSlate()
# p.make_ffmpeg_jpg("a", "b", "c", "d", "e", "f", "/home/rapa/baked/show/baked/AST/Environment/Tree/MOD/dev/maya/images/captures/Tree_MOD_v012_capture.jpg", "/home/rapa/great.jpg")