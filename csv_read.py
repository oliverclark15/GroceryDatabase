
import csv
import random
from random import randrange
from datetime import timedelta
from datetime import datetime

TABLE_LIST = {"users.csv":"User","payment_method.csv":"Payment_History","stock_products.csv":"Stock_Product"}

TABLE_DICT = {"users.csv":["user_id","password","status","email","first_name","last_name"], "payment_method.csv":["payment_id","type","card_number","expiry_date","billing_address","city","province","postal_code"], "stock_products.csv":["product_id","name","units_available","price_per_unit"]}
DEFAULT = 0
FILE_NAME = ""
CONVERTED_LIST = []
NUM_PROVIDERS = 40
TODAY = datetime.now()
YEAR_AGO = TODAY - timedelta(days=365)
MONTH_AGO = TODAY - timedelta(days=30)



global f

class Table:
    def __init__(self,type):
        self.rows = []
        self.table_name = type
        self.unique_keys = []
        self.commands = []

    def add_unit_row(self, r):
        self.rows.append(r)

    def print_contents(self):
        for row in self.rows:
            print(row)

    def add_column(self,list):
        for row in self.rows:
            row.append(random.choice(list))

    def print_sql(self):
        t_commands = self.commands
        for comm in t_commands:
            print(comm)

    def translate_to_SQL(self):
        temp_command = ""
        for row in self.rows:
            temp_command = ""
            for value in row:
                #value = value.replace(","," ")
                #value = value.replace("  "," ")
                if any(x.isalpha() for x in value):
                    value = "'" + value + "'"
                temp_command += value + ","
            temp_command = temp_command[:-1]
            self.commands.append("INSERT INTO " + self.table_name + "\nValues (" + temp_command + ");")

    def get_unique_keys(self):
        for row in self.rows:
            if (self.table_name == "User"):         #Remove from unique keys USER ID if not status 1 (for payment saves)
                if (row[2] == "1"):
                    self.unique_keys.append(row[0])
            else:
                self.unique_keys.append(row[0])



class Row:
    def __init__(self,row_temp):
        self.row = row_temp


def read_in():
    global f
    unit_row = {}
    empty_list = []
    for key,value in TABLE_LIST.items():
        FILE_NAME = key
        f = open(FILE_NAME, 'r')
        print("Opening :"+FILE_NAME)
        reader = csv.DictReader(f)
        temp_table = Table(value)
        for row in reader:
            unit_row.clear()
            for unit in (TABLE_DICT[FILE_NAME]):
                column_data = row.get(unit, DEFAULT)
                unit_row[unit] = column_data
            alt_row = list(unit_row.values())
            temp_table.add_unit_row(alt_row)
        #temp_table.print_contents()
        #temp_table.translate_to_SQL()
        CONVERTED_LIST.append(temp_table)
        f.close()
    print(CONVERTED_LIST)

def write_out():
    for table in CONVERTED_LIST:
        t_name = table.table_name
        t_name += ".csv"
        with open(t_name, 'w') as csvfile:
            writer_m = csv.writer(csvfile, dialect = 'excel')
            for row in table.rows:
                writer_m.writerow(row)




  #  with open('eggs.csv', 'wb') as csvfile:
   #     spamwriter = csv.writer(csvfile, delimiter=' ',
     #                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
      #  spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
   #     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
def unique_keys():
    for table in CONVERTED_LIST:
        table.get_unique_keys()

def create_payment_save():
    payment_saves = Table("Payment_Save")
    t1 = CONVERTED_LIST[0]
    t2 = CONVERTED_LIST[1]
    t_unique_1 = t1.unique_keys
    t_unique_2 = t2.unique_keys
    for user in t_unique_1:
        random_card = random.choice(t_unique_2)
        pair = [random_card,user]
        payment_saves.add_unit_row(pair)
    #payment_saves.print_contents()
    CONVERTED_LIST.append(payment_saves)
    #s


def create_carts():
    carts = Table("Cart")
    user_dict = {}
    num_carts = 0
    pm_user_pair = CONVERTED_LIST[3].rows
    print(pm_user_pair)
    # Each user may have a currently active cart, leaving the rest as 'historical' carts
    print(len(pm_user_pair))
    num_history_carts = 375
    print(num_history_carts)
    t_date = YEAR_AGO
    # Creating the historical carts
    while num_carts < num_history_carts:
        random_pu_pair = random.choice(pm_user_pair)
        h_user = random_pu_pair[1]
        h_payment = random_pu_pair[0]
        cart_counter = random.randint(1,4)
        t_date = YEAR_AGO
        for i in range (1,cart_counter):
            num_carts += 1
            temp = user_dict.get(h_user,-1)
            if (temp > 0):
                cart_id = temp + 1
            else:
                cart_id = 1
            user_dict[h_user] = cart_id
            date = random_date(t_date,TODAY)
            t_date = date
            date = ((str(date))[:10])
            information = [str(h_user), str(cart_id),str(h_payment), date,]
            carts.add_unit_row(information)
    while num_carts < 500:
        random_pu_pair = random.choice(pm_user_pair)
        h_user = random_pu_pair[1]
        temp = user_dict.get(h_user, -1)
        if (temp > 0):
            cart_id = temp + 1
        else:
            cart_id = 1
        date = random_date(MONTH_AGO, TODAY)
        date = ((str(date))[:10])
        information = [str(h_user), str(cart_id),'Null', date,]
        carts.add_unit_row(information)
        num_carts += 1
        user_dict[h_user] = cart_id
    # carts.print_contents()
    CONVERTED_LIST.append(carts)


def create_cart_lists():
    cart_lists = Table("Cart_List")
    cart_info = CONVERTED_LIST[4].rows
    product_info = CONVERTED_LIST[2].rows
    item_list = []
    for cart in cart_info:
        user = cart[0]
        cart_no = cart[3]
        information = [user, cart_no]
        number_of_items = random.randint(1,30)
        running_cost = 0
        for i in range(1, 30):
            if i > number_of_items:
                information.append('0')
            else:
                random_item = random.choice(product_info)
                r_name = random_item[1]
                ppu = float(random_item[3])
                quantity = random.uniform(1.0,4.2)
                cost = ppu * quantity
                running_cost += cost
                quantity = "{0:.2f}".format(quantity)
                cost = "{0:.2f}".format(cost)
                t_info = r_name +","+str(quantity) +","+ str(cost)
                information.append(t_info)
        running_cost = "{0:.2f}".format(running_cost)
        information.insert(2, running_cost)
        cart_lists.add_unit_row(information)
    CONVERTED_LIST.append(cart_lists)
        #cart_lists.print_contents()

def create_stock_providers():
    stock_providers = Table("Stock_Providers")
    stock_info = CONVERTED_LIST[3].rows
    day_list = ['M ','Tu ','W ','Th ','F']

    for i in range (0,NUM_PROVIDERS):
        z = 0
        rand = random.randint(1, 31)
        string = ""
        for z in range(0,4):
            temp = 2**z
            if rand & temp:
                string += (day_list[z])
        prov_num = random.randint(1000,9999)
        information = [str(prov_num), string]
        stock_providers.add_unit_row(information)
    CONVERTED_LIST.append(stock_providers)


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


read_in()
unique_keys()
create_payment_save()
create_carts()
print(TODAY)
print(YEAR_AGO)
create_cart_lists()
create_stock_providers()
unique_keys()
temp = CONVERTED_LIST[6].unique_keys
print(temp)
print(len(CONVERTED_LIST))
for table in CONVERTED_LIST:
    print(table.table_name)
    if table.table_name == "Stock_Product":
        table.add_column(temp)
    table.print_contents()
    #table.translate_to_SQL()
    #table.print_sql()

write_out()


