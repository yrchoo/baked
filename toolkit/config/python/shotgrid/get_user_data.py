import os

class Get_User_Data():
    def __init__(self, name="", project="", seq="", shot="", asset="", task="", cur=""):
        self.user_data = {}
        self.user_data["USER_NAME"] = os.getenv("USER_NAME")
        self.user_data["PROJECT"] = os.getenv("PROJECT")
        self.user_data["SEQ"] = os.getenv("SEQ")
        self.user_data["SHOT"] = os.getenv("SHOT")
        self.user_data["ASSET"] = os.getenv("ASSET")
        self.user_data["TASK"] = os.getenv("TASK")
        self.user_data["CURRENT"] = os.getenv("CURRENT")

    def return_data(self):
        return self.user_data