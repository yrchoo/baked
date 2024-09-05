import subprocess,glob,os
input_file = "/home/rapa/baked/show/baked/AST/Character/Choo/LKD/pub/maya/images/exr/Choo_LKD_v002/Choo_LKD_v002.%04d.exr"
input_dir = os.path.dirname(input_file) # 폴더 경로
input_filename = os.path.basename(input_file) # Choo_MOD_v001.%04d.exr
files = glob.glob(f"{input_dir}/*")
input_file = max(files, key=os.path.getmtime) # Choo_MOD_v001.1096.exr
output_dir = f"{input_dir}/thumbnail/"
if not os.path.exists(output_dir):
    os.path.makedir(f"{input_dir}/thumbnail")
output_file = f"{output_dir}{input_filename}"
output_file = output_file.replace(".%04d.exr", ".jpg")
print ("---------------------------------------------------------------------")
print (input_dir)
print (input_filename)
print (input_file)
print (output_file)
print ("---------------------------------------------------------------------")

try:
    # FFmpeg 명령어 구성
    command = [
        'ffmpeg',
        '-i', input_file,   # 입력 파일 (EXR)
        '-q:v', "2",  # 품질 설정
        output_file          # 출력 파일 (JPG)
    ]
except:
    pass
    # FFmpeg 명령 실행
subprocess.run(command, check=True)