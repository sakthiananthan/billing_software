import data.json.json_utils as js
class Ps1:
    def __init__(self) -> None:
        self.data_file="data/json/ledger.json"
        self.product_file="data/json/product.json"
        self.stock_file="data/json/stock.json"
        self.bill_file="data/json/bill.json"
        self.users= js.read_json("data/json/users.json")


class Ps2:
    def __init__(self) -> None:
        self.data_file="data/json/ps2/ledger.json"
        self.product_file="data/json/ps2/product.json"
        self.stock_file="data/json/ps2/stock.json"
        self.bill_file="data/json/ps2/bill.json"
