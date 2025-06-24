import math
import sys
import Rental.rentItem as rent
import datetime
from Rental.rentConfig import INVOICE_PATH


def readInvoice(invoiceName):
    '''
    Read Invoice and stores it in a dict
    '''
    invoiceDetail = {}
    invoiceDetail["items"] = {}
    try:
        file = open(INVOICE_PATH+invoiceName+".txt", "r")
    except:
        return {}
    invoiceLists = file.read().strip().split("\n\n\n\n\n")
    invoiceHead = invoiceLists[0]
    invoiceBody = invoiceLists[1]
    file.close()

    for i in invoiceHead.strip().split("\n"):
        invoice = i.strip().split(":")
        try:
            invoiceDetail[invoice[0].strip().replace(
                " ", "-").lower()] = int(invoice[1].strip())
        except:
            invoiceDetail[invoice[0].strip().replace(
                " ", "-").lower()] = invoice[1].strip()

    for i in invoiceBody.strip().split("\n"):
        invoice = i.strip().split(",")
        invoiceDetail["items"][invoice[0].strip()] = [x.strip() for x in invoice[1:]]
    return invoiceDetail

def parse_invoice(invoiceDetail):
    '''
        Parse the invoice dict in console 
    '''
    print("-"*60+"\n")
    print("-"*25+"Invoice for %s"%invoiceDetail["customer-name"]+"-"*25+"\n")

    for key,value in invoiceDetail.items():
        if type(value)==dict: continue
        print(key.replace("-"," ").capitalize()+": "+str(value)+"\n")
    print("SN"+" "*10+"Name"+" "*25+"Price"+" "*12+"Qunatity"+" "*10)
    for key,value in invoiceDetail["items"].items():
        print(key+" "*10+str(value[0])+" "*(30-len(str(value[0])))+str(value[1])+" "*(20-len(str(value[1])))+str(value[2]))
    print("-"*60+"\n")


def returnItems(filepath):
    '''
        Checks the items, check delay and gives total price to the user
    '''
    stock = rent.read_stocks()
    invoiceDetail = readInvoice(str(filepath))
    try:
        if (invoiceDetail["returned"]!="false"):
            return "Item already returned"
    except Exception as e:
        print(e)
    if invoiceDetail == {}:
        print("No invoice found of %s" % filepath)
        return
    returnDate = datetime.datetime.timestamp(datetime.datetime.strptime(
        invoiceDetail["return-date"], "%Y/%m/%d %H-%M-%S"))
    returnedDate = datetime.datetime.timestamp(datetime.datetime.now())
    difference = math.floor((returnedDate-returnDate)/(24*60*60))
    fine = 0

    if difference <= 0: fine = 0
    else: fine = difference*10

    invoiceDetail["returned-date"] = datetime.datetime.now().strftime("%Y/%m/%d %H-%M-%S")
    invoiceDetail["fine"] = fine
    amountToPay = (
        int(invoiceDetail["total-amount"].split("$")[1])-invoiceDetail["paid"])+fine
    parse_invoice(invoiceDetail)
    if fine != 0:
        print("There was %s day delay" % difference)
        print("Fine of %s will be added to your pending amount" % fine)
    print("User needs to pay $%s" % amountToPay)
    for i in invoiceDetail["items"].keys():
        stock[i][2] = int(stock[i][2])+int(invoiceDetail["items"][i][2])
    
    if (input("Set invoice to paied ?").lower()=="y"):
        rent.updateStore(stock)
        updateInvoice(str(filepath), invoiceDetail)
        return invoiceDetail
    return "not paid"


def updateInvoice(filename, invoiceDetail: dict):
    try:
        file = open(INVOICE_PATH+filename+".txt", "w")
    except:
        print("No stock file found exiting the program")
        sys.exit()
    invoiceDetail["paid"] = int(
        invoiceDetail["total-amount"].split("$")[1])+invoiceDetail["fine"]
    invoiceDetail["returned"]="true"
    for key, value in invoiceDetail.items():
        if type(value) == dict:
            continue
        file.write(key.replace("-", " ").capitalize()+": "+str(value)+"\n")

    file.write("\n\n\n\n\n")

    for i in invoiceDetail["items"].keys():
        file.write(
            ", ".join(str(x) for x in [i, invoiceDetail["items"][i][0], invoiceDetail["items"][i][1], invoiceDetail["items"][i][2]])+"\n")
    file.close()
    parse_invoice(invoiceDetail)