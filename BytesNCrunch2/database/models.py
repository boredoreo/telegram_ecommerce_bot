
class User:
    
    def __init__(self,userid=None, role=None):
        self.userid=userid
        self.role=role
        

        
class Student:

    def __init__(self, role=None, userid=None, name=None, matno=None, room= None, account_number=None, bank=None):
        self.role = role
        self.userid = userid
        self.name =name
        self.matno=matno
        self.room = room
        self.account_number= account_number
        self.bank = bank

    def __str__(self):
        return self.role

    def load_to_dict(self):
        return {
            "role" : self.role,
            "userid" : self.userid,
            "name":self.name,
            "matno":self.matno,
            "room" : self.room,
            "account_nuumber" : self.account_number,
            "bank": self.bank
        }

class Vendor:    
    def __init__(
        self, userid = None,
        name = None,
        shop_name =None,
        email=None,
        phone_no =None,
        account_number=None,
        bank = None
        ):

        self.userid = userid
        self.name = name
        self.shop_name = shop_name 
        self.email = email 
        self.phone_no =phone_no 
        self.account_number = account_number 
        self.bank =  bank

    def load_to_dict(self):
        return {
            "userid" : self.userid,
            "name":self.name,
            "shop_name":self.shop_name,
            "email" : self.email,
            "phone_no" : self.phone_no,
            "account_nuumber" : self.account_number,
            "bank": self.bank
        }
    
    def __str__(self):
        return "vendor"

class Product:
    # mycon = connector.connect(
    #     host=os.environ["DB_HOST"],
    #     user=os.environ["DB_USER"],
    #     password=os.environ["DB_PASSWORD"],
    #     database=os.environ["DATABASE"]
    # )
    name=None
    image=None
    description=None
    vendorID=None
    available=None
    price=None
    instance = None
    def __init__(
        self, name=None, 
        image=None, description=None,
        vendorID=None, available=None, 
        price=None, instance=None
        ):
        self.name = name
        self.image = image
        self.description = description 
        self.vendorID = vendorID 
        self.available = available
        self.price = price
        self.instance = instance

    def load_to_dict(self):
        return {
            "name":self.name,
            "shop_name":self.shop_name,
            "email" : self.email,
            "phone_no" : self.phone_no,
            "account_nuumber" : self.account_number,
            "bank": self.bank
        }
      




            
