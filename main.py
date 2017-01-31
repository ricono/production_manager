import pymysql, production_order, datetime

"""Connection with db"""
try:
    mydb = pymysql.connect(user = 'root', password = '', host = '127.0.0.1', db = 'production', charset='utf8')
    cur = mydb.cursor()
except pymysql.Error:
    print("There was a problem in connecting to the database.  Please ensure that the 'aegton' database exists on the local host system.")
    raise pymysql.Error
except pymysql.Warning:
    pass

def product_name():
    """Check, is name of product fine"""
    name = input("Name of product (mirnati/alenti): ").lower()
    while name !="miranti" and name != "alenti":
        name = input("Name of product (mirnati/alenti): ").lower()
    return name

def validdate():
    """Check, is date formay fine"""
    while True:
        try:
            date = input("Please enter production date (YYYY-MM-DD): ")
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD")

def valid_digit():
    """Is digit"""
    value = input("Please enter quantity: ")
    if value.isdigit() is not True:
        value = valid_digit()
    else:
        return value
    

def add_po(): 
    statement = "INSERT INTO production_plan VALUES (NULL, 'miranti','0000-00-00', '0000-00-00',0)"
    cur.execute(statement)
    mydb.commit()
    statement = "SELECT ID FROM production_plan ORDER BY ID DESC LIMIT 1"
    cur.execute(statement)
    ponumber = cur.fetchone()
    ponumber = ponumber[0]
    product = product_name()
    production_date = validdate()
    qty = valid_digit()
    new_po = production_order.PO(ponumber, product, production_date, qty)
    statement = "UPDATE production_plan SET product = '%s', orderdate = '%s', productiondate = '%s', qty = '%s' WHERE ID = '%s'" %(new_po.product, new_po.order_date, new_po.production_date, new_po.qty, new_po.ponumber)
    cur.execute(statement)
    mydb.commit()
    new_po.show_info()

add_po()
