import os
import subprocess

class Make_User_Data():
    def __init__(self, name, project, seq, shot, asset, task, asset_type):
        user_file_path = "/home/rapa/baked/toolkit/config/core/user"
        user_string = f"""
export NAME='{name}'
export PROJECT='{project}'
export SEQ='{seq}'
export SHOT='{shot}'
export ASSET='{asset}'
export TASK='{task}'
export ASSET_TYPE='{asset_type}'
        """
        if not os.path.exists(user_file_path) :
            os.makedirs(user_file_path)
        print(f"create user data {user_string}")
        os.system(f"""echo "#!/bin/sh\n {user_string}" > {user_file_path}/user.sh""")
        # subprocess.Popen(['nohup', 'python3.9', '/home/rapa/baked/toolkit/config/python/shotgrid/fetch_shotgrid_data.py', '&'],
        #                     stdout=subprocess.DEVNULL,
        #                     stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    Make_User_Data("Yerin Choo", "baked", "ABC", "ABC_0010", "", "CMP", "")