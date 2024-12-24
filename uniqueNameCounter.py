# DB- https://github.com/brianary/Lingua-EN-Nickname/tree/main

# Create Dictionary
NickNames = {}

def uploadDB():
    # Start with upload the DB nicknames
    with open('nicknames_.txt', 'r') as file:
        for line in file:
            # 
            parts = line.split()
            name_key = parts[0].lower()
            aliases = [aliase.lower() for aliase in parts[1:]]

            NickNames[name_key] = aliases
    # print(NickNames)

# Call the function once
uploadDB()

def hammingDistance(nameOne, nameTwo):  
    if len(nameOne) != len(nameTwo):
        return -1
    return sum(nameOne[i] != nameTwo[i] for i in range(len(nameOne)))

def normalizeNameDB(name):
    for name_key, aliases in NickNames.items():
        if name in aliases or name == name_key:
            return name_key
    return name

# Check if the firstname in the DB, then check if shipName is == or with types or nickname to shipname
def checkNameeSimillar(nameOne, nameTwo):
    if nameOne == nameTwo:
        return True
    
    if normalizeNameDB(nameOne) == normalizeNameDB(nameTwo):
        return True
    
    if hammingDistance(nameOne, nameTwo) > -1 and hammingDistance(nameOne, nameTwo) <= len(nameOne) / 4:
        return True
    
    return False

def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    #  First, we want to handle the case sensitivity, so we will transform everything to lowercase letters.
    bill_first_name = billFirstName.lower()
    ship_first_name = shipFirstName.lower()
    bill_last_name = billLastName.lower()
    ship_last_name = shipLastName.lower()

    # Check first name
    if checkNameeSimillar(bill_first_name, ship_first_name) and checkNameeSimillar(bill_last_name, ship_last_name):
        return 1

    return 2

# Check the basic exmp from forter:

# Check identical
print(countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli"), "identical")  # 1

# Check hammingdistance
print(countUniqueNames("Deborph", "Eglo", "Deborah", "Egli", "Deborah Egli"), "hammingdistance") # 1
print(countUniqueNames("Deforah", "Egli", "deborah", "Egli", "Deborah Egli"), "hammingdistance")  # 1

# Check upper lower case
print(countUniqueNames("deborah", "Egli", "Deborah", "Egli", "Deborah Egli"))  # 1
print(countUniqueNames("Deborah", "egli", "Deborah", "Egli", "Deborah Egli"))  # 1

# Check different name with same nickname ? 
print(countUniqueNames("Abigail", "Egli", "Abner", "Egli", "Deborah Egli"), "different name - same nickname")  # 1

# Doesn't work 
print(countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"))  # 1
print(countUniqueNames("Deborah", "Egli", "Egni", "Deborah", "Egli Deborah"))  # 1
print(countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah"))  # 1

# Work
print(countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli"))  # 2
