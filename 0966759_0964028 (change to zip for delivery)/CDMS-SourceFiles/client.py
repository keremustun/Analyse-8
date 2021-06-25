cities = ["Rotterdam", "Amsterdam", "Den Haag", "Eindhoven","Maastricht","Delft","Breda","Haarlem","Utrecht","Leiden"]

def registerClient():
    name            = input("\n1. Enter the name of the new client: ")

    print(                  "\n2. Entering the address...")
    streetName      = input("2.1. Street name: ")
    zipCode         = input("2.2. Zipcode: ")
    print(                  "2.3. City: (Choose one from the list below) ")
    for city in cities:
        print("- " + city )
    
    city            = input("\nCity: ")



    email   = input("\n3. Email address: ")
    mobile  = input("\n4. Mobile: ")

    print("\n"+ "="*40)
    print("Client {} has been added to the database".format(name))