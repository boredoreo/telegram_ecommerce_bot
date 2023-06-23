import mysql.connector as connector
from dotenv.main import load_dotenv
import os

load_dotenv()

#User Model
class User:
    userid = None
    role = None
    #Either Vendor() or Student()
    user_type = None
    mycon = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    def __init__(self, instance=None):
        if instance != None:
            self.userid =instance
            crsr = self.mycon.cursor()
            crsr.execute(
                "SELECT * FROM user WHERE userid=%s",
                (instance,)
            )
            result = crsr.fetchall()[0]
            self.userid, self.role = result
            print(result)

            match self.role:
                case "vendor":
                    self.user_type = Vendor(instance=instance)
                
                case "customer" | "dispatcher":
                    self.user_type = Student(instance=instance)


    def commit(self):
        crsr = self.mycon.cursor()
        print(self.userid)
        crsr.execute(
            "INSERT INTO user (userid, role) VALUES (%s, %s)",
            (self.userid, self.role)
        )
        self.mycon.commit()
        self.user_type.commit()

    def is_user(self, userid):
        crsr = self.mycon.cursor()
        crsr.execute(
            "SELECT * FROM user WHERE userid=%s",
            (userid,)
        )
        result = crsr.fetchall()
        if result == []:
            return False
        else:
            self.instance = userid
            print(userid)
            return True

#Customer Model
class Student():

    old_customer = None 
    mycon = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    def __init__(self, role=None, userid=None, name=None, matno=None, room= None,instance=None):
        self.role = role
        self.userid = userid
        self.name =name
        self.matno=matno
        self.room = room
        if instance != None:
            csrs = self.mycon.cursor()
            csrs.execute(
                "SELECT * FROM student WHERE userid={}".format(instance)
            )
            result = csrs.fetchall()[0]
            self.role, self.userid, self.name, self.matno, self.room, account_no, bank = result
            
    def commit(self):
        mycursor = self.mycon.cursor()
        mycursor.execute(
            "INSERT INTO student (role, userid, name, matno ,  room) VALUES (%s, %s, %s, %s, %s)",
            (self.role, self.userid,self.name,self.matno,self.room)
             )
        self.mycon.commit()


class Vendor:
    mycon = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    userid = None
    name = None
    shop_name =None
    email=None
    phone_no =None
    account_number=None
    bank = None
    
    def __init__(
        self, userid = None,
        name = None,
        shop_name =None,
        email=None,
        phone_no =None,
        account_number=None,
        bank = None,
        instance=None):

        self.userid, self.name, self.shop_name,self.email, self.phone_no, self.account_number, self.bank = userid, name, shop_name, email, phone_no, account_number, bank
        if instance != None:
            crsr = self.mycon.cursor()
            crsr.execute(
                "SELECT * FROM vendor WHERE userid={}".format(instance)
            )
            result = crsr.fetchall()[0]
            self.userid, self.name, self.shop_name,self.email, self.phone_no, self.account_number, self.bank = result


            
    def get_all(self):
        crsr = self.mycon.cursor()
        crsr.execute(
            "SELECT * FROM vendor"
        )

        result = crsr.fetchall()
        print(result)
        print(type(result[0]))
        return [i + (Product().get_my_all(myid=i[0])[0][2],) for i in result ]
      
        
    def commit(self):
        crsr = self.mycon.cursor()
        crsr.execute(
           "INSERT INTO vendor (userid, name, shop_name,email,  phone_no) VALUES (%s, %s, %s, %s, %s)",
            (self.userid, self.name, self.shop_name, self.email, self.phone_no)
            )
        self.mycon.commit()

class Product:
    mycon = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    name=None
    image=None
    description=None
    vendorID=None
    available=None
    price=None
    instance = None
    def __init__(self, name=None, image=None, description=None, vendorID=None, available=None, price=None, instance=None):
        self.name, self.image, self.description, self.vendorID, self.available, self.price, self.instance = name, image, description, vendorID, available, price, instance
        if instance != None:
            crsr = self.mycon.cursor()
            crsr.execute(
                "SELECT * FROM product WHERE id=%s",
                (instance,)
            )
            self.instance=instance

    def get_my_all(self, myid):
        crsr = self.mycon.cursor()
        crsr.execute(
            "SELECT * FROM product WHERE vendorID=%s",
            (myid,)
        )

        return crsr.fetchall()
        

    def get_all(self):
        crsr = self.mycon.cursor()
        crsr.execute(
            "SELECT * FROM product"
        )

        return crsr.fetchall()



    def edit(self, name, image, description, price, instance):
        crsr = self.mycon.cursor()
        crsr.execute(
            "UPDATE product SET name=%s, image=%s, description=%s, price =%s WHERE id = %s",
            ( name, image, description, price, instance)
        )
        self.mycon.commit()

    def commit(self):
        crsr = self.mycon.cursor()
        crsr.execute(
            "INSERT INTO product (name, image, description, vendorID, available, price) VALUES (%s,%s,%s,%s,%s,%s)",
            ( self.name, self.image, self.description, self.vendorID, self.available, self.price)
        )
        self.mycon.commit()


class OrderItem:
    
    mycon = connector.connect(
        host="localhost",
        user="oreo",
        password="302914",
        database="ByteNCrunch"
    )
    def __init__(self, product_id, order_id, item_count):
        self.product_id, self.order_id, self.item_count = product_id, order_id, item_count
        
    def commit(self):
        crsr = mycon.cursor()
        crsr.eexecute(
            "INSERT INTO order_item (product_id, order_id, item_count)  VALUES (%s, %s, %s)", 
            (self.product_id, self.order_id, self.item_count )
        )
        mycon.commit()
 