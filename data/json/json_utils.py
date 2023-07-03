import json

def read_json(file):
    try:
        f=open(file)
        data=json.load(f)
        f.close()
    except:
        data={
          "vendors":[] 
        }
        write_json(file,data)
    return data

def write_json(file,data):
    f=open(file,"w")
    data_json=json.dumps(data,indent=3)
    f.write(data_json)
    f.close()

def clear_json(file,data):
    f=open(file,"w")
    data_json=json.dumps(data,indent=3)
    f.write(data_json)
    f.close()