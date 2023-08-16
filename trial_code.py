import os
import math
from datetime import date
import mysql.connector

def add_book(mycursor_admin_add, mydb):
    book_name=input("\nEnter the name of the book : ")
    book_author=input("Author name : ")
    book_topic=input("Topic of the book : ")
    book_publisher=input("Book publisher : ")
    while True:
        try:
            book_price=float(input("Price of the book : "))
            break
        except:
            print("Enter a number")
    str_bookadder="INSERT INTO BOOK_MANAGER(Book_Name,Author,Topic,Publisher,Price) VALUES(%s,%s,%s,%s,%s)"
    print("")
    book_data = (book_name, book_author, book_topic, book_publisher, book_price)
    try:
        mycursor_admin_add.execute(str_bookadder,book_data)
        book_id=mycursor_admin_add.lastrowid
        mydb.commit()
        print("Book added succesfully")
        print(f"Book Id = {book_id}")
    except Exception as e:
        print(f'''Error : Book not added
              Error Statement- {e}''')
    finally:
        print("\n")


def remove_book(mycursor_admin_remove,mydb):
            while True:
#         remove_choice=input('''\nSelect the operation to remove the book-
# 1. Remove by Book_Id
# 2. Back\n''')
        # try:
        #     remove_choice=int(remove_choice)
            # if remove_choice==1:
                book_id=input("Enter the book_id or book_no : ")
                try:
                    book_id=int(book_id)
                    book_remover="UPDATE BOOK_MANAGER SET Issue_Status='Not Available' WHERE Book_No=%s"
                    try:
                        check_book_existence = "SELECT * FROM BOOK_MANAGER WHERE Book_No=%s"
                        check_book_available = "SELECT Issue_Status FROM BOOK_MANAGER WHERE Book_No=%s"
                        mycursor_admin_remove.execute(check_book_existence, (book_id,))
                        book = mycursor_admin_remove.fetchone()
                        mycursor_admin_remove.execute(check_book_available, (book_id,))
                        book_av=mycursor_admin_remove.fetchone()
                    except:
                        print("Unable to fetch book to compare.")
                    if book:
                        if book_av[0] == 'Not Issued':
                            try:
                                mycursor_admin_remove.execute(book_remover,(book_id,))
                                mydb.commit()
                                print("\nBook removed succesfully, no longer available for issue")
                                print(f"{book_av}")
                            except Exception as e:
                                print("Removal Unsuccesful")
                                print(f"Error- {e}")
                        else:
                            print(f"\nCannot not Remove book since Book status is : {book_av[0]}")
                        break
                    else:
                        print("\nBook not found in the database")
                        break
                except:
                    try:
                        book_id=float(book_id)
                        print("\nEnter an integer, not a decimal number.")
                    except:
                        print("\nNumeric Input expected")
            print("\n")
            # elif remove_choice==2:
                # pass
            # elif remove_choice==2:
            #     break
            # else:
            #     print("Choose 1 or 2")
        # except:
        #     try:
        #         remove_choice=float(remove_choice)
        #         print("Wrong input! Enter an integer, not a decimal number")
        #     except:
        #         print("Wrong input! Numeric input expected")
            # finally:
            #     print("\n")


def check_member(mycursor_admin_membercheck,mydb):
    while True:
        admin_choose_ip=input('''\nSelect the way to search the member-
1. Search by Member_Id
2. Search by Member_Name
3. Back\n''')
        try:
            admin_choose_ip=int(admin_choose_ip)
            if admin_choose_ip==1:
                while True:
                    admin_memberid_ip=input("\nEnter the Member Id : ")
                    try:
                        admin_memberid_ip=int(admin_memberid_ip)
                        break
                    except:
                        print("\nNumeric input expected")
                user_bringer="SELECT Membership_No,Member_Name,Member_MobNo,Member_Add,Fine_Amt,Membership_Status,Joining_Date,Leave_Date FROM Member_Manager WHERE Membership_No=%s"
                try:
                    mycursor_admin_membercheck.execute(user_bringer,(admin_memberid_ip,))
                    Member_receiver=mycursor_admin_membercheck.fetchall()
                    print("")
                    #print(type(Member_receiver))
                except Exception as e:
                    print("Error! Could not search member")
                    print(f"Error - {e}")
                if not Member_receiver:
                    print("Member not found")
                else:
                    n=('Membership_No','Name','Mobile_No','Address','Fine_Amt','Membership_Status','JoinDate','LeaveDate')
                    m=Member_receiver[0]
                    print("Member found\n")
                    for i,j in zip(n,m):
                        if j==None:
                            continue
                        print(f"{i} : {j}")
                    input("Press Enter to continue")

            elif admin_choose_ip==2:
                while True:
                    m_name=input("\nEnter Member Name : ")
                    try:
                        m_name=float(m_name)
                        print("\nDid not expect numeric input")
                    except:
                        break
                mFindstr="SELECT Membership_No,Member_Name,Member_MobNo,Member_Add,Fine_Amt,Membership_Status,Joining_Date,Leave_Date FROM MEMBER_MANAGER WHERE Member_Name LIKE %s"
                try:
                    search_pattern = f"%{m_name}%"
                    mycursor_admin_membercheck.execute(mFindstr,(search_pattern,))
                    Member_receiver=mycursor_admin_membercheck.fetchall()
                    print("")
                except Exception as e:
                    print("Error! Could not search member")
                    print(f"Error - {e}")
                if not Member_receiver:
                    print("Member not Found")
                else:
                    o=('Membership_No','Name','Mobile_No','Address','Fine_Amt','Membership_Status','JoinDate','LeaveDate')
                    m=Member_receiver
                    if len(m)==1:
                        print("Member found\n")
                    else:
                        print("Members found\n")
                    for item in m:
                        print(" ")
                        if item[7]==None:
                            for i in range (0,7):
                                print(f"{o[i]} : {item[i]}")
                        else:
                            for i in range (0,8):
                                print(f"{o[i]} : {item[i]}")
            elif admin_choose_ip==3:
                break
            else:
                print("Enter between 1 to 3")
        except:
            try:
                admin_choose_ip=float(admin_choose_ip)
                print("Wrong input! Enter an integer, not a decimal number")
            except:
                print("Wrong input! Numeric input expected")
        finally:
            print("\n")


def addMember_byAdmin(mycursor_admin_addmember,mydb):
    print(" ")
    Member_Name=input("Member Name : ") #Name should not have numerical value
    Member_MobNo=input("Mobile No : ") #Should have only numeric value
    Member_Address=input("Address : ")
    Member_EmailId=input("Email Id : ")
    Member_IdPt=input("Id Proof Type(Aadhar/PAN/DL/) : ")
    Member_IdP_No=input("Id Proof No : ")
    Member_JoinDate=input("Joining Date(null if not older) : ")
    if Member_JoinDate=='null' or Member_JoinDate=='Null':
        Member_JoinDate=date.today()
    Member_Password=input("Create Password : ")
    str_memberadder="INSERT INTO MEMBER_MANAGER(Member_Name,Member_MobNo,Member_Add,Member_EmailId ,IdProof_Type,IdProof_No,Joining_Date,PASSWORD) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    print("")
    Member_Data=(Member_Name,Member_MobNo,Member_Address,Member_EmailId,Member_IdPt,Member_IdP_No,Member_JoinDate,Member_Password)
    try:
        mycursor_admin_addmember.execute(str_memberadder,Member_Data)
        Member_Id = mycursor_admin_addmember.lastrowid
        mydb.commit()
        print("Member added succesfully")
        print(f"Member Id = {Member_Id}")
    except Exception as e:
        print("Error : Member not added")
        print(f"Error Statement- {e}")
    finally:
        print("\n")


def removeMember_byAdmin(mycursor_admin_removemember,mydb):
    # while True:
    Member_Id=input("\nEnter the Membership No : ")
    try:
        Member_Id=int(Member_Id)
        Member_remover="UPDATE MEMBER_MANAGER SET Membership_Status='NOT_ACTIVE' WHERE Membership_No=%s"
        try:
            checkMemberExistence = "SELECT Membership_No, Member_Name, Fine_Amt, Joining_Date FROM MEMBER_MANAGER WHERE Membership_No=%s"
            checkRemoveAvailability = "SELECT Fine_Amt, IssuedBooks FROM MEMBER_MANAGER WHERE Membership_No=%s"
            mycursor_admin_removemember.execute(checkMemberExistence, (Member_Id,))
            MemberData=mycursor_admin_removemember.fetchone()
        except:
            print("Unable to fetch Member Data")
        if not MemberData:
            print("Member not found")
        else:
            try:
                mycursor_admin_removemember.execute(checkRemoveAvailability, (Member_Id,))
                MemberRemoveAvail=mycursor_admin_removemember.fetchone()
            except:
                print("Could not fetch Fine Amount or Issued Status")
            if MemberRemoveAvail[0]==0 and MemberRemoveAvail[1]==0:
                try:
                    mycursor_admin_removemember.execute(Member_remover, (Member_Id,))
                    print("Member Removed")
                    print(" ")
                except Exception as e:
                    print(f"Error in removing member - {e}")
            else:
                memberRemoveAvailData=('Fine', 'Currently issued books')
                memberRemoveAvailDict=dict(zip(memberRemoveAvailData, MemberRemoveAvail))
                print("Cannot remove member")
                try:
                    for key, value in memberRemoveAvailDict.items():
                        if value!=0:
                            print(f"{key} : {value}")
                    print("Clear the Member Dues before removing")
                except Exception as e:
                    print(f"{e}")
    except:
        try:
            Member_Id=float(Member_Id)
            print("Integer input expected, not Decimal input")
        except:
            print("Numeric input expected")
    finally:
        print("\n")


def start_msg():
    while True:
        user_ip=input('''Select the Login Mode -
1. Admin
2. Member
3. Guest
4. New User (Create Account)
5. Exit\n''')
        print("")
        try:
           user_ip=int(user_ip)
           if 1<=user_ip<=5:
               return user_ip
           else:
               print("Wrong input! Enter an integer between 1 to 5")
        except:
            try:
                user_ip=float(user_ip)
                print("Wrong input! Enter an integer, not a decimal number")
            except:
                print("Wrong input! Numeric input expected")
        finally:
            print("")


def admin_chosen(mycursor_admin, mydb):
    obtain_pass="SELECT PASSWORD FROM MEMBER_MANAGER WHERE Member_Name='ADMIN'"
    mycursor_admin.execute(obtain_pass)
    admin_pass_result=mycursor_admin.fetchone()
    while True:
        admin_pass=input("Enter the Admin Password : ")
        if admin_pass_result and admin_pass_result[0]==admin_pass:
            print("\nWelcome Admin!")
            break
        elif admin_pass=="b" or admin_pass=="B":
            return
        else:
            print("\nIncorrect Password : Try Again\n")
            print("\nPress b for Back")

    while True:
        admin_ip=input('''Choose the input-
1. Add Book
2. Remove Book
3. Check Member
4. Add Member
5. Remove Member
6. Search Book
7. Logout
''')
        try:
            admin_ip=int(admin_ip)
            if 1<=admin_ip<=7:
                if admin_ip==1:
                    add_book(mycursor_admin, mydb)
                elif admin_ip==2:
                    remove_book(mycursor_admin,mydb)
                elif admin_ip==3:
                    check_member(mycursor_admin,mydb)
                elif admin_ip==4:
                    addMember_byAdmin(mycursor_admin,mydb)
                elif admin_ip==5:
                    removeMember_byAdmin(mycursor_admin,mydb)
                elif admin_ip==6:
                    pass
                elif admin_ip==7:
                   return
            else:
               print("Wrong input! Enter an integer between 1 to 5")
        except:
            try:
                admin_ip=float(admin_ip)
                print("Wrong input! Enter an integer, not a decimal number")
            except:
                print("Wrong input! Numeric input expected")


def newUser_chosen(myCursor_newUser,mydb):
    status=0
    names = ['ADMIN', "admin", 'Admin', 'ADMINISTRATOR', 'administrator', 'Administrator']
    while True: #Apply the condition to not allow numbers in name field -> Done
        Member_Name=input("Enter Name : ")
        if Member_Name not in names:
            try:
                Member_Name_a=float(Member_Name)
                print("Only alphabets expected")
            except:
                break
        else:
            print("\nThis name is not allowed")
            print("Choose another name\n")
    while True:
        Member_MobNo=input("Mobile No : ") #Apply the condition for only numbers in this field -> Done
        try:
            Member_MobNo_2=int(Member_MobNo)
            if len(Member_MobNo)!=10:
                print("\nIncorrect Mobile No format")
                continue
            else:
                break
        except:
            print("\nMobile No. expected")
    Member_Address=input("Address : ")
    Member_EmailId=input("Email Id : ")
    Member_IdPt=input("Id Proof Type(Aadhar/PAN/DL/) : ")
    Member_IdP_No=input("Id Proof No : ")
    Member_JoinDate=input("Joining Date(null if not older) : ")
    if Member_JoinDate=="null" or Member_JoinDate=='Null' or Member_JoinDate=='NULL':
        Member_JoinDate=date.today()
    str_memberadder="INSERT INTO MEMBER_MANAGER(Member_Name,Member_MobNo,Member_Add,Member_EmailId ,IdProof_Type,IdProof_No,Joining_Date) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    print("")
    Member_Data=(Member_Name,Member_MobNo,Member_Address,Member_EmailId,Member_IdPt,Member_IdP_No,Member_JoinDate)
    try:
        myCursor_newUser.execute(str_memberadder,Member_Data)
        Member_Id = myCursor_newUser.lastrowid
        mydb.commit()
        print("Member added succesfully")
        print(f"Member Id = {Member_Id}")
        print(f"Name : {Member_Name}")
        status=1
    except Exception as e:
        print("Error : Member not added")
        print(f"Error Statement- {e}")
    if status==1:
        print("\nNow create a password for Member Account")
        Member_Password=input("Password : ")
        try:
            str_pwadder="UPDATE MEMBER_MANAGER SET PASSWORD=%s WHERE Membership_No=%s"
            Password_addData=(Member_Password,Member_Id)
            myCursor_newUser.execute(str_pwadder,Password_addData)
            mydb.commit()
            print("\nPassword added succesfully")
        except:
            print("Error : Password not added")
            print(f"Error Statement- {e}")
        finally:
            print("\n")


def guest_chosen():
    print("\tGuest Mode")
    while True:
        search_type=input('''Choose the service-
            1. Seach Books by Name
            2. Search Books by Title
            3. Search Books by Author
            4. Back
            ''')
        try:
            search_type=int(search_type)
            if search_type==1:
                pass
            elif search_type==2:
                pass
            elif search_type==3:
                pass
            elif search_type==4:
                break
            else:
                print("\Wrong input! Enter an integer between 1 to 4")
        except:
            try:
                search_type=float(search_type)
                print("Wrong input! Enter an integer, not a decimal number")
            except:
                print("Wrong input! Numeric input expected")
        finally:
            print("\n")

def main():
    try:
        mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='nrupah'
        )
        with mydb.cursor() as mycursor:
            print("\t\t\tWelcome to Library Management System\n")
            while True:
                try:
                    mode=start_msg()
                    if mode==1:
                        admin_chosen(mycursor, mydb)
                    elif mode==2:
                        print("True")
                    elif mode==3:
                        print("True")
                    elif mode==4:
                        newUser_chosen(mycursor, mydb)
                    elif mode==5:
                        break
                except Exception as e:
                    print(f"Error in Execution of the Program- {e}")
                finally:
                    print("")
                    if mode == 5:  # Show the "Thanks for using!!!" message only if the user selected "Exit".
                        print("Thanks for using !!!")
    except Exception as e:
        print(f"Error in connection to server - {e}")

if __name__ == '__main__':
    main()



