import pymysql, production_order, datetime, prettytable

M = 12
A = 10
PRODUCTS = ("miranti", "alenti")

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
    while name not in PRODUCTS:
        name = input("Name of product (mirnati/alenti): ").lower()
    return name

def valid_date():
    """Check, is date formay fine"""
    while True:
        try:
            date = input("Please enter production date (YYYY-MM-DD): ")
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD")

def valid_digit(text):
    """Is digit"""
    text=text
    value = input("Please enter %s: " %text)
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
    production_date = valid_date()
    qty = valid_digit("quantity")
    new_po = production_order.PO(ponumber, product, production_date, qty)
    statement = "UPDATE production_plan SET product = '%s', orderdate = '%s', productiondate = '%s', qty = '%s' WHERE ID = '%s'" %(new_po.product, new_po.order_date, new_po.production_date, new_po.qty, new_po.ponumber)
    cur.execute(statement)
    mydb.commit()
    new_po.show_info()

def show_po():
    date = valid_date()
    statement = "SELECT * FROM production_plan WHERE productiondate = '%s'" %(date)
    cur.execute(statement)
    table = cur.fetchall()
    print_table(table)
    return table

def print_table(table):
    table= table
    x = prettytable.PrettyTable()
    x.field_names = ["PO number", "Product", "Creating date", "Production date", "Quantity"]
    for i in range(0, len(table)):
        x.add_row([table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]])
    print(x.get_string())
    return table

def delete_po():
    table = show_po()
    po_number = valid_digit("po number")
    print(po_number)
    for i in range(0, len(table)):
        if table[i][0] == int(po_number):
            statement = "DELETE FROM production_plan WHERE ID = '%s'" %(po_number)
            cur.execute(statement)
            mydb.commit()
            print("Production order", po_number, "has been removed")

def check_dayily_qty():
    miranti, alenti = 0,0
    date = valid_date()
    statement = "SELECT * FROM production_plan WHERE productiondate = '%s'" %(date)
    cur.execute(statement)
    table = cur.fetchall()
    print_table(table)
    for i in range(0, len(table)):
        if table[i][1] == "miranti":
            miranti = miranti + table[i][4]
        elif table[i][1] == "alenti":
            alenti = alenti + table[i][4]
    return miranti, alenti

def utilization():
    """Calculation of production capacity utilization"""
    miranti, alenti = check_dayily_qty()
    print("Utilization of production capacity for MIRANTI line: ", round(miranti/M*100), "%")
    print("Utilization of production capacity for ALENTI line: ", round(alenti/A*100), "%")
    
def get_BOM(name, qty):
    qty = qty
    product = name
    statement = "SELECT id, partid, qty * '%s' FROM %s" %(qty, product)
    cur.execute(statement)
    bom = cur.fetchall()
    x = prettytable.PrettyTable()
    x.field_names = ["Id", "Item", "Quantity"]
    for i in range(0, len(bom)):
        x.add_row([bom[i][0], bom[i][1], bom[i][2]])
    print("\nItems need on production for %s:\n" %(str(product)))
    print(x.get_string())
    
def items_warehouse():
    """Check and show table with items need on production line"""
    miranti, alenti = check_dayily_qty()
    get_BOM("miranti",miranti)
    get_BOM("alenti", alenti)
    
def full_list():
    """Create list of all items need on production line for chosen day"""
    miranti, alenti = check_dayily_qty()
    statement = "SELECT partid, sum(quantity) FROM (SELECT partid, qty*'%s' as quantity FROM miranti UNION ALL SELECT partid, qty*'%s'  as quantity FROM alenti) as subq GROUP BY partid ORDER BY partid" %(miranti, alenti)
    cur.execute(statement)
    daily_list = cur.fetchall()
    x = prettytable.PrettyTable()
    x.field_names = ["Id", "Item", "Quantity"]
    for i in range(0, len(daily_list)):
        x.add_row([i+1, daily_list[i][0], daily_list[i][1]])
    print("\nItems need on production for chosen day:\n")
    print(x.get_string())
    
    
def menu():
    print("""
    Menu:\n
    1 - New PO
    2 - Delete PO
    3 - Check production plan  
    4 - List of items need on produsction
    5 - Create list for warehouse
    6 - Close
    
    """)

    menu_choice = int(input("Insert option: "))
    return menu_choice

def main():
    menu_choice = 0
    while menu_choice != 6:
        menu_choice = menu()   
        if menu_choice == 1:
            add_po()         
        elif menu_choice == 2:
            delete_po()
        elif menu_choice == 3:
            utilization()
        elif menu_choice == 4:
            items_warehouse()
        elif menu_choice == 5:
            full_list()
        elif menu_choice == 6:
            print("END")
        else:
            print("Wrong number")

main()
