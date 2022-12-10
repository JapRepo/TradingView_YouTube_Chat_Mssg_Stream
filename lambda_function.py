import DatabaseConnect as dynamodb
import streamFunc as stream
import time
import decimal

def lambda_handler(event, context):
    if "body" in event:
        message = event["body"]
    else:
        message = event
        
    if isinstance(message, str):
        try:
            message = json.loads(message)
        except Exception as e:
            print(e) 
    elif isinstance(message, list):
        message = message[0]
    print(message)
    
    tradeSymbol     = message["Symbol"].upper()
    tradeSignalSide = message["Side"].capitalize()
    tradeQtyReq     = float_to_str(message["Qty"])
    tradePrice      = float(message["Price"])
    
    mssgLine1 = "****** "+tradeSymbol +" " + tradeSignalSide +" Trade ******* "
    mssgline2 = " Trade Symbol ---> "+ tradeSymbol +" " +" , " 
    mssgLine3 = " Trade Price  ---> "+ str(tradePrice)+" " + " , " 
    mssgLine4 = " Trade Qty    ---> "+ str(tradeQtyReq)+" " + " , "
    mssgLine5 = " Trade Type   ---> "+ tradeSignalSide+" " + " "
    mssgLine6 = " ************************************************* "
    
    client_id   = "xxxxxxxxxxx.apps.googleusercontent.com"
    tokenOld    = dynamodb.GetData(client_id)["Item"]
    #print(tokenOld)
    creds   = stream.Authenticate(tokenOld,client_id)
    resKeyStore = dynamodb.PutData(creds)
    mssg = mssgLine1 + mssgline2 + mssgLine3 + mssgLine4 +  mssgLine5 + mssgLine6
    print(mssg)
    returnWrite = stream.StreamChatWrite(creds ,mssg)
    
    return None

mssgLine1 = "*********Chart Symbols********* "
mssgline2 = " Blue Arrow ---> Long."
mssgLine3 = " Pink Arrow ---> Partial Close." 
mssgLine4 = " Yellow Arrow ---> Expecting PullBack."
mssgLine5 = ""
mssgLine6 = " ************************************************* "

ctx = decimal.Context()

# 20 digits should be enough for everyone :D
ctx.prec = 9

def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')



    