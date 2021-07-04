from database import *
#Clients don't log into the system, so no class for a client.
#An advisor, a system admin or a super admin, can log into the system, so we use classes for them.



class Advisor():
    def __init__(self,un,pw):
        Username = un
        Password = pw

    def changePassword(self):
        userInput = ''
        while userInput == '': 
            userInput = input("Enter your current password or enter 'x' to exit")
            if userInput == 'x':
                return

            correctPassword = authenticatePassword(userInput)
            if correctPassword:
                newPass        = input("Enter the new password")
                confirmNewPass = input("Enter the new password again for confirmation")
                if newPass == confirmNewPass:
                    updatePassword(self,newPass)
                    print("Password has been succesfully updated!")
                    return
                else:
                    print("Passwords dont match")
                    userInput = ''

    def addClient():
        registerClient()

    def modClient():
        clientId = input("Enter the id of the client that you want to update\n\
        Or\n\
        Enter 'list' to show the list of all clients and their info\n\
        Or\n\
        Enter 'x' to exit\n\n")

        if clientId == 'x':
            return
        elif clientId == 'list':
            allClients = showAllClients()
            print(getColumns("clients"))
            for client in allClients:
                print(client + "\n")
        
        print("\n"*5)
        clientId = input("Enter the id of the client that you want to update: ")
        clientInfo = getClientInfo(clientId)
        if clientInfo == []:
            print("Client doesn't exist")
        else:
            print(clientInfo)





#System admin class : Advisor

#Super admin class : System admin

class SuperAdmin():
    def __init__(self):
        Username = "superadmin"
        Password = "Admin!23"