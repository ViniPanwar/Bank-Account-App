import csv
import pandas as pd #Execute pip install pandas at command line
from tabulate import tabulate #Execute pip install tabulate at command line
import os

def main():     # main function
    val = get_data()
    actions = ["1", "2", "3", "4", "5"] #Initialize valid entires
    retry = 3
    actionNotComplete =True
    while ((actionNotComplete) and (retry >= 1)):
        if val in actions:     # If input provided is valid
            if(val == "1"):
                createNewAccount()
            elif (val == "2"):
                creditDebitAccount()
            elif (val == "3"):
                listAccount()
            elif (val == "4"):
                accountHistory()
            else:
                print ("\nTHANK YOU!")
            actionNotComplete = False
        else:                  # If input in not valid
            print("\n\'Invalid Input\'")
            print("Please try again!\n")
            val = get_data()
            retry = retry - 1
        # User provided invalid enties more than three times
        if (retry <= 0):
            print("\nInput not recognized. Please come back later!")
# End Main()

def get_data(val = None):       #Get input from User
    print ("\nBank Account Application\n")
    print ("1 - Create New Account")
    print ("2 - Credit/Debit an Account")
    print ("3 - List all Accounts")
    print ("4 - List Account History")
    print ("5 - Exit\n")
    val = input ("What would you like to do? ")
    return val          #return the input provided to main()
# End Function get_data()

def createNewAccount():
    accId = 0
    if os.path.isfile(filename): #Check if file already exists
        with open(filename, 'r') as readFile:
            for line in readFile.readlines():
                col = line.split(',')
                if(col[0] == "Account_ID"):
                    accId = 0
                else:
                    for index,value in enumerate(col):
                        if (index == 0):
                            accId = value
        readFile.close()
        accId = int(accId) + 1
    else: #Create new file if file not found
        # File with Account Information
        with open(filename,'w', newline='') as writeFile:
            header =['Account_ID','First_Name','Last_Name','Balance']
            writer = csv.writer(writeFile,quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)
            accId = 1
        writeFile.close()
        # File with all transaction information
        with open(trn_filename,'w', newline='') as writeTrnFile:
            header1 = ['Account_ID','First_Name','Last_Name','Transaction','Balance']
            writer = csv.writer(writeTrnFile,quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header1)
        writeTrnFile.close()

    print("\n Creating new Account...")
    firstName = input("Enter First Name: ")
    lastName = input("Enter Last Name: ")
    balance = input("Enter Initial Balance: ")
    newAcc = [accId, firstName, lastName, balance]
    try:
        with open (filename, 'a', newline = '') as appendFile:
            writer = csv.writer(appendFile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(newAcc)
    finally:
        appendFile.close()
    transaction = 'Initial Balance'
    trnHistory = [accId, firstName, lastName, transaction, balance]
    try:
        with open (trn_filename, 'a', newline = '') as appendtrnFile:
            writer = csv.writer(appendtrnFile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(trnHistory)
    finally:
        appendtrnFile.close()
    print("\nNew Account Created for {} {}.".format(firstName, lastName))
    main()
# End Function createNewAccount()



def creditDebitAccount():
    #Exception Handling for Integer value
    while True:
        try:
            accId = int(input ("\nEnter Account Id: "))
            break
        except ValueError:
            print("Invalid Entry! Enter a numeric Value.")
    #Exception HAndling for Integer Value
    while True:
        try:
            amt = int(input ("Enter the Amount: "))
            break
        except ValueError:
            print("Invalid Amount. Enter a numeric Value.")

    trans = input ("Enter \t C - Credit \t D - Debit:\t")
    newBalance = None

    fields = ['Account_ID','First_Name', 'Last_Name', 'Balance']
    df = pd.read_csv(filename, usecols=fields)
    accounts=[]
    accounts = df['Account_ID'].tolist()

    trnHistory = [] # List for storing transaction history

    if accId in accounts: #Check if Account exists
        oldBalance = df.loc[df["Account_ID"] == accId, "Balance"]
        firstName = df[df.Account_ID == accId].First_Name.item()
        lastName = df[df.Account_ID == accId].Last_Name.item()
        if trans in ['C', 'c']: # Perform Credit
            transaction = 'Credit'
            print("\nCrediting Account....")
            newBalance = int(oldBalance) + amt
            df.loc[df["Account_ID"] == accId, "Balance"] = newBalance
            df.to_csv(filename, index = False)

            print("\n Amount ${} credited for {} ".format(amt, firstName))
            trnHistory = [accId, firstName, lastName, transaction, amt]
            try:
                with open (trn_filename, 'a', newline = '') as appendFile:
                    writer = csv.writer(appendFile, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(trnHistory)
            finally:
                appendFile.close()
        elif trans in ['D', 'd']: # Perform Debit
            if (int(oldBalance) >= amt): #Check if Amount enter is less than balance
                transaction = 'Debit'
                print("\n Debiting Account....")
                newBalance = int(oldBalance) - amt
                df.loc[df["Account_ID"] == accId, "Balance"] = newBalance
                df.to_csv(filename, index = False)
                print("\n Amount ${} debitted for {}".format(amt, firstName))
                trnHistory = [accId, firstName, lastName, transaction, amt]
                try:
                    with open (trn_filename, 'a', newline = '') as appendFile:
                        writer = csv.writer(appendFile, quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(trnHistory)
                finally:
                    appendFile.close()
            else:
                print("\n Not Enough Balance")

        else:
            print("\n Invalid Input. Try Again!")
            creditDebitAccount()

    else:
        print("\n Account does not Exist. Try Again!\n")

    main()
# End Function creditDebitAccount()


def listAccount():
    if (os.path.isfile(filename)):
        with open(filename, 'r') as readFile:
            reader = csv.reader(readFile)
            headers = next(reader)
            # print data in tabular form
            print (tabulate([(line[0], line[1] + " " + line[2], line[3]) for line in reader], headers = (headers[0], "Name", headers[3])))
        readFile.close()
    else:
        "File does not Exist."
    main()
# End Function listAccount()

def accountHistory():
    if(os.path.isfile("transactionInfo.tsv")):
        while True:
            try:
                accId = int(input ("\nEnter Account Id: "))
                break
            except ValueError:
                print("Invalid Entry! Enter a numeric Value.")
        finalBalance = 0
        firstName = ""
        lastName = ""
        fields = ['Account_ID','First_Name', 'Last_Name', 'Balance']
        df = pd.read_csv(trn_filename, usecols=fields)
        accounts=[]
        accounts = df['Account_ID'].tolist()
        if accId in accounts: #Check if account exists.

            with open(trn_filename, 'r') as readtrnFile:
                with open ('temp.csv','w', newline='') as temp:
                    reader = csv.reader(readtrnFile)
                    headers = next(reader)
                    writer = csv.writer(temp, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(headers)
                    for line in readtrnFile.readlines():
                        col = line.split(',')

                        if (col[0] == str(accId)):
                            firstName = col[1]
                            lastName = col[2]
                            if (col[3] == 'Initial Balance'):
                                 finalBalance = int(col[4])
                            if (col[3] == 'Credit'):
                                finalBalance += int(col[4])
                            if (col[3] == 'Debit'):
                                finalBalance -= int(col[4])
                            tempRecord = [col[0],col[1],col[2],col[3],col[4].strip()]
                            writer.writerow(tempRecord)
                temp.close()
            readtrnFile.close()
            with open ('temp.csv','r') as readTempFile:
                reader1 = csv.reader(readTempFile)
                headers = next(reader1)
                # print data in tabular form

                print (tabulate([(line[0], line[1] + " " + line[2], line[3], line[4]) for line in reader1], headers = (headers[0], "Name", headers[3], headers[4])))
                print("\n Current Balance for {} {} is {}".format(firstName,lastName,finalBalance))

            readTempFile.close()
            os.remove('temp.csv')

        else: #Account provided does not exist
            print("\n Account does not Exist.")
    else:
        print("File does not exist.")
# End Function accountHistory()

filename = "bankAccountInfo.csv"
trn_filename = "transactionInfo.csv"

main()
