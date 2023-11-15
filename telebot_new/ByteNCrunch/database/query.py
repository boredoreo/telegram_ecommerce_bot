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
    return 0

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
    return result

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
    # "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), image LONGBLOB, description VARCHAR(800), vendorID BIGINT, available BOOL, price INT, FOREIGN KEY (vendorID) REFERENCES vendor(userid)"
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE id=%s",
        (product_id,)
    )

    result = crsr.fetchall()[0]
    mycon.close()

    return result

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
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE vendorID=%s",(myid,)
    )

    result = crsr.fetchall()
    mycon.close()
    return result

