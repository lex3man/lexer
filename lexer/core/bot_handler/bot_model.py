from core.models import TgBot
from Content_and_logic.models import TypeBlock, Command, keyboard, keyboard_button
import random, string

# class Bot:
#     def __fillActions(self, action_name):
#         Action()
#         return Action
    
#     def execute(self, header, *args):
#         result = self.__fillActions(header).execute(*args)
#         return JsonResp(result)

def GetSessionID():
    code = ''.join(random.choices(string.ascii_letters, k = 15))
    return code

class BotHandler:
    name : str
    token : str
    
    def __new__(self, name, token):
        self.session = GetSessionID()
        self.name = name
        self.token = token
        return self
    
    def feelaction(self, message, content_type):
        pass