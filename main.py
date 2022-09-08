from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


from matplotlib.style import available

Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users= json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current="login_screen_success"
        else:
            self.ids.wrong_details.text="Wrong credentials, please try again!"    

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users= json.load(file)
        users[uname]={'username': uname, 'password': pword,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        with open("users.json",'w') as file:
            json.dump(users, file)
        self.manager.current="sign_up_screen_success"    

class SignUpScreenSuccess(Screen):
    def login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"   

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'       
        self.manager.current="login_screen" 

    def get_quote(self, feel):     
        feel=feel.lower()
        available_feel=glob.glob("quotes/*")
        available_feel=[Path(filename).stem for filename in available_feel]
        
        quotes={}
        if feel in available_feel:
            name=f"quotes/{feel}.txt"
            with open(name) as file:
                quotes=file.readlines()
            self.ids.quote.text= random.choice(quotes)
        else:
            self.ids.quote.text="Please try another feeling!"  

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass            

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()



#Shift-Alt-F to format json file 