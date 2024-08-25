import os

class Get_User_Data():
    def __init__(self, name="추예린", project="baked", seq="ABC", shot="ABC_0010", asset="", task="CMP", asset_type=""):
        self.user_data = {}
        self.user_data["name"] = os.getenv("NAME")
        self.user_data["project"] = os.getenv("PROJECT")
        self.user_data["sequence"] = os.getenv("SEQ")
        self.user_data["shot"] = os.getenv("SHOT")
        self.user_data["asset"] = os.getenv("ASSET")
        self.user_data["task"] = os.getenv("TASK")
        self.user_data["asset_type"] = os.getenv("ASSET_TYPE")

        if not self.user_data["name"] :
            self.user_data["name"] = name
            self.user_data["project"] = project
            self.user_data["sequence"] = seq
            self.user_data["shot"] = shot
            self.user_data["asset"] = asset
            self.user_data["task"] = task
            self.user_data["asset_type"] = asset_type

    def return_data(self):
        return self.user_data