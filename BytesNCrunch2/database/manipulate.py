import mysql.connector as connector
from dotenv.main import load_dotenv
from .models import User, Vendor, Student, Product
import os

load_dotenv()

mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

def commit_user(user:User):
    userid = user.userid
    role = user.role
    crsr = mycon.cursor()
    print(userid)
    crsr.execute(
        "INSERT INTO user (userid, role) VALUES (%s, %s)",
        (userid, role)
    )
    mycon.commit()
    user_type.commit()

def commit_vendor(vendor:Vendor):
    userid = vendor.userid
    name = vendor.name
    shop_name = vendor.shop_name
    email = vendor.email
    phone_no = vendor.phone_no
    crsr = mycon.cursor()
    crsr.execute(
        "INSERT INTO vendor (userid, name, shop_name,email,  phone_no) VALUES (%s, %s, %s, %s, %s)",
        (userid, name, shop_name, email, phone_no)
        )
    mycon.commit()

def commmit_student(student:Student):
    role = student.role
    userid = student.userid
    name = student.name
    matno = student.matno
    room = student.room
    mycursor = mycon.cursor()
    mycursor.execute(
        "INSERT INTO student (role, userid, name, matno ,  room) VALUES (%s, %s, %s, %s, %s)",
        (role, userid,name,matno,room)
         )
    mycon.commit()

def commit_product(product:Product):
    "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), image LONGBLOB, description VARCHAR(800), vendorID BIGINT, available BOOL, price INT, FOREIGN KEY (vendorID) REFERENCES vendor(userid)"
    name = product.name
    image = product.image
    description = product.description
    vendorID = product.vendorID
    available =product.available
    price = product.price

    crsr = mycon.cursor()
    crsr.execute(
        "INSERT INTO product (name, image, description, vendorID, available, price) VALUES (%s,%s,%s,%s,%s,%s)",
        ( name, image, description, vendorID, available, price)
    )
    mycon.commit()



def img_to_blob(img):
    data = None
    if os.path.exists(img):
        with open(img, "rb") as file:
            data = file.read()
        os.remove(img)

        return data

def load_blob(blob, file_name):
    with open(file_name, "wb") as file:
        file.write(blob)