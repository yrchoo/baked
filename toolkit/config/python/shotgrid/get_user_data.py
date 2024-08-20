import os

class Get_User_Data():
    def __init__(self, name="추예린", project="baked", seq="ABC", shot="ABC_0010", asset="", task="CMP"):
        self.user_data = {}
        self.user_data["USER_NAME"] = os.getenv("USER_NAME")
        self.user_data["PROJECT"] = os.getenv("PROJECT")
        self.user_data["SEQ"] = os.getenv("SEQ")
        self.user_data["SHOT"] = os.getenv("SHOT")
        self.user_data["ASSET"] = os.getenv("ASSET")
        self.user_data["TASK"] = os.getenv("TASK")

        if None in self.user_data.values() :
            self.user_data["USER_NAME"] = name
            self.user_data["PROJECT"] = project
            self.user_data["SEQ"] = seq
            self.user_data["SHOT"] = shot
            self.user_data["ASSET"] = asset
            self.user_data["TASK"] = task

    def return_data(self):
        return self.user_data