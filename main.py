from flask import Flask, render_template, redirect, request, url_for, jsonify, session
from flask_session import Session
import data.json.json_utils as json_utils
import create_ledger
import product_manager
import stock_manager
from ps1 import Ps1, Ps2
import shutil
from datetime import datetime


app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

store_admin=Ps1()
store_admin_2=Ps2()

def login(user,password):
      user_data=json_utils.read_json("data/json/users.json")
      print(user_data["admin"],user,password)
      for users in user_data["admin"]:
            if user in users.keys():
                  if users[user]==password:
                        print("admin logged in")
                        session["name"]="admin"
                        return True
      for users in user_data["users"]:
            if user in users.keys():
                  if users[user]==password:
                        print("user logged in")
                        session["name"]="user"
                        return True
                  
@app.route("/logout",methods=["POST","GET"])
def logout():
      print("logging out ...")
      for key in list(session.keys()):
            session.pop(key)
      return redirect("/")

data=create_ledger.json_utils.read_json(store_admin.data_file)



@app.route("/")
def index():
    return render_template("login.html")

@app.route("/home",methods=["POST","GET"])
def home():
      if request.method=="POST":
            if login(request.form["userid"],request.form["password"]):
                  return render_template("homepage.html",user=session["name"])
            else:
                 return redirect("/")
      if request.method=="GET":
            if not session.get("name"):
                  return redirect("/")
            else:
                 return render_template("homepage.html",user=session["name"])
       

@app.route("/ledger",methods=["POST","GET"])
def ledger():
      if not session.get("name"):
        return redirect("/")
      info=""
      err=""
      if request.method=="POST":
            ledger=create_ledger.create_ledger(request.form["name"],request.form["address"],request.form["gst"],request.form["phone"],store_admin.data_file)
            if ledger:
                  info="Ledger created successfully !"
                  data=create_ledger.json_utils.read_json(store_admin.data_file)
            else:
                  err="Some error creating ledger! Please contact admin"
                  
            return render_template("homepage.html",err=err,info=info,data=data,user=session["name"])
      else:
            data=create_ledger.json_utils.read_json(store_admin.data_file)
            ledger_data=create_ledger.json_utils.read_json(store_admin.data_file)
            return render_template("ledger_dashboard.html",data=data,summary=data["summary"],ledger_data=ledger_data)
      
@app.route("/stock_bill_update",methods=["POST","GET"])
def stock_bill_update():
      if not session.get("name"):
        return redirect("/")
      print(request.method)
      if request.method=="POST":
            stock_manager.update_stock()
      return redirect("/bills")


@app.route("/stock/<msg>",methods=["POST","GET"])
@app.route("/stock",methods=["POST","GET"])
def stock(msg=None):
      if not session.get("name"):
        return redirect("/")
      if msg==None:
            info=""
      elif msg=="updated":
            info="Updated successfully!"
      err=""
      if request.method=="POST":
            product_manager.create_product(store_admin.product_file,store_admin.stock_file,request.form["product_en"],
                                           request.form["product_ta"],request.form["pc_1_rate"],
                                           request.form["pc_cus_rate"],request.form["pc_cus_count"],
                                           request.form["box_rate"],request.form["box_count"],request.form["tag"],request.form["comp"]
                                           ,request.form["mrp"])
            info="product added successfully"
            data=create_ledger.json_utils.read_json(store_admin.product_file)
            ledger_data=create_ledger.json_utils.read_json(store_admin.data_file)
            return render_template("product.html",info=info,err=err,data=data,ledger_data=ledger_data)
      else:
            data=create_ledger.json_utils.read_json(store_admin.product_file)
            ledger_data=create_ledger.json_utils.read_json(store_admin.data_file)
            return render_template("product.html",info=info,err=err,data=data,ledger_data=ledger_data)



@app.route("/stockmanager",methods=["POST","GET"])
@app.route("/stockmanager/<msg>",methods=["POST","GET"])
def stockmanager(msg=None):
      if not session.get("name"):
        return redirect("/")
      if msg==None:
            info=""
      else:
            info="stock updated successfully"
      err=""
      if request.method=="POST":
           
           product_manager.update_stock(store_admin.data_file,store_admin.product_file,store_admin.stock_file,request.form["product"],float(request.form["cp"]),int(request.form["nos"]))

      data=json_utils.read_json(store_admin.data_file)
      prod_data=json_utils.read_json(store_admin.product_file)
      stock_data=json_utils.read_json(store_admin.stock_file)
      return render_template("stock_dashboard.html",ledger_data=data,prod_data=prod_data,stock_data=stock_data,info=info)

@app.route("/payment",methods=["POST","GET"])
def make_payment():
      if not session.get("name"):
        return redirect("/")
      info=""
      err=""
      if request.method=="POST":
            create_ledger.make_payment(store_admin.data_file,request.form["comp"],float(request.form["amount"]))
      data=create_ledger.json_utils.read_json(store_admin.data_file)
      ledger_data=create_ledger.json_utils.read_json(store_admin.data_file)
      return render_template("ledger_dashboard.html",data=data,summary=data["summary"],ledger_data=ledger_data)

@app.route("/bills",methods=["POST","GET"])
@app.route("/bills/<int:id>",methods=["POST","GET"])
def bill_manager(id=None):
      if not session.get("name"):
        return redirect("/")
      info=""
      err=""
      data=json_utils.read_json(store_admin.data_file)
      prod_data=json_utils.read_json(store_admin.product_file)
      stock_data=json_utils.read_json(store_admin.stock_file)
      bill_data=json_utils.read_json(store_admin.bill_file)
      total=0
      savings=0
      if id!=None:
            sno=1
            for item in bill_data["items"]:
                  if id==item["sno"]:
                        bill_data["items"].remove(item)
            for item in bill_data["items"]:
                  item["sno"]=sno
                  sno+=1
      elif request.method=="GET":
            print("reset ")
            bill_init={
                  "items":[]
            }
            json_utils.clear_json(store_admin.bill_file,bill_init)
            bill_data=json_utils.read_json(store_admin.bill_file)

      if request.method=="POST":
            prod_id=request.form["product"]
            nos=int(request.form["nos"])
            print(nos<prod_data[prod_id]["pc_rate_cnt"])
            if request.form["cus"]!="":
                  calc_rate=float(request.form["cus"])
            elif nos<prod_data[prod_id]["pc_rate_cnt"]:
                  calc_rate=float(prod_data[prod_id]["pc_rate1"])
            elif nos<prod_data[prod_id]["box_count"]:
                  calc_rate=float(prod_data[prod_id]["pc_rate_cus"])
            else:
                  calc_rate=float(prod_data[prod_id]["box_pr"])
            add_item={
                  "sno": len(bill_data["items"])+1,
                  "product": prod_data[request.form["product"]]["tamil_name"],
                  "pc_rate":calc_rate,
                  "mrp":stock_data[request.form["product"]]["mrp"],
                  "Nos":int(request.form["nos"]),
                  "amount": int(request.form["nos"])*calc_rate,
                  "saving": int(request.form["nos"])*(float(stock_data[request.form["product"]]["mrp"])-calc_rate),
                  "stock_key":request.form["product"]
                  }
            bill_data["items"].append(add_item)
      json_utils.write_json(store_admin.bill_file,bill_data)
      bill_data=json_utils.read_json(store_admin.bill_file)
      for item in bill_data["items"]:
            total=total+item["amount"]
            savings=savings+item["saving"]
      return render_template("biller_tool.html",ledger_data=data,prod_data=prod_data,stock_data=stock_data,bill_data=bill_data["items"],total=total,savings=savings)

@app.route("/print",methods=["POST","GET"])
@app.route("/print/<id>",methods=["POST","GET"])
def print_page(id=None):
      
      if not session.get("name"):
            return redirect("/")    
      if id !=None:
            bill_summary=json_utils.read_json("data/json/bills/bill_summary.json")
            bill_data=json_utils.read_json(bill_summary[id]["file"])
            total=savings=0
            for item in bill_data["items"]:
                  total=total+item["amount"]
                  savings=savings+item["saving"]
            return  render_template("billing_invoice.html",bill_data=bill_data["items"],total=total,savings=savings)
      dt=datetime.now().strftime("%Y%m%d%H%M%S")
      file_name="data/json/bills/bill_backup"+str(dt)+".json"
      shutil.copyfile("data/json/bill.json",file_name)
      bill_summary=json_utils.read_json("data/json/bills/bill_summary.json")
      bill_size=len(bill_summary)
      bill_data=json_utils.read_json(file_name)
      total=0
      savings=0
      for item in bill_data["items"]:
            total=total+item["amount"]
            savings=savings+item["saving"]
      bill_summary["bill"+str(bill_size+1)]={
            "sno":str(bill_size+1),
            "file":file_name,
            "total":total
      }
      json_utils.write_json("data/json/bills/bill_summary.json",bill_summary)
      return render_template("billing_invoice.html",bill_data=bill_data["items"],total=total,savings=savings)

@app.route("/dailysummary", methods=["POST","GET"])
def daily_summary():
      print(session.get("name"))
      if not session.get("name"):
        return redirect("/")
      summary=json_utils.read_json("data/json/bills/bill_summary.json")
      total_sales=0
      for bills,val in summary.items():
            total_sales=total_sales+val["total"]
      return render_template("daily_summary.html",summary=summary,total=total_sales)

@app.route("/prod_update/<prod_id>",methods=["POST","GET"])
def product_update(prod_id):
      if not session.get("name"):
        return redirect("/")
      product_manager.update_product(prod_id,request.form["prod_name"],request.form["tamil_name"],request.form["pc_rate1"],request.form["pc_rate_cus"],request.form["pc_rate_box"],request.form["mrp"],store_admin.product_file,store_admin.stock_file)
      msg="updated"
      return redirect(url_for("stock", msg=msg)) 


@app.route("/prod_delete/<prod_id>",methods=["POST","GET"])
def product_delete(prod_id):
      if not session.get("name"):
        return redirect("/")
      info=""
      err=""
      stock_data=json_utils.read_json(store_admin.stock_file)
      data=create_ledger.json_utils.read_json(store_admin.product_file)
      ledger_data=create_ledger.json_utils.read_json(store_admin.data_file)
      if stock_data[prod_id]["item_stock"]>0:
            err="Can't delete items in stock"
            return render_template("product.html",info=info,err=err,data=data,ledger_data=ledger_data)
      else:
            stock_data.pop(prod_id)
            data.pop(prod_id)
            i=1
            for key,val in stock_data.items():
                  stock_data[key]["sno"]=i
                  data[key]["sno"]=i
                  i+=1
            json_utils.write_json(store_admin.stock_file,stock_data)
            json_utils.write_json(store_admin.product_file,data)
            info="product deleted successfully"
            return render_template("product.html",info=info,err=err,data=data,ledger_data=ledger_data)


@app.route("/stock_update/<prod_id>",methods=["POST","GET"])
def stock_update(prod_id):
      if not session.get("name"):
        return redirect("/")
      stock_data=json_utils.read_json(store_admin.stock_file)
      stock_data[prod_id]["item_stock"]=int(request.form["stock"])
      json_utils.write_json(store_admin.stock_file,stock_data)
      return redirect(url_for("stockmanager", msg="updated")) 

if __name__=="__main__":
    app.run(debug=True)