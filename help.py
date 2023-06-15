import sqlite3


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


email = User_Data().get_mail("admin", "admin")
uid = User_Data().get_id("admin", "admin", "admin")
img = User_Data().get_picture(1)
print(email, uid, img)
