import os
import subprocess
input_mov = "/home/rapa/baked/show/baked/AST/Character/Choo/MOD/pub/maya/movies/ffmpeg/Choo_MOD_v001_slate.mov"
mov_dir = os.path.dirname(input_mov)
mov_name = os.path.basename(input_mov)
mov_name, _ = os.path.splitext(mov_name)
img_path = f"{mov_dir}/{mov_name}.jpg"
frame_number = 24
command = ['ffmpeg', '-y', '-i', input_mov, '-vf', f"select='eq(n\,{frame_number})'", '-vsync', 'vfr', '-frames:v', '1', img_path]
subprocess.run(command)