import os
# git 내부에 있는 모든 파일을 돌면서 .gitkeep 파일을 추가해주는 코드입니다

path = "/Users/yerin/Desktop/NetflixAcademy/baked" # 각자 환경에 맞는 파일 경로로 수정하여 사용하세요


def _find_empty_dir(path):
    file_list = os.listdir(path)
    
    for file in file_list:
        if os.path.isdir(f"{path}/{file}"):
            _find_empty_dir(f"{path}/{file}")

    if file_list : return

    print(path)
    os.system(f"touch {path}/.gitkeep")

_find_empty_dir(path)