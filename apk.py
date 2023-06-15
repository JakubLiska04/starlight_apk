from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from tkinter import filedialog
from kivy.uix.scrollview import ScrollView

kv = Builder.load_file("apk.kv")


class Database():
    def database(self):
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE if not exists data(id INTEGER PRIMARY KEY,
                        Username VARCHAR(255), Email VARCHAR(255), Password VARCHAR(255), 
                        Price DECIMAL(20,2), Budget DECIMAL(20,2), Designer BOOL, Customer BOOL, Picture BLOB)""")
        data = []
        data = cur.execute("SELECT * FROM data")
        data = cur.fetchall()
        con.commit()
        con.close()
        return data

# enter na log in, reg a pod.


class User_Data():

    def get_id(self, Username, Email, Password):
        self.Username = Username
        self.Email = Email
        self.Password = Password
        data = Database().database()
        user_id_list = []
        for row in data:
            user_id = row[0]
            nickname = row[1]
            mail = row[2]
            passwords = row[3]
            if nickname == Username and mail == Email and passwords == Password:
                if nickname > "" and mail > "" and passwords > "":
                    user_id_list.append(user_id)
        try:
            return(user_id_list[0])
        except IndexError:
            return(0)

    def get_picture(self, uid):
        self.uid = uid
        data = Database().database()
        profile_list = []
        for row in data:
            picture = row[8]
            ids = row[0]
            if ids == uid:
                profile_list.append(picture)
        try:
            return(profile_list[0])
        except IndexError:
            return(0)

    def get_mail(self, Username, Password):
        self.Username = Username
        self.Password = Password
        data = Database().database()
        email_list = []
        for row in data:
            username = row[1]
            password = row[3]
            mail = row[2]
            if username == Username and password == Password:
                email_list.append(mail)
        try:
            return(email_list[0])
        except IndexError:
            return(0)


class Register(Screen):
    pass


class LogIn(Screen):
    pass


class Profile(Screen):
    pass


class Designer(Screen):
    pass


class MainScreen(Screen):
    pass


class ProfileEdit(Screen):
    pass


class Chats(Screen):
    pass


class Password_change(Screen):
    pass


class Designer_edit(Screen):
    pass


class Customer_edit(Screen):
    pass


class Profile_delete(Screen):
    pass


class Works(Screen):
    pass


class Order(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        Window.size = [300, 600]
        # screens
        sm = ScreenManager()
        sm.add_widget(Register(name="register"))
        sm.add_widget(LogIn(name="log_in"))
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(Profile(name="profile"))
        sm.add_widget(Password_change(name="password_change"))
        sm.add_widget(Designer(name="designer"))
        sm.add_widget(ProfileEdit(name="profile_edit"))
        sm.add_widget(Designer_edit(name="designer_edit"))
        sm.add_widget(Customer_edit(name="customer_edit"))
        sm.add_widget(Chats(name="chats"))
        sm.add_widget(Profile_delete(name="profile_delete"))
        sm.add_widget(Works(name="works"))
        sm.add_widget(Order(name="order"))
        return sm

    def log_in(self):
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        img = User_Data().get_picture(uid)

        if uid > 0:
            self.root.get_screen("profile").ids.profile.text = username
            self.root.get_screen("password_change").ids.profile.text = username
            self.root.get_screen("designer").ids.profile.text = username
            self.root.get_screen("profile_delete").ids.profile.text = username
            self.root.get_screen(
                "profile_edit").ids.profile.text = username
            self.root.current = "main_screen"
            if img != None:
                self.root.get_screen("designer").ids.profile_pic.icon = img
                self.root.get_screen("profile").ids.profile_pic.icon = img
                self.root.current = "main_screen"
                print("Welcome", email, uid)
        else:
            print("Log in Failed")

    def register(self):
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        username = self.root.get_screen('register').ids.username.text
        email = self.root.get_screen('register').ids.email.text
        password = self.root.get_screen('register').ids.password.text
        data_acc = [(username), (email), (password)]
        data = Database().database()
        usernames = []
        mails = []
        for line in data:
            nickname = line[1]
            mail = line[2]
            usernames.append(nickname)
            mails.append(mail)
        if username not in usernames:
            if email not in mails:
                if username != "":
                    if email != "":
                        if password != "":
                            if username.isalnum() and password.isalnum() == True:
                                cur.execute(
                                    "INSERT INTO data(username, email, password) VALUES(?,?,?)", data_acc)
                                self.root.get_screen(
                                    "profile").ids.profile.text = username
                                con.commit()
                                con.close()
                                print("Registered")
                                self.root.transition.direction = "left"
                                self.root.current = "main_screen"
                            else:
                                print(
                                    "Use only valid letters(A-Z) and numbers (0-9)")
                        else:
                            print("Fill in the blanks please!")
                    else:
                        print("Fill in the blanks please!")
                else:
                    print("Fill in the blanks please!")
            else:
                print("Someone is already using this email!")
        else:
            print("Username is already taken!")

    def stay_signed(self):
        button = self.root.get_screen("log_in").ids.stay_signed
        signed_in = button.icon = "checkbox-marked"
        signed_out = button.icon = "checkbox-blank-outline"
        if button == "down":
            button = signed_in
            print("You will be signed in!")
        else:
            button = signed_out
            print("You will be signed out!")
        pass

    def forgot_password(self):
        print("You forgot password????")

    def log_out(self):
        self.root.get_screen("log_in").ids.username.text = ""
        self.root.get_screen("log_in").ids.password.text = ""
        self.root.get_screen("register").ids.username.text = ""
        self.root.get_screen("register").ids.email.text = ""
        self.root.get_screen("register").ids.password.text = ""
        self.root.current = "log_in"

    def designer_submit(self):
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        Price = self.root.get_screen("designer_edit").ids.price.text
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        cur.execute('UPDATE data  SET price=? WHERE id=?',
                    (Price, uid,))
        print("success")
        con.commit()
        con.close()

    def customer_submit(self):
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        budget = self.root.get_screen("customer_edit").ids.budget.text
        cur.execute('UPDATE data  SET Budget=? WHERE id=?',
                    (budget, uid,))
        print("success")
        con.commit()
        con.close()

    def set_profile(self):
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        designer = self.root.get_screen(
            "profile_edit").ids.designer_button.state
        customer = self.root.get_screen(
            "profile_edit").ids.customer_button.state
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        if designer == "down":
            cur.execute('UPDATE data SET designer=? WHERE id=?',
                        (True, uid))
            print('Done!')

        if customer == "down":
            cur.execute('UPDATE data SET customer=? WHERE id=?',
                        (True, uid))
            print('Done!')

        con.commit()
        con.close()

    def upload_profile_pic(self):
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        picture = filedialog.askopenfilename(initialdir="/",
                                             title="Select a File",
                                             filetypes=(("picture",
                                                         "*.png*"),
                                                        ("all files",
                                                         "*.*")))
        cur.execute(
            "UPDATE data  SET Picture=? WHERE id=? ", (picture, uid))
        self.root.get_screen("designer").ids.profile_pic.icon = picture
        self.root.get_screen("profile").ids.profile_pic.icon = picture
        con.commit()
        con.close()

    def password_change(self):
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        old_password = self.root.get_screen(
            "password_change").ids.old_password.text
        new_password = self.root.get_screen(
            "password_change").ids.new_password.text
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        if old_password == password:
            cur.execute("UPDATE data SET password = ? WHERE id=?",
                        (new_password, uid))
            con.commit()
            con.close()
            print("Success!")

            self.root.get_screen(
                'password_change').ids.profile.text = ''
            self.root.get_screen(
                "password_change").ids.old_password.text = ''
            self.root.get_screen(
                "password_change").ids.new_password.text = ''
            self.root.get_screen("log_in").ids.username.text = ""
            self.root.get_screen("log_in").ids.password.text = ""
            self.root.get_screen("register").ids.username.text = ""
            self.root.get_screen("register").ids.email.text = ""
            self.root.get_screen("register").ids.password.text = ""
            self.root.current = "log_in"
        else:
            self.root.get_screen(
                'password_change').ids.profile.text = 'Wrong Password!'

    def upload_work(self):
        pass

    def search(self):
        # vyhľadávanie účtov nick--> id v databáze
        pass

    def delete_data(self):
        con = sqlite3.connect("apk.db")
        cur = con.cursor()
        username = self.root.get_screen('log_in').ids.username.text
        password = self.root.get_screen('log_in').ids.password.text
        email = User_Data().get_mail(username, password)
        uid = User_Data().get_id(username, email, password)
        cur.execute("DELETE FROM data WHERE id=?", (uid,))
        con.commit()
        con.close()


if __name__ == '__main__':
    MainApp().run()
