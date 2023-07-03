import data.json.json_utils as json_utils

def create_ledger(name,address,gst,phone,file):
    try:
        data=json_utils.read_json(file)
        print(data)
        if name in data.keys():
            return False
        data[name]={
            "sno":len(data),
            "address":address,
            "gst":gst,
            "phone":phone,
            "purchase":0,
            "paid":0,
            "balance":0
        }
        json_utils.write_json(file,data)
        return True
    except:
        return False

def make_payment(file,company,payment):
    data=json_utils.read_json(file)
    data[company]["paid"]= data[company]["paid"]+payment
    data[company]["balance"]=data[company]["purchase"]-data[company]["paid"]
    data["summary"]["paid"]=data["summary"]["paid"]+payment
    print(data["summary"]["purchase"] -data["summary"]["paid"])
    data["summary"]["balance"]= data["summary"]["purchase"] -data["summary"]["paid"]
    json_utils.write_json(file,data)


