import os
import subprocess

class Make_User_Data():
    def __init__(self, name="추예린", project="baked", seq="ABC", shot="ABC_0010", asset="", task="CMP",asset_type=""):
        user_file_path = "/home/rapa/env_baked/user/"
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

        os.system(f"echo '#!/bin/sh\n {user_string}' > {user_file_path}/user.sh")
        subprocess.run(['python3.9', '/home/rapa/baked/toolkit/config/python/fetch_shotgrid_data.py', '&'])


Make_User_Data()