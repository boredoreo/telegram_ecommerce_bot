import mysql.connector as connector
from dotenv.main import load_dotenv
from .models import User, Student
import os

load_dotenv()



def commit_user(user:User):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    userid = user.userid
    role = user.role
    crsr = mycon.cursor()
    print(userid)
    crsr.execute(
        "INSERT INTO user (userid, role) VALUES (%s, %s)",
        (userid, role)
    )
    mycon.commit()

    mycon.close()
    

# def commit_vendor(vendor:Vendor):
#     mycon = connector.connect(
#     host=os.environ["DB_HOST"],
#     user=os.environ["DB_USER"],
#     password=os.environ["DB_PASSWORD"],
#     database=os.environ["DATABASE"]
#     )

#     userid = vendor.userid
#     name = vendor.name
#     shop_name = vendor.shop_name
#     email = vendor.email
#     phone_no = vendor.phone_no
#     crsr = mycon.cursor()
#     crsr.execute(
#         "INSERT INTO vendor (userid, name, shop_name,email,  phone_no) VALUES (%s, %s, %s, %s, %s)",
#         (userid, name, shop_name, email, phone_no)
#         )
#     mycon.commit()
#     mycon.close()

def commmit_student(student:Student):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    role = student.role
    userid = student.userid
    name = student.name
    matno = student.matno
    email = student.email
    room = student.room
    mycursor = mycon.cursor()
    mycursor.execute(
        "INSERT INTO student (role, userid, name, email, matno ,  room) VALUES (%s, %s, %s,%s, %s, %s)",
        (role, userid,name,email, matno,room)
         )
    mycon.commit()
    mycon.close()

# def commit_product(product:Product):

#     mycon = connector.connect(
#     host=os.environ["DB_HOST"],
#     user=os.environ["DB_USER"],
#     password=os.environ["DB_PASSWORD"],
#     database=os.environ["DATABASE"]
#     )

#     name = product.name
#     image = product.image
#     description = product.description
#     vendorID = product.vendorID
#     available =product.available
#     price = product.price

#     crsr = mycon.cursor()
#     crsr.execute(
#         "INSERT INTO product (name, image, description, vendorID, available, price) VALUES (%s,%s,%s,%s,%s,%s)",
#         ( name, image, description, vendorID, available, price)
#     )
#     mycon.commit()
#     mycon.close()

# def edit_product(product:Product):

#     mycon = connector.connect(
#     host=os.environ["DB_HOST"],
#     user=os.environ["DB_USER"],
#     password=os.environ["DB_PASSWORD"],
#     database=os.environ["DATABASE"]
#     )

#     crsr = mycon.cursor()
#     crsr.execute(
#         "UPDATE product SET name=%s, image=%s, description=%s,available=%s, price =%s WHERE id = %s",
#         (product.name, product.image, product.description, product.available, product.price, product.instance)
#     )
#     mycon.commit()
#     print((product.name, product.image, product.description, product.available, product.price, product.instance))
#     mycon.close()
#     print("dofnn")

def delete_product(product_id):

    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    crsr = mycon.cursor()
    crsr.execute(
        "DELETE FROM product WHERE id = %s",
        (product_id,)
    )
    mycon.commit()
    mycon.close()


def img_to_blob(img):

    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    data = None
    if os.path.exists(img):
        with open(img, "rb") as file:
            data = file.read()
        os.remove(img)
        mycon.close()
        return data

    

def load_blob(blob, file_name):

    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    with open(file_name, "wb") as file:
        file.write(blob)

    mycon.close()

def create_order():
    pass

def create_order_item():
    "id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, order_id INT, item_count INT, FOREIGN KEY (product_id) REFERENCES product(id), FOREIGN KEY (order_id) REFERENCES orders(id)"
    pass
