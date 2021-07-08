from database import *
#Clients don't log into the system, so no class for a client.
#An advisor, a system admin or a super admin, can log into the system, so we use classes for them.



class Advisor():
    def __init__(self, userInfo):
        self.Info = userInfo
        self.Username = userInfo[0][1]
        self.Login_Type = "1"

    def showMenu(self):
        action = ''
        while action != 'x':
            self.menuOptions()
            print("Enter x to log out") 
            action = input("\nAction: ")
            self.menuActions(action,self.Info,self.Login_Type)

    @staticmethod
    def menuOptions():
        print("\n\nMenu | Choose an action\n" + "="*50)
        print("Enter 1 to update your password ")
        print("Enter 2 to add a new client ")
        print("Enter 3 to modify info of a client ")
        print("Enter 4 to search and retrieve info of a client")

    @staticmethod
    def menuActions(action,userInfo,logintypeArg):
        if action == "1":
            changePassword(userInfo[0][1],logintypeArg)
        if action == "2":
            registerClient()    
        if action == "3":
            modRecord("client")
        if action == "4":
            searchRecord('client')
        if action == "x":
            return False

    

    

class SystemAdmin(Advisor):
    def __init__(self, userInfo):
        super(SystemAdmin, self).__init__(userInfo)
        self.Login_Type = '2'

    @staticmethod
    def menuOptions():
        Advisor.menuOptions()
        print("Enter 5 to delete a client ")
        print("Enter 6 to check the list of users and their roles ")
        print("Enter 7 to add an advisor ")
        print("Enter 8 to modify the info of an advisor ")
        print("Enter 9 to delete an advisor")
        print("Enter 10 to reset an advisor's password (temporary password)")
        print("Enter 11 to make a backup of the system")
        print("Enter 12 to see the logs")

    @staticmethod
    def menuActions(action,userInfo,logintypeArg):
        Advisor.menuActions(action, userInfo, logintypeArg)
        if action == "5":
            deleteRecord('client')
        if action == "6":
            listAllUsers()
        if action == "7":
            registerAdvisor()
        if action == "8":
            modRecord("advisor")
        if action == "9":
            deleteRecord('advisor')
        if action == "10":
            resetPassword("1")
        if action == "11":
            print("x")
        if action == "12":
            show_log()

    
        


    def listUsers():
        print("users")

    

#System admin class : Advisor

#Super admin class : System admin

class SuperAdmin(SystemAdmin):
    def __init__(self):
        self.Username = "superadmin"
        self.Password = "Admin!23"
        self.Login_Type = '3'

    def showMenu(self):
        action = ''
        while action != 'x':
            unread_sus = checkForSus()
            print("\n" * 30)
            print("\n\nMenu | Choose an action\n" + "="*50)
            self.menuOptions()
            
            if unread_sus != 0:
                if unread_sus == 1:
                    print(f"\nThere is {unread_sus} suspicious activity logged.")
                else:
                    print(f"\nThere are {unread_sus} suspicious activities logged.")
                print("Enter 'sus' to read them\n")

            print("Enter 'x' to log out") 
            action = input("\nAction: ")
            self.menuActions(action,self.Username,self.Login_Type)

    

    def menuOptions(self):
        print("Enter 1 to add a new client ")
        print("Enter 2 to modify info of a client ")
        print("Enter 3 to search and retrieve info of a client")
        print("Enter 4 to delete a client ")
        print("Enter 5 to check the list of users and their roles ")
        print("Enter 6 to add an advisor ")
        print("Enter 7 to modify the info of an advisor ")
        print("Enter 8 to delete an advisor")
        print("Enter 9 to reset an advisor's password (temporary password)")
        print("Enter 10 to make a backup of the system")
        print("Enter 11 to see the logs")
        print("Enter 12 to add system admin")
        print("Enter 13 to mod a system admin")
        print("Enter 14 to delete a system admin")
        print("Enter 15 to reset a system admin's password (temporary password)")
        print("Enter 16 to empty a table")
        print("Enter 17 to drop a table")
       
    
    def menuActions(self,action,un,logintypeArg):
        if action == "1":
            registerClient()    
        if action == "2":
            modRecord('client')
        if action == "3":
            searchRecord('client')
        if action == "4":
            deleteRecord('client')
        if action == "5":
            listAllUsers()
        if action == "6":
            registerAdvisor()
        if action == "7":
            modRecord('advisor')
        if action == "8":
            deleteRecord('advisor')
        if action == "9":
            print("x")
        if action == "10":
            print("x") 
        if action == "11":
            show_log()
        if action == "12":
            registerSystemAdmin()
        if action == "13":
            modRecord("system admin")
        if action == "14":
            deleteRecord("system admin")
        if action == "15":
            resetPassword("2")
        if action == "16":
            empty_table()
        if action == "17":
            drop_table()
        if action == 'sus':
            showSus()
            
        if action == "x":
            return False
            