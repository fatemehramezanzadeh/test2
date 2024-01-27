import sqlite3
import tkinter

#------------------------------------- functions -----------------------------------------

def login():
    global cnt,islogin
    user=text_user.get()
    pas=text_pass.get()
    sql=f''' SELECT * FROM users WHERE username="{user}" AND password="{pas}"'''
    result=cnt.execute(sql)
    rows=result.fetchall()

    if len(rows)<1:
        lbl_msg.configure(text="wrong username or password!",fg="red")
    else:
        lbl_msg.configure(text="welcome to your account!", fg="green")
        islogin=user
        text_user.delete(0,"end")
        text_pass.delete(0,"end")
        btn_login.configure(state="disabled")
        btn_logout.configure(state="active")
        btn_shop.configure(state="active")
        if islogin=="admin":
            btn_admin.configure(state="active")


def submit():
    def clearAll():
        text_user2.delete(0, "end")
        text_pass2.delete(0, "end")
        text_cpass.delete(0, "end")
        text_addr.delete(0, "end")
    def register():
        user=text_user2.get()
        pas=text_pass2.get()
        cpas=text_cpass.get()
        addr=text_addr.get()
        result,msg=validate(user,pas,cpas,addr)
        if not result: # if result==False
            lbl_msg2.configure(text=msg,fg="red")
        else:
            sql=f'''INSERT INTO users (username,password,address,score)
                VALUES ("{user}","{pas}","{addr}",1)'''
            cnt.execute(sql)
            cnt.commit()
            lbl_msg2.configure(text="submit done!", fg="green")
            clearAll()

    win_sub=tkinter.Toplevel(win)
    win_sub.title("Submit")
    win_sub.geometry("300x250")

    lbl_user2 = tkinter.Label(win_sub, text="username: ")
    lbl_user2.pack()
    text_user2 = tkinter.Entry(win_sub)
    text_user2.pack()

    lbl_pass2 = tkinter.Label(win_sub, text="password: ")
    lbl_pass2.pack()
    text_pass2 = tkinter.Entry(win_sub)
    text_pass2.pack()

    lbl_cpass = tkinter.Label(win_sub, text="password confirmation: ")
    lbl_cpass.pack()
    text_cpass = tkinter.Entry(win_sub)
    text_cpass.pack()

    lbl_addr = tkinter.Label(win_sub, text="address: ")
    lbl_addr.pack()
    text_addr = tkinter.Entry(win_sub)
    text_addr.pack()

    lbl_msg2 = tkinter.Label(win_sub, text="")
    lbl_msg2.pack()

    btn_sub=tkinter.Button(win_sub,text="Register",command=register)
    btn_sub.pack()

    btn_buy = tkinter.Button(win, text="shop Panel", state="disabled", command=shopPanel)
    btn_buy.pack(pady=5)

    win_sub.mainloop()

def validate(user,pas,cpas,addr):
    sql=f'''SELECT * FROM users WHERE username="{user}"'''
    result=cnt.execute(sql)

    row=result.fetchone()
    if not row is None:
        return False,"username already exist!"

    if user=="" or pas=="" or cpas=="" or addr=="":
        return False,"please fill the inputs!"
    if len(pas)<6:
        return  False,"pass length should be at least 8!"
    if pas!=cpas:
        return  False,"password and confirmation mismatch!"
    return True,""

def logout():
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    btn_admin.configure(state="disabled")
    islogin=False
    lbl_msg.configure(text="you are loggout now!",fg="green")
    btn_shop.configure(state="disabled")

def shopPanel():
    def shop():
        pid=txt_id4.get()
        pqnt=txt_qnt4.get()
        result,msg=validate_shop(pid,pqnt)
        if not result:
            lbl_msg4.configure(text=msg,fg="red")
            return
        result=update_qnt(pid,pqnt)
        if not result:
            lbl_msg4.configure(text="something went wrong while connecting db", fg="red")
            return
        # insert shop data into cart table
        #reset list


    winShop=tkinter.Toplevel(win)
    winShop.title("Shop Panel")
    winShop.geometry("400x400")

    lst=tkinter.Listbox(winShop,width=50)
    lst.pack(pady=20)

    lbl_id4=tkinter.Label(winShop,text="ID:")
    lbl_id4.pack()
    txt_id4=tkinter.Entry(winShop)
    txt_id4.pack()

    lbl_qnt4 = tkinter.Label(winShop, text="QNT:")
    lbl_qnt4.pack()
    txt_qnt4 = tkinter.Entry(winShop)
    txt_qnt4.pack()

    lbl_msg4=tkinter.Label(winShop,text="")
    lbl_msg4.pack()

    btn_shop4=tkinter.Button(winShop,text="SHOP NOW",command=shop)
    btn_shop4.pack()

    products=get_all_products()
    for product in products:
        info=f"Id:{product[0]}    Name:{product[1]}    Price:{product[2]}    QNT:{product[3]}"
        lst.insert(0,info)
    winShop.mainloop()

def get_all_products():
    sql='''SELECT * FROM products WHERE qnt>0'''
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows

def validate_shop(pid,pqnt):
    if pid=="" or pqnt=="":
        return False,"please fill the blanks"
    pqnt=int(pqnt)

    sql=f'''SELECT * FROM PRODUCTS WHERE id={pid}'''
    result=cnt.execute(sql)
    row=result.fetchone()
    if row is None:
        return False,"wrong product id"

    sql=f'''SELECT * FROM PRODUCTS WHERE id={pid} and {pqnt}<=qnt'''
    result = cnt.execute(sql)
    row = result.fetchone()
    if row is None:
        return False, "not enough products!"

    return True,""

def update_qnt(pid,pqnt):
    try:
        pqnt=int(pqnt)
        sql=f'''UPDATE products SET qnt=qnt-{pqnt} WHERE id={pid}'''
        cnt.execute(sql)
        cnt.commit()
        return True
    except:
        return False


#-----------------------------------------------------------------------------------------
cnt=sqlite3.connect("shop.db")
islogin=False

win=tkinter.Tk()
win.title("Login")
win.geometry("300x300")

lbl_user=tkinter.Label(win,text="username: ")
lbl_user.pack()
text_user=tkinter.Entry(win)
text_user.pack()

lbl_pass=tkinter.Label(win,text="password: ")
lbl_pass.pack()
text_pass=tkinter.Entry(win)
text_pass.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

btn_login=tkinter.Button(win,text="Login",command=login)
btn_login.pack()

btn_submit=tkinter.Button(win,text="Submit",command=submit)
btn_submit.pack(pady=10)

btn_logout=tkinter.Button(win,text="Logout",command=logout,state="disabled")
btn_logout.pack()

btn_admin=tkinter.Button(win,text="Admin Panel",state="disabled")
btn_admin.pack(pady=5)

btn_shop=tkinter.Button(win,text="shop Panel",state="disabled", command=shopPanel)
btn_shop.pack(pady=5)

btn_buy=tkinter.Button(win,text="shop Panel",state="disabled", command=shopPanel)
btn_buy.pack(pady=5)
def update_qnt(pid,pqnt):
    try:
        pqnt=int(pqnt)
        sql=f'''UPDATE products SET qnt=qnt-{pqnt} WHERE id={pid}'''
        cnt.execute(sql)
        cnt.commit()
        return True
    except:
        return False

    def validate_buy(uid):
        if uid == "" or pqnt == "":
            return False, "please fill the blanks"
        uid= int(uid)



win.mainloop()

import json
{"color":"read"}

#  def login----------------------------------

def login(user, pas):
    info = readwrite()

    if (user in info) and (info[user] == pas):
        return True
    else:
        return False


#  def validatation---------------------------


def validate(user, pas, cpas):
    info=readwrite()

    if pas != cpas:
        return False, " password and configpass mismatch ! "
    if len(pas) < 5:
        return False, " password is least than 5 character ! "
    # if  (user in info ) and (info[user]==pas):
    if user in info:
        return False, " user already exist"
    return True, ""


#  def submit---------------------------------


def submit(user, pas):
    info = readwrite()
    info[user] = pas
    readwrite(info)
    print("submit done ! ")



def deleteAccount():
    global islogin
    if not islogin:  # islogin==False
        print("please login first!")
        return
    if islogin == "admin":
        print("access denied!")
        return
    confirm = input("are you sure? yes/no")
    if confirm != "yes":
        print("canceled by user!")
        return

    info = readwrite()
    info.pop(islogin)
    readwrite(info)

    islogin=False
    print("account deleted successfully!")


def logout():
    global islogin
    if not islogin:
        print("please login first!")
        return
    islogin=False

def readwrite(info=False):
    if not info: #(if info==False)
        with open("users.json") as f:
            return json.load(f)
    else:
        with open("users.json", 'w') as f:
            json.dump(info, f)


# **********************************************************************************************
# **********************************************************************************************



islogin = False

#  start -------------------------------


while (True):
   print('1.login  2.submit  3.delet  4.edit  5.logout  6.exit')
   plan = input(' what is your plan ? ')


   if plan == "1":
        if islogin != False:
            print("you are already logged in!")
            continue
        user = input("enter user : ")
        pas = input("enter pas : ")
        result = login(user, pas)
        if result:
            print(' welcom to your account ')
            islogin = user
        else:
            print(' wrong pas or user ! ')
   elif plan == "2":
        user = input("enter user : ")
        pas = input("enter pas : ")
        cpas = input("enter cpas : ")

        result, errormsg = validate(user, pas, cpas)
        if result == False:
            print(errormsg)
            continue
        submit(user, pas)

   elif plan == "3":
       deleteAccount()

   elif plan == "4":
       if not islogin:  # islogin==False
           print("please login first!")
           continue
       oldpass=input("old password")
       newpass=input("new password: ")
       cnewpass=input("new password confirmation: ")
       if not login(islogin,oldpass):
           print("wrong old password!")
           continue
       result,errormsg=validate(False,newpass,cnewpass)
       if not result:
                  print(errormsg)
                  continue

       info = readwrite()

       info[islogin]=newpass


       readwrite(info)
       print("password has been changed!")


   elif plan=="5":
        logout()
        print("you are logged out now!")
   elif plan == "6":
       break

   else:
        print("wrong input!")
class fileAction:
    def __init__(self,fileName):
        self.fileName=fileName

    def readFile(self):
        with open(self.fileName) as f:
            content=f.read()
            print(content)
f1=fileAction("doc1.txt")
f1.readFile()

f2=fileAction("doc2.txt")
f2.readFile()