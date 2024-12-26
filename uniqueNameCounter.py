# DB- https://github.com/brianary/Lingua-EN-Nickname/tree/main

# Create Dictionary
from functools import lru_cache

# Define the global threshold for name similarity
NAME_SIMILARITY_THRESHOLD = 3

NickNames = {}

def uploadDB():
    """
    This function loads the nickname database from a text file and updates the NickNames dictionary.
    Each line in the file contains a main name and its aliases separated by spaces.
    The aliases are casefolded and stored as sets (sets of nicknames).
    """
    with open('nicknames_.txt', 'r') as file:
        for line in file:
            
            parts = line.split()
            nameKey = parts[0].casefold()
            aliases = {aliase.casefold() for aliase in parts[1:]}

            NickNames[nameKey] = aliases
    
# Call the function once
uploadDB()

def hammingDistance(firstName: str, secondName: str) -> int: 
    """
    Calculate the Hamming distance between two strings of the same length.
    The Hamming distance is the number of positions at which the corresponding 
    characters are different between two strings.

    Parameters:
    firstName (str): The first string.
    secondName (str): The second string.

    Returns:
    int: The Hamming distance between the two strings, or -1 if the strings have different lengths.
    """

    if len(firstName) != len(secondName):
        return -1
    return sum(firstName[i] != secondName[i] for i in range(len(firstName)))

def normalizeNameDB(name: str) -> set:
    """
    This function searches for the name in the NickNames dictionary and returns all matching names, including aliases.
    If no match is found, it returns the name itself.

    Parameters:
    name (str): The name to search for its aliases.
    
    Returns:
    set: A set of matching names/aliases, or a set containing the name itself.
    """
    matchedNames = set()

    for nameKey, aliases in NickNames.items():
        if name == nameKey or name in aliases:
            matchedNames.add(nameKey)

    if not matchedNames:
        matchedNames.add(name)

    return matchedNames

def LevenshteinDistance(str1: str, str2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    The Levenshtein distance is the minimum number of single-character edits (insertions, deletions, or substitutions) 
    required to change one string into the other.

    Parameters:
    str1 (str): The first string.
    str2 (str): The second string.

    Returns:
    int: The Levenshtein distance between the two strings.
    """
        
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

# Check if two names are similar using Levenshtein distance
def levenshteinSimilar(firstName: str, secondName: str) -> bool:
    """
    This function checks if two names are similar based on Levenshtein distance.
    The names are considered similar if the Levenshtein distance between them is 
    within a defined threshold, based on the length of the names.

    Parameters:
    firstName (str): The first name.
    secondName (str): The second name.

    Returns:
    bool: True if the names are similar based on the Levenshtein distance, otherwise False.
    """
    distance = LevenshteinDistance(firstName, secondName)
    max_length = max(len(firstName), len(secondName)) 
    return distance <= max_length / NAME_SIMILARITY_THRESHOLD

# Levenshtein similarity with nicknames
@lru_cache(maxsize= 128)
def levenshteinWithAliases(firstName: str, secondName: str):
    """
    This function checks if two names or their aliases are similar using Levenshtein distance.
    It first checks if the two names are directly similar. If not, it checks if any alias
    of either name matches the other name using Levenshtein distance.

    Parameters:
    firstName (str): The first name.
    secondName (str): The second name.

    Returns:
    bool: True if the names or their aliases are similar based on the Levenshtein distance, otherwise False.
    """
    # Levenshtein check between the first name and the second name
    if levenshteinSimilar(firstName, secondName):
        return True
    
    keyNameFirst = normalizeNameDB(firstName)
    keyNameSecond = normalizeNameDB(secondName)
    # For each alias of the first name, check if it matches the second name using Levenshtein
    for name in keyNameFirst:
        for alies in NickNames.get(name, []):
            if levenshteinSimilar(alies, secondName):
                return True

    # For each alias of the second name, check if it matches the first name using Levenshtein
    for name in keyNameSecond:
        for alies in NickNames.get(name, []):
            if levenshteinSimilar(alies, firstName):
                return True

    return False

def checkWordSimilarity(firstName: str, secondName: str) -> bool:
    """ 
    This function checks if two names are similar by comparing them using multiple methods.
    It checks if the names are equivalent, or if they are similar by their distance (e.g., using Hamming or Levenshtein distance).

    Parameters:
    firstName (str): The first name to compare.
    secondName (str): The second name to compare.

    Returns:
    bool: True if the names are equivalent or similar, otherwise False.
    """
    if NamesEquivalent(firstName, secondName):
        return True
    
    if compareNamesByDistance(firstName, secondName):
        return True
    
    return False

def NamesEquivalent(firstName: str, secondName: str) -> bool:
    """
    This function checks if two names are equivalent, either exactly or based on their aliases.
    It compares both the names and their possible aliases from the database.

    Parameters:
    firstName (str): The first name to compare.
    secondName (str): The second name to compare.

    Returns:
    bool: True if the names are equivalent, otherwise False.
    """
    if firstName == secondName:
        return True
    
    firstNameMatches = normalizeNameDB(firstName)
    secondNameMatches = normalizeNameDB(secondName)

    if firstNameMatches & secondNameMatches:
        return True
    
    return False

def compareNamesByDistance(firstName: str, secondName: str) -> bool:
    """
    This function compares two names using distance-based methods, such as Hamming and Levenshtein.

    Parameters:
    firstName (str): The first name to compare.
    secondName (str): The second name to compare.

    Returns:
    bool: True if the names are similar based on distance, otherwise False.
    """
    hammingDist = hammingDistance(firstName, secondName)

    if  hammingDist > -1 and  hammingDist <= (len(firstName) / NAME_SIMILARITY_THRESHOLD):
        return True
    
    if levenshteinWithAliases(firstName, secondName):
        return True

    return False

# Check similarity between first and middle names
def checkSimilarity(firstName, secondName) -> bool:
    """
    This function checks if two names (or lists of names) are similar by comparing each part of the names.
    It first checks for an exact match, then compares each component if the names are passed as lists of names.

    Parameters:
    firstName (str or list): The first name or a list of first names.
    secondName (str or list): The second name or a list of second names.

    Returns:
    bool: True if the names are identical or similar, otherwise False.
    """
        
    if firstName == secondName:
        return True
    
    if isinstance(firstName, str):
        firstName = [firstName]  
    
    if isinstance(secondName, str):
        secondName = [secondName]

    if (len(firstName) >= len(secondName)):
        min = secondName
        other = firstName
    else:
        min = firstName
        other = secondName

    for i in range(len(min)):
        if not(checkWordSimilarity(min[i],other[i])):
            return False
    
    return True

def countUniqueNames(billFirstName: str, billLastName: str, shipFirstName: str, 
                     shipLastName: str, billNameOnCard: str) -> int:
    """
    This function calculates the number of unique names involved in a transaction
    by comparing the billing and shipping names with the name on the card. If any 
    of the names match, the count is decreased.

    Parameters:
    billFirstName (str): First name on the bill, which may include a middle name.
    billLastName (str): Last name on the bill.
    shipFirstName (str): First name on the shipping address, which may include a middle name.
    shipLastName (str): Last name on the shipping address.
    billNameOnCard (str): Name printed on the card used for the transaction.

    Returns:
    int: The number of unique names involved in the transaction. The result is at least 1.
    """

    # Validate that all inputs are non-empty strings
    if not all(isinstance(arg, str) and arg.strip() != "" for arg in [billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard]):
        raise ValueError("All inputs must be non-empty strings.")

    # Maximum number of people per transaction.
    uniqueNames = 3
   
    # Convert everything to lowercase for case-insensitive comparison
    billFirstNames = billFirstName.casefold().split()
    shipFirstNames = shipFirstName.casefold().split()
    billingLastName = billLastName.casefold()
    shippingLastName = shipLastName.casefold()
    BillCardName = billNameOnCard.casefold().split()

    # Check billing and shipping name are equal
    if checkSimilarity(billingLastName, shippingLastName) and checkSimilarity(billFirstNames, shipFirstNames):
            uniqueNames -= 1
    
    # check if bill name matches the name on card:

    # First case: Check if bill last name matches the first entry in the card's name
    #  And if the bill's first name matches the remaining part of the card's name
    if checkSimilarity(billingLastName, BillCardName[0]) and checkSimilarity(billFirstNames, BillCardName[1:]):
            uniqueNames -= 1

    # Second case: Check if bill last name matches the last entry in the card's name
    # And if the bill's first name matches the remaining part of the card's name
    elif checkSimilarity(billingLastName, BillCardName[-1]) and checkSimilarity(billFirstNames, BillCardName[:-1]):
            uniqueNames -= 1

    # Check if shipping name matches the name on the card:

    # First case: Check if ship last name matches the first entry in the card's name
    #  And if the ship's first name matches the remaining part of the card's name
    if checkSimilarity(shippingLastName, BillCardName[0]) and checkSimilarity(shipFirstNames, BillCardName[1:]):
            uniqueNames -= 1
      
    # Second case: Check if ship last name matches the last entry in the card's name
    # And if the ship's first name matches the remaining part of the card's name
    elif checkSimilarity(shippingLastName, BillCardName[-1]) and checkSimilarity(shipFirstNames, BillCardName[:-1]):
            uniqueNames -= 1

    return uniqueNames if uniqueNames > 1 else 1


print(countUniqueNames("Deborah hila", "Egli", "Deborah hila ex", "Egli", "Deborah Egli"))  # 1
print(countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"))  # 1
print(countUniqueNames("Deborah", "Egli", "Egni", "Egli", "Deborah Egli"))  # 2
print(countUniqueNames("Deborah S", "Egpi", "Deborah", "Egli", "Egli Deborah"))  # 1
print(countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli"))  # 2



# def test_identical_names():
#     result = countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
#     assert result == 1, f"Expected 1, but got {result}"

# def test_hamming_distance():
#     result = countUniqueNames("Deborph", "Eglo", "Deborah", "Egli", "Deborah Egli")
#     assert result == 1, f"Expected 1, but got {result}"

# def test_LevenshteinDistanceance():
#     result = countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")
#     assert result == 1, f"Expected 1, but got {result}"

# def test_name_with_different_case():
#     result = countUniqueNames("deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
#     assert result == 1, f"Expected 1, but got {result}"

# def test_different_names():
#     result = countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli")
#     assert result == 2, f"Expected 2, but got {result}"

# def tests():
#     test_identical_names()
#     test_hamming_distance()
#     test_LevenshteinDistanceance()
#     test_name_with_different_case()
#     test_different_names()
#     print("succ")

# tests()