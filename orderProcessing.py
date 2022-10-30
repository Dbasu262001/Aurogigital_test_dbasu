import xml.etree.ElementTree as ET


class OrderNode:
    def __init__(self,price,volume,orderId):
        self.price=price
        self.volume=volume
        self.orderId=orderId
        self.previous=None
        self.next=None

class OrderList:
    def __init__(self,listType):
        self.head=None
        self.tail=None
        self.length=0
        self.listType = listType
    
    def addNode(self,price,volume,orderId):
        Node = OrderNode(price,volume,orderId)
        self.length+=1
        if(self.head==None):
            self.head=Node
            self.tail=Node
        else:
            # listType = 0  for buy list
            if(self.listType==0):
                n=self.head
                while(n!=None and n.price<price):
                    n=n.next
                if(n!=None):
                    if(n!=self.head):
                        Node.previous=n.previous.next
                        n.previous.next=Node
                        Node.next=n
                        n.previous = Node
                    else:
                        Node.next=self.head
                        self.head.previous=Node
                        self.head=Node
                else:
                    Node.previous=self.tail
                    self.tail.next=Node
                    self.tail=Node
            else:
                n=self.head
                while(n!=None and n.price>price):
                    n=n.next
                if(n!=None):
                    if(n!=self.head):
                        Node.previous=n.previous.next
                        n.previous.next=Node
                        Node.next=n
                        n.previous = Node
                    else:
                        Node.next=self.head
                        self.head.previous=Node
                        self.head=Node
                else:
                    Node.previous=self.tail
                    self.tail.next=Node
                    self.tail=Node
    def deleteNode(self,orderId):
        self.length-=1
        n=self.head
        while(n!=None and n.orderId!=orderId):
            n=n.next
        if(n!=None):
            if(n==self.head):
                self.head=self.head.next
                self.head.previous.next=None
                self.head.previous =None
            elif(n==self.tail):
                self.tail =self.tail.previous
                self.tail.next.previous=None
                self.tail.next=None
            else:
                n.previous.next=n.next
                n.next.previous=n.previous
                n.next=None
                n.previous=None
    
    def find(self,price,volume):
        vol =volume
        n=self.head
        if(self.listType == 0):
            while(n!=None):
                if(n.price>= price):
                    if(vol> n.volume):
                        vol-=n.volume
                        nn = n.next
                        if(n==self.head):
                            self.head=self.head.next
                            self.head.previous.next=None
                            self.head.previous =None
                        elif(n==self.tail):
                            self.tail =self.tail.previous
                            self.tail.next.previous=None
                            self.tail.next=None
                        else:
                            n.previous.next=n.next
                            n.next.previous=n.previous
                            n.next=None
                            n.previous=None
                        n=nn
                    elif (vol == n.volume):
                        vol-=n.volume
                        if(n==self.head):
                            self.head=self.head.next
                            self.head.previous.next=None
                            self.head.previous =None
                        elif(n==self.tail):
                            self.tail =self.tail.previous
                            self.tail.next.previous=None
                            self.tail.next=None
                        else:
                            n.previous.next=n.next
                            n.next.previous=n.previous
                            n.next=None
                            n.previous=None
                        break
                    else:
                        n.volume-=vol
                        vol = 0
                        break
                else:
                    break
        else:
            while(n!=None):
                if(n.price<= price):
                    if(vol> n.volume):
                        vol-=n.volume
                        nn = n.next
                        if(n==self.head):
                            self.head=self.head.next
                            self.head.previous.next=None
                            self.head.previous =None
                        elif(n==self.tail):
                            self.tail =self.tail.previous
                            self.tail.next.previous=None
                            self.tail.next=None
                        else:
                            n.previous.next=n.next
                            n.next.previous=n.previous
                            n.next=None
                            n.previous=None
                        n=nn
                    elif (vol == n.volume):
                        vol-=n.volume
                        if(n==self.head):
                            self.head=self.head.next
                            self.head.previous.next=None
                            self.head.previous =None
                        elif(n==self.tail):
                            self.tail =self.tail.previous
                            self.tail.next.previous=None
                            self.tail.next=None
                        else:
                            n.previous.next=n.next
                            n.next.previous=n.previous
                            n.next=None
                            n.previous=None
                        break
                    else:
                        n.volume-=vol
                        vol = 0
                        break
                else:
                    break
        return vol
    
    def show(self):
        n=self.head
        while(n!=None):
            print(n.volume,"@",n.val)
            n=n.next
    
class Book:
    def __init__(self):
        self.BuyList = OrderList(0)
        self.SellList = OrderList(1)

tree = ET.parse('orders.xml')

root = tree.getroot()
a = list(root)
print(str(a[0].tag)=='AddOrder')

Book1 = Book()
Book2 = Book()
Book3 = Book()

Books = {1:Book1 , 2:Book2 ,3:Book3}
for i in range(len(a)):
    bookNumber = 0
    print(i)
    if(a[i].get('book')=='book-1'):
        bookNumber=1
    elif(a[i].get('book')=='book-2'):
        bookNumber=2
    elif(a[i].get('book')=='book-3'):
        bookNumber=3
        
    orderType=0
    if(a[i].get('operation')=='SELL'):
        orderType=1
    
    price=float(a[i].get('price'))
    volume=int(a[i].get('volume'))
    orderId = int(a[i].get('orderId'))
    if(str(a[i].tag)=='AddOrder'):
        if(orderType == 0):
            remVol = Books[bookNumber].SellList.find(price,volume)
            if(remVol>0):
                Books[bookNumber].BuyList.addNode(price,volume,orderId)
        else:
            remVol = Books[bookNumber].BuyList.find(price,volume)
            if(remVol>0):
                Books[bookNumber].SellList.addNode(price,volume,orderId)
    else:
        Books[bookNumber].SellList.deleteNode(orderId)
        Books[bookNumber].BuyList.deleteNode(orderId)

Book1.BuyList.show()
Book2.SellList.show()