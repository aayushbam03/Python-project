from Rental import rent_item
from Rental import returnItems
from Rental import parse_invoice

def return_item():
    filename=input("Enter the invoice id: ").strip()
    fileItem=returnItems(filename)
    if fileItem==None:
        return
    if fileItem=="not paid":
        print("Invoice not paid")
    if type(fileItem)==str:
        print("*"*10+"Error"+"*"*10)
        print(fileItem)
        return
    parse_invoice(fileItem)

def interact():
    while True:
        print("\n")
        print("-"*25+"Welcome to Store"+"-"*25)
        print("Press 1 to rent item")
        print("Press 2 to return item")
        print("Press 3 to exit store")
        userInput=0
        while True:
            try:
                userInput=int(input("\nEnter your choice:"))
                break
            except:
                print("Choose from 1-3")
                continue
        if userInput==1:
            rent_item()
        if userInput==2:
            return_item()
        if userInput==3:
            break

    print("Thanks come again!")
        

def main():
    interact()
