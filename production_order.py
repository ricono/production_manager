import datetime

class PO():
    """Production order"""

    def __init__(self, ponumber, product, production_date, qty):
        self.ponumber = ponumber
        self.product = product
        self.production_date = production_date
        self.order_date = datetime.date.today()
        self.qty = qty
        print("PO %s has been created" %str(ponumber))

    def show_info(self):
        print("PO number: " + str(self.ponumber))
        print("Product: " + self.product)
        print("Production date: " + str(self.production_date))
        print("Quantity: " + str(self.qty))
        print("Date of order: " + str(self.order_date))


        
    
