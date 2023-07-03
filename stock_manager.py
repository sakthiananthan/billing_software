import data.json.json_utils as json_utils

def update_stock():
    print("inside update stock")
    bill_data=json_utils.read_json("data/json/bill.json")
    stock_data=json_utils.read_json("data/json/stock.json")
    for item in bill_data["items"]:
        stock_item=item["stock_key"]
        count=item["Nos"]
        stock_data[stock_item]["item_stock"]=stock_data[stock_item]["item_stock"]-count
    json_utils.write_json("data/json/stock.json",stock_data)

                          
