import mysql.connector as ms
import time
db=ms.connect(host='localhost',user='root',passwd='yourpass',database='yourdatabse')
myc=db.cursor()

def choice():
    print("1. SignUp")
    print("2. Login")
    print("3. View Leader Board")
    inputChoice=int(input("Enter your choice: "))
    if(inputChoice==1):
        SignUp()
    elif(inputChoice==2):
        Login()
    elif(inputChoice==3):
        LeaderBoard()
    else:
        choice()

def SignUp():
    print("\n" * 20)
    userName=input("Enter User Name to Sign Up: ")
    myc.execute("select Name from userData where Name='{Name}'".format(Name=userName))
    tmp1=myc.fetchall()

    if(tmp1==[]):
        password = input("Enter Password for your account: ")
        weight=int(input("Enter your weight in Kg: "))
        height=int(input("Enter your height in cms: "))
        sql = "insert into userData values('{}','{}',{},{},{},{},{})".format(userName, password,20,0,0,weight,height)
        myc.execute(sql)
        db.commit()

        print("\n(+_+) Your account has been created")
        Login()
    else:
        print("\nOops!Seems a account already exists with this name.Please try with different name")

def Login():
    print("\n"*20)
    userName = input("Enter User Name: ")
    com = "select Name from userData where Name='{Name}'".format(Name=userName)
    myc.execute(com)
    tmp1 = myc.fetchall()

    if(tmp1!=[]):
        password = input("Enter Password: ")
        com = "select Password from userData where Name='{Name}'".format(Name=userName)
        myc.execute(com)
        tmp2 = myc.fetchall()
        #print(tmp2)
        for i in tmp2:
            if (i[0] == password):
                for i in "Login Successful":
                    print(i,end="")
                    time.sleep(0.06)
                time.sleep(2)
                DashBoard(userName)
            else:
                print("password incorrect")
    else:
        print("Account not found")

def DashBoard(user):
    print("\n" * 20)
    print("\nHi,",user)
    time.sleep(2)
    myc.execute("select Weight from userData where Name='{Name}'".format(Name=user))
    weight = myc.fetchall()
    myc.execute("select Height from userData where Name='{Name}'".format(Name=user))
    height = myc.fetchall()
    myc.execute("select target from userData where Name='{Name}'".format(Name=user))
    target = myc.fetchall()
    myc.execute("select pushUps from userData where Name='{Name}'".format(Name=user))
    pushUps = myc.fetchall()

    for i in weight:
        print("\tYour weight: ",i[0])
        weightF=i[0]
    for i in height:
        print("\tYour height: ", i[0])
        BMI=weightF/(i[0]/100)**2
        print("\tYour BMI: ","%.2f"%BMI)
    for i in target:
        print("\tYour target: ",i[0])
        tmp5=i[0]
    for i in pushUps:
        print("\tNo. of push ups you have done: ",i[0])
        tmp6=i[0]
        if(tmp5<=tmp6):
            print("\nYay! you have reached your target\n")
        else:
            percentage=(tmp6/tmp5)*100
            print("\nOops! you haven't reached your target. And,")
            print("you have completed,","%.2f"%percentage,"% of your goal\n")
    time.sleep(3)
    print("\t1. Update today's health stats\n\t2. Change Target\n\t3. Log Out")
    choice=int(input("\t\tEnter your choice: "))
    if (choice == 1):
        ChangeIT(user, 1)
    if(choice==2):
        ChangeIT(user,2)

def ChangeIT(user,c):
    if (c == 1):
        valueInput = int(input("\t\tEnter No. of push ups you done today: "))
        myc.execute("update userData set pushUps ={value} where Name='{Name}'".format(value=valueInput, Name=user))
        db.commit()
        DashBoard(user)
    elif(c==2):
        valueInput = int(input("\t\tWhat's your target?: "))
        myc.execute(f"update userData set target ={valueInput} where Name='{user}'")
        db.commit()
        myc.execute("update userData set target ={value} where Name='{Name}'".format(value=valueInput, Name=user))
        db.commit()
        DashBoard(user)

def LeaderBoard():
    print("\n" * 20)
    print("------------\nLeader Board\n------------")
    myc.execute("select Name ,pushUps from userData order by pushUps desc")
    tmp6=myc.fetchall()
    for i in tmp6:
        print(i[0],":", i[1])
        time.sleep(0.3)

print("\nWelcome to Health Management System")

choice()
