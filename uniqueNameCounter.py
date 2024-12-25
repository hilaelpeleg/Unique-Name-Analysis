# DB- https://github.com/brianary/Lingua-EN-Nickname/tree/main

# Create Dictionary
NickNames = {}

def uploadDB():
    # Start with upload the DB nicknames
    with open('nicknames.txt', 'r') as file:
        for line in file:
            
            parts = line.split()
            name_key = parts[0].lower()
            aliases = [aliase.lower() for aliase in parts[1:]]

            NickNames[name_key] = aliases
    
# Call the function once
uploadDB()

def hammingDistance(firstName, secondName):  
    if len(firstName) != len(secondName):
        return -1
    return sum(firstName[i] != secondName[i] for i in range(len(firstName)))

def normalizeNameDB(name):
    for name_key, aliases in NickNames.items():
        if name in aliases or name == name_key:
            return name_key
    return name

def levenshtein_dist(str1, str2):
    n = len(str1)
    m = len(str2)

    matrix=[[0] * (m+1) for _ in range(n+1)]

    for i in range(n + 1):
        matrix[i][0] = i

    for j in range(m + 1):
        matrix[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            case1 = matrix[i-1][j-1] + (str1[i -1] != str2[j -1])
            case2 = matrix[i][j-1] + 1
            case3 = matrix[i-1][j] + 1
            matrix[i][j] = min(case1, case2, case3)
       
    return matrix[n][m]

def levenshtein_similar(firstName, secondName):
    distance = levenshtein_dist(firstName, secondName)
    max_length = max(len(firstName), len(secondName)) 
    return distance <= max_length / 3

def levenshtein_similar_to_nicknames(firstName, secondName):
    # Levenshtein check between the first name and the second name
    if levenshtein_similar(firstName, secondName):
        return True
    
    key_name_first = normalizeNameDB(firstName)
    key_name_second = normalizeNameDB(secondName)

    # For each alias of the first name, check if it matches the second name using Levenshtein
    for alies in NickNames.get(key_name_first, []):
        if levenshtein_similar(alies, secondName):
            return True

    # For each alias of the second name, check if it matches the first name using Levenshtein
    for alies in NickNames.get(key_name_second, []):
        if levenshtein_similar(alies, firstName):
            return True

    return False

# Check if the firstname in the DB, then check if shipName is == or with types or nickname to shipname
def checkNameeSimillar(firstName, secondName):
    if firstName == secondName:
        return True
    
    if normalizeNameDB(firstName) == normalizeNameDB(secondName):
        return True
      
    if levenshtein_similar_to_nicknames(firstName, secondName):
        return True
    
    return False

def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    # Maximum number of people per transaction.
    uniqueNames = 3
    
    # First, we want to handle the case sensitivity, so we will transform everything to lowercase letters.
    # bill and ship first name could include middle names
    bill_first_name = billFirstName.lower().split()
    ship_first_name = shipFirstName.lower().split()
    bill_last_name = billLastName.lower()
    ship_last_name = shipLastName.lower()

    bill_name_on_card = billNameOnCard.lower().split()
    first_name_card = bill_name_on_card[0]
    last_name_card = bill_name_on_card[1]

    # Check billing and shipping name are equal
    if checkNameeSimillar(bill_first_name[0], ship_first_name[0]):
        if checkNameeSimillar(bill_last_name, ship_last_name):
            uniqueNames -= 1
    
    # check if bill name == name on card
    # Check if bill first name == first name on the card and bill last name == last name on the card
    if checkNameeSimillar(bill_first_name[0], first_name_card):
        if checkNameeSimillar(bill_last_name, last_name_card):
            uniqueNames -= 1

    # Check if bill last* name == first* name on the card and bill first* name == last* name on the card
    elif checkNameeSimillar(bill_last_name, first_name_card):
        if checkNameeSimillar(bill_first_name[0], last_name_card):
            uniqueNames -= 1

    # Check if ship name == name on card
    # Check if ship first name == first name on the card and ship last name == last name on the card
    if checkNameeSimillar(ship_first_name[0], first_name_card):
        if checkNameeSimillar(ship_last_name, last_name_card):
            uniqueNames -= 1
      
    # Check if ship last* name == first* name on the card and ship first* name == last* name on the card
    elif checkNameeSimillar(ship_last_name, first_name_card):
        if checkNameeSimillar(ship_first_name[0], last_name_card):
            uniqueNames -= 1

    if uniqueNames == 0:
        return 1
    
    return uniqueNames

def test_identical_names():
    result = countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
    assert result == 1, f"Expected 1, but got {result}"

def test_hamming_distance():
    result = countUniqueNames("Deborph", "Eglo", "Deborah", "Egli", "Deborah Egli")
    assert result == 1, f"Expected 1, but got {result}"

def test_levenshtein_distance():
    result = countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")
    assert result == 1, f"Expected 1, but got {result}"

def test_name_with_different_case():
    result = countUniqueNames("deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
    assert result == 1, f"Expected 1, but got {result}"

def test_different_names():
    result = countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli")
    assert result == 2, f"Expected 2, but got {result}"

def tests():
    test_identical_names()
    test_hamming_distance()
    test_levenshtein_distance()
    test_name_with_different_case()
    test_different_names()
    print("succ")

tests()