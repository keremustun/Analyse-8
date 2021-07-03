from register import registerClient
#Clients don't log into the system, so no class for a client.
#An advisor, a system admin or a super admin, can log into the system, so we use classes for them.
class Advisor():
    def __init__(self):
        Username = ""
        Password = ""

    def changePassword(self):
        userInput = ''
        while userInput == '': 
            userInput = input("Enter your current password or enter 'x' to exit")
            if userInput == 'x':
                break

            correctPassword = authenticatePassword(userInput)
            if correctPassword:
                newPass        = input("Enter the new password")
                confirmNewPass = input("Enter the new password again for confirmation")
                if newPass == confirmNewPass:
                    updatePassword(self,newPass)
                    print("Password has been succesfully updated!")
                    break
                else:
                    print("Passwords dont match")
                    userInput = ''

    def addClient():
        registerClient()


#System admin class : Advisor

#Super admin class : System admin

class SuperAdmin():
    def __init__(self):
        Username = "superadmin"
        Password = "Admin!23"