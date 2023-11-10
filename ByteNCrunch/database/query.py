import mysql.connector as connector
from dotenv.main import load_dotenv
from .models import User, Vendor, Student, Product
import os
import config

load_dotenv()



def is_user(userid = None) -> bool:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    mycon.close()
    if result == []:
        return False
    else:
        return True

def is_vendor(userid) -> bool:

    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    mycon.close()
    if result == []:
        return False
    else:
        return True

def is_student(userid) -> bool:

    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    mycon.close()
    if result == []:
        return False
    else:
        return True

def get_user(userid) -> User:

    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
        )            
    result = crsr.fetchall()[0]  
    mycon.close()
    return User(userid=result[0], role=result[1])

def get_vendor(userid) -> Vendor:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor WHERE userid=%s",
        (userid,)
        )           
    result = crsr.fetchall()[0]  
    mycon.close()
    return Vendor(
        userid=result[0],
        name=result[1],
        shop_name=result[2],
        email=result[4],
        phone_no=result[5],
        account_number=result[6],
        bank=result[7]
    )

def get_all_vendors():
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor"
    )
    result = crsr.fetchall()
    mycon.close()
    return [i + (get_my_products(myid=i[0])[0][2],) for i in result ]

def get_student(userid) ->  Student:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
        )           
    result = crsr.fetchall()[0]  
    mycon.close()
    return Student(
        role=result[0],
        userid=result[1],
        name=result[2],
        matno=result[3],
        room=result[4],
        account_number=result[5],
        bank=result[6]
    )

def get_product(product_id) -> Product:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )
    "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), image LONGBLOB, description VARCHAR(800), vendorID BIGINT, available BOOL, price INT, FOREIGN KEY (vendorID) REFERENCES vendor(userid)"
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE id=%s",
        (product_id,)
    )

    result = crsr.fetchall()[0]
    mycon.close()

    return Product(
        name=result[1],
        image=result[2],
        description=result[3],
        vendorID=result[4],
        available=result[5], 
        price=result[6],
        instance=product_id             
    )

def get_all_products() -> list:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product"
    )

    result = crsr.fetchall()

    mycon.close()

    return result
   

def get_products_from(myid):
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE vendorID=%s",
        (myid,)
    )

    result = crsr.fetchall()
    mycon.close()
    return result

