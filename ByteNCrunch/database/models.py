from enum import Enum


class User:
    
    def __init__(self,userid=None, role=None):
        self.userid=userid
        self.role=role
        

        
class Student:

    def __init__(self, role=None, userid=None, name=None, matno=None,email=None, room= None, account_number=None, bank=None):
        self.role = role
        self.userid = userid
        self.name =name
        self.matno=matno
        self.email = email
        self.room = room
        self.account_number= account_number
        self.bank = bank

    def __str__(self):
        return self.role


class Order:
	def __init__(self, id=None,customer_id=None,status=None):
		self.id = id
		self.customer_id= customer_id
		self.status = status
		
		
class OrderItem:
	def __init__(self, id=None,product_id=None,order=None,item_count=0):
		self.id=id
		self.product_id = product_id
		self.order=order
		self.item_count=item_count
		
		
class Status(Enum):
	Delivered = "delivered"
	Cancelled = "cancelled"
	Pending = "pending"
	Rejected_By_Vendor = "rejected_by_vendor"
	
	
            
