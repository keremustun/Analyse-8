from database import *
#Clients don't log into the system, so no class for a client.
#An advisor, a system admin or a super admin, can log into the system, so we use classes for them.



class Advisor():
    def __init__(self, userInfo):
        self.UserId =  userInfo[0][0]
        self.Username = userInfo[0][1]
        self.Password = userInfo[0][2]
        self.First_Name = userInfo[0][3]
        self.Last_Name = userInfo[0][4]
        self.Registered_Date = userInfo[0][5]
        self.Login_Type = "1"

    def showMenu(self):
        print("Enter 1 to update your password ")
        print("Enter 2 to add a new client ")
        print("Enter 3 to modify info of a client ")
        print("Enter 4 to search and retrieve info of a client")
        
        action = input("Action: ")

        if action == "1":
            self.changePassword()
        if action == "2":
            registerClient()    
        if action == "3":
            modClient()
        if action == "4":
            searchClient()


    def changePassword(self):
        userInput = ''
        strikes = 0
        while userInput == '': 
            userInput = input("Enter your current password or enter 'x' to exit:\n")
            if userInput == 'x':
                return

            correctPassword = authenticatePassword(userInput, self.Username, self.Login_Type)
            if correctPassword:
                newPass        = input("Enter the new password: ")
                confirmNewPass = input("Enter the new password again for confirmation: ")
                if newPass == confirmNewPass:
                    updatePassword(newPass, self.UserId, self.Login_Type)
                    print("Password has been succesfully updated!")
                    return
                else:
                    print("Passwords dont match")
                    userInput = ''
            else:
                strikes += 1
                if strikes == 3:
                    print("Incorrect password too many times. Logging out...")
                    quit()
                else:
                    print("Incorrect password. Please try again.")
                    userInput = ''

    





#System admin class : Advisor

#Super admin class : System admin

class SuperAdmin():
    def __init__(self):
        Username = "superadmin"
        Password = "Admin!23"