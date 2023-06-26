import mysql.connector as connector
from dotenv.main import load_dotenv
from .models import User, Vendor, Student, Product
import os
import config

load_dotenv()

mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE
    )

def is_user(userid = None) -> bool:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    if result == []:
        return False
    else:
        return True

def is_vendor(userid) -> bool:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    if result == []:
        return False
    else:
        return True

def is_student(userid) -> bool:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    if result == []:
        return False
    else:
        return True

def get_user(userid) -> User:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
        )            
    result = crsr.fetchall()[0]  
    return User(userid=result[0], role=result[1])

def get_vendor(userid) -> Vendor:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor WHERE userid=%s",
        (userid,)
        )           
    result = crsr.fetchall()[0]  
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
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor"
    )
    result = crsr.fetchall()
    return [i + (get_my_products(myid=i[0])[0][2],) for i in result ]

def get_student(userid) ->  Student:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
        )           
    result = crsr.fetchall()[0]  
    return Student(
        role=result[0],
        userid=result[1],
        name=result[2],
        matno=result[3],
        room=result[4],
        account_number=result[5],
        bank=result[6]
    )

def get_product(product_id) -> list:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE id=%s",
        (product_id,)
    )

    return crsr.fetchall()[0]

def get_all_products() -> list:
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product"
    )

    return crsr.fetchall()
   

def get_my_products(myid):
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE vendorID=%s",
        (myid,)
    )

    return crsr.fetchall()

