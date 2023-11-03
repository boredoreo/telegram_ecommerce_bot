import mysql.connector as connector
from dotenv.main import load_dotenv
import os

load_dotenv()

def create_database(host, user, password, name):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE {}".format(name))
    mydb.commit() 

def create_table(host, user, password, name, fields):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )

    operation = "CREATE TABLE {} ({})".format(name, fields)
    crsr = mydb.cursor()
    crsr.execute(operation)
    mydb.commit()

tables = {
    "student" : "role CHAR(120), userid BIGINT PRIMARY KEY, name VARCHAR(120), matno CHAR(10) UNIQUE,room VARCHAR(255), account_number CHAR(10), bank CHAR(180)",
    "vendor" : "userid BIGINT PRIMARY KEY, name VARCHAR(120), shop_name VARCHAR(500) UNIQUE,email CHAR(120), phone_no CHAR(11), account_number CHAR(10), bank CHAR(180)",
    "product" : "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), image LONGBLOB, description VARCHAR(800), vendorID BIGINT, available BOOL, price INT, FOREIGN KEY (vendorID) REFERENCES vendor(userid)",
    "orders" : "id INT AUTO_INCREMENT PRIMARY KEY , customer_id BIGINT, status CHAR(120), item_count INT, FOREIGN KEY (customer_id) REFERENCES student(userid)",
    "order_item" : "id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, order_id INT, item_count INT, FOREIGN KEY (product_id) REFERENCES product(id), FOREIGN KEY (order_id) REFERENCES orders(id)",
    "user" : " userid BIGINT PRIMARY KEY, role CHAR(120) "

}

create_database("localhost", "root", "302914", "ByteNCrunch")
for key, val in tables.items():
    create_table("localhost", "", "302914", key, val
    )