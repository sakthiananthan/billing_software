import data.json.json_utils as json_utils


def create_product(file,stock_file,prod_eng,prod_tam,pc_1,pc_rt,pc_ct,box_pr,box_ct,tag,comp,mrp):
    data=json_utils.read_json(file)
    if tag=="":
        tag="NA"
    prod_id=prod_eng.replace(" ","_")+comp.replace(" ","_")
    if prod_id not in data:
        data[prod_id]={
            "sno":len(data)+1,
            "prod":prod_eng,
            "comp":comp,
            "tamil_name":prod_tam,
            "pc_rate1":float(pc_1),
            "pc_rate_cus":float(pc_rt),
            "pc_rate_cnt":float(pc_ct),
            "box_pr":float(box_pr),
            "box_count":int(box_ct),
            "prod_tag":tag,
            "mrp":float(mrp)
        }
    json_utils.write_json(file,data)
    stock_data=json_utils.read_json(stock_file)

    if prod_id not in stock_data:
        stock_data[prod_id]={
            "sno":len(stock_data)+1,
            "prod":prod_eng,
            "comp":comp,
            "mrp": float(mrp),
            "cp": 0,
            "item_stock":0,
            "margin_pc":0,
            "margin_cus_pc":0,
            "margin_box":0,
            "sp_1":float(pc_1),
            "sp_cus":float(pc_rt),
            "sp_box":float(box_pr),
        }
        json_utils.write_json(stock_file,stock_data)

def update_product(p_id,prod_name,tamil_name,pc_rate1,pc_rate_cus,rate_box,mrp,file,stock_file):
    data=json_utils.read_json(file)
    data[p_id]["pc_rate1"]=float(pc_rate1)
    data[p_id]["pc_rate_cus"]=float(pc_rate_cus)
    data[p_id]["box_pr"]=float(rate_box)
    data[p_id]["mrp"]=float(mrp)
    data[p_id]["prod"]=prod_name
    data[p_id]["tamil_name"]=tamil_name
    stock_data=json_utils.read_json(stock_file)
    stock_data[p_id]["mrp"]=float(mrp)
    stock_data[p_id]["sp_1"]=float(pc_rate1)
    stock_data[p_id]["sp_cus"]=float(pc_rate_cus)
    stock_data[p_id]["sp_box"]=float(rate_box)
    stock_data[p_id]["margin_pc"]=round(((data[p_id]["pc_rate1"]-stock_data[p_id]["cp"])*100/data[p_id]["pc_rate1"]),2)
    stock_data[p_id]["margin_cus_pc"]=round(((data[p_id]["pc_rate_cus"]-stock_data[p_id]["cp"])*100/data[p_id]["pc_rate_cus"]),2)
    stock_data[p_id]["margin_box"]=round(((data[p_id]["box_pr"]-stock_data[p_id]["cp"])*100/data[p_id]["box_pr"]),2)
    print(data[p_id])
    print(stock_data[p_id])
    json_utils.write_json(file,data)
    json_utils.write_json(stock_file,stock_data)
    print("price updated")

def update_stock(df,pf,sf,prod,cp,nos):
    stock_data=json_utils.read_json(sf)
    product_data=json_utils.read_json(pf)
    prod_id=prod
    comp=stock_data[prod_id]["comp"]
    if prod_id in stock_data:
        stock_data[prod_id]["cp"]=cp
        stock_data[prod_id]["item_stock"]=int(stock_data[prod]["item_stock"])+nos
        stock_data[prod_id]["margin_pc"]=round(((product_data[prod]["pc_rate1"]-cp)*100/product_data[prod]["pc_rate1"]),2)
        stock_data[prod_id]["margin_cus_pc"]=round(((product_data[prod]["pc_rate_cus"]-cp)*100/product_data[prod]["pc_rate_cus"]),2)
        stock_data[prod_id]["margin_box"]=round(((product_data[prod]["box_pr"]-cp)*100/product_data[prod]["box_pr"]),2)
        json_utils.write_json(sf,stock_data)
    else:
        print("invalid product")
    ledger_data=json_utils.read_json(df)
    ledger_data[comp]["purchase"]=ledger_data[comp]["purchase"]+cp*nos
    ledger_data[comp]["balance"]=ledger_data[comp]["purchase"]-ledger_data[comp]["paid"]
    ledger_data["summary"]["purchase"]=ledger_data["summary"]["purchase"]+cp*nos
    ledger_data["summary"]["balance"]=ledger_data["summary"]["purchase"]-ledger_data["summary"]["paid"]
    json_utils.write_json(df,ledger_data)
    
    
    