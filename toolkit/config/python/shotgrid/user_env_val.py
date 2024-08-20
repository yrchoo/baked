import os

class Make_User_Data():
    def __init__(self, name="추예린", project="baked", seq="ABC", shot="ABC_0010", asset="", task="CMP", cur="ABC_0010"):
        user_file_path = "/home/rapa/env_baked/user/"
        user_string = f"""
export USER_NAME='{name}'
export PROJECT='{project}'
export SEQ='{seq}'
export SHOT='{shot}'
export ASSET='{asset}'
export TASK='{task}'
export CURRENT='{cur}'
        """
        if not os.path.exists(user_file_path) :
            os.makedirs(user_file_path)

        os.system(f"echo '#!/bin/sh\n {user_string}' > {user_file_path}/user.sh")


Make_User_Data()