
import csv
import random
TABLE_LIST = {"users.csv":"User","payment_method.csv":"Payment Method","stock_products.csv":"Stock Product"}

TABLE_DICT = {"users.csv":["user_id","password","status","email","first_name","last_name"], "payment_method.csv":["payment_id","type","card_number","expiry_date","billing_address","city","province","postal_code"], "stock_products.csv":["product_id","name","units_available","price_per_unit"]}
DEFAULT = 0
FILE_NAME = ""
CONVERTED_LIST = []

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

    def print_sql(self):
        t_commands = self.commands
        for comm in t_commands:
            print(comm)

    def translate_to_SQL(self):
        temp_command = ""
        for row in self.rows:
            temp_command = ""
            for value in row:
                value = value.replace(","," ")
                value = value.replace("  "," ")
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
        print(self.unique_keys)


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

def unique_keys():
    for table in CONVERTED_LIST:
        table.get_unique_keys()

def create_payment_save():
    payment_saves = Table("Payment Save")
    t1 = CONVERTED_LIST[0]
    t2 = CONVERTED_LIST[1]
    t_unique_1 = t1.unique_keys
    t_unique_2 = t2.unique_keys
    for key in t_unique_2:
        random_user = random.choice(t_unique_1)
        pair = [key, random_user]
        payment_saves.add_unit_row(pair)
    #payment_saves.print_contents()
    CONVERTED_LIST.append(payment_saves)


read_in()
unique_keys()
#create_payment_save()
for table in CONVERTED_LIST:
    table.translate_to_SQL()
    table.print_sql()


