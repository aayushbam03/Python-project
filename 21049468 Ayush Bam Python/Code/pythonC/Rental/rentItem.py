from datetime import datetime
import sys
from Rental.rentConfig import STORE_STOCK
from Rental.returnItem import parse_invoice, readInvoice


class OutOfStockException(Exception):
    ...


def read_stocks()->dict:
    stock={}
    try:
        file = open(STORE_STOCK, "r")
    except FileNotFoundError as e:
        print(e)
        return {}
    for i in file.read().strip().split("\n"):
        stocks = i.strip().split(",")
        stock[stocks[0].strip()] = [x.strip() for x in stocks[1:]]
    file.close()
    return stock


def rentItems(customerName, userOrder,noOfDays,amountPaid=0):
    stock=read_stocks()
    invioceId=datetime.timestamp(datetime.now())
    if stock == {}:
        print("No Stock found")
        sys.exit()
    totalPrice = 0
    [totalPrice:=totalPrice+int(stock[str(i[0])][1].split("$")[1])*i[1] for i in userOrder]
    while True:
        try:
            amountPaid=int(input("Total is %s enter the advance amount you want to pay ! "%(totalPrice*noOfDays)))
            if amountPaid <0 :
                print("Advance can not be less than 0")
            if amountPaid > (totalPrice*noOfDays):
                print("You cannot pay more than %s"%(totalPrice*noOfDays))
                continue
            break
        except:
            print("Invalid price please try again")
            continue
    fileName = "./invoice/"+str(invioceId).split(".")[0]+".txt"
    file = open(fileName, "w")
    file.write("Customer Name: %s \n" % (customerName))
    file.write("Invoice Id: %s \n" % (int(invioceId)))
    file.write("Rented Date: %s \n" %
               (datetime.fromtimestamp(invioceId)).strftime("%Y/%m/%d %H-%M-%S"))
    file.write("Return Date: %s \n" %
               (datetime.fromtimestamp(invioceId+noOfDays*24*60*60)).strftime("%Y/%m/%d %H-%M-%S"))
    file.write("Total Amount: $%s \n" % (totalPrice*noOfDays))
    file.write("Paid: %s \n"%amountPaid)
    file.write("Returned: %s \n"%"false")
    file.write("\n\n\n\n\n")
    for i in userOrder:
        bookid = str(i[0])
        file.write(bookid+", "+", ".join(stock[bookid][:-1]) + f", {i[1]} \n")
    file.close()
    return str(invioceId).split(".")[0]

def updateStore(stock:dict):
    try:
        file = open(STORE_STOCK, "w")
    except Exception as e:
        print("No stock file found exiting the program")
        sys.exit()
    for i in stock.keys():
        file.write(
            ", ".join(str(x) for x in [i, stock[i][0], stock[i][1], stock[i][2]])+"\n")
    file.close()


def rent_item():
    customerName=""
    customerChoice=[]
    stock=read_stocks()
    while True:
        print("-"*60+"\n")
        print("SN"+" "*10+"Name"+" "*25+"Price"+" "*12+"Qunatity"+" "*10)
        for key,value in stock.items():
            print(key+" "*10+str(value[0])+" "*(30-len(str(value[0])))+str(value[1])+" "*(20-len(str(value[1])))+str(value[2]))
        print("-"*60+"\n")
        while True:
            try:
                id=int(input("\nEnter your choice: "))
                if int(stock[str(id)][2])<1:
                    print("No stock available ")
                    continue
                while True:
                    quantity=int(input("\nEnter the quantity: "))
                    if quantity < 1:
                        print("Quantity must be mre than 0")
                    if quantity > int(stock[str(id)][2]):
                        print("Product less in stock compared to stock in store")
                        continue
                    break
                stock[str(id)]
                customerChoice.append([id,quantity])
                stock[str(id)][2]=int(stock[str(id)][2])-quantity
                break
            except ValueError:
                print("Invalid input try again")
                continue
            except KeyError:
                print("Item corresponding to user input not found please try again")
                continue
        if not customerName:
            customerName=input("\nEnter your Name: ")
            while True:
                try:
                    noOfDays=int(input("\nEnter number of day you want to rent: "))
                    if noOfDays >30:
                        print("Can rent for 30 days only")
                        continue
                    if noOfDays < 1:
                        noOfDays=2
                        print("Default is set to 2 day\n")
                    break
                except:
                    print("Invalid input")
                    continue
        if input("Press y to rent another item again !").lower()=="y": continue
        break
    invoiceId=rentItems(customerName,customerChoice,noOfDays)
    updateStore(stock)
    parse_invoice(readInvoice(invoiceId))