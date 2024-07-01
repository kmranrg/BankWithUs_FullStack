import sqlite3

def insert_into_db(customer_values):

    db = sqlite3.connect("Bank_DB.sqlite")

    db.execute("create table if not exists bank_customer_records(account_number integer, name text, pan_card text, age integer, account_type text, amount integer, email text, otp text)")

    db.execute("insert into bank_customer_records values(?,?,?,?,?,?,?,?)",customer_values)
    db.commit()
    db.close()

def search_account_number_in_db(account_number):
    db = sqlite3.connect("Bank_DB.sqlite")
    db.execute("create table if not exists bank_customer_records(account_number integer, name text, pan_card text, age integer, account_type text, amount integer, email text, otp text)")
    db.commit()
    cursor = db.cursor()
    query = f"select * from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()
    status = ''

    if len(record) == 0:
        status = "Account not present in the database"
    else:
        status =  "Account Exists"
    
    cursor.close()
    db.close()
    return status

def get_account_balance(account_number):
    db = sqlite3.connect("Bank_DB.sqlite")
    cursor = db.cursor()
    query = f"select amount from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()
    db.close()
    return record[0][0]

def withdraw_from_account_balance(account_number, withdraw_amount):
    db = sqlite3.connect("Bank_DB.sqlite")
    cursor = db.cursor()
    query = f"select amount from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()

    new_account_balance = record[0][0] - withdraw_amount

    query = f"update bank_customer_records set amount = {new_account_balance} where account_number is {int(account_number)}"
    cursor.execute(query)
    db.commit()
    query = f"select amount from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()

    cursor.close()
    db.close()
    return record[0][0]

def deposit_to_account_balance(account_number, deposit_amount):
    db = sqlite3.connect("Bank_DB.sqlite")
    cursor = db.cursor()
    query = f"select amount from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()

    new_account_balance = record[0][0] + deposit_amount

    query = f"update bank_customer_records set amount = {new_account_balance} where account_number is {int(account_number)}"
    cursor.execute(query)
    db.commit()
    query = f"select amount from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()

    cursor.close()
    db.close()
    return record[0][0]

def get_details_to_send_mail(account_number):
    db = sqlite3.connect("Bank_DB.sqlite")
    cursor = db.cursor()
    query = f"select email, name from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()
    db.close()
    return record[0]

def update_otp(account_number, new_otp):
    db = sqlite3.connect("Bank_DB.sqlite")
    cursor = db.cursor()

    query = f"update bank_customer_records set otp = {new_otp} where account_number is {int(account_number)}"
    cursor.execute(query)
    db.commit()

    cursor.close()
    db.close()
    return

def get_otp_from_db(account_number):
    db = sqlite3.connect("Bank_DB.sqlite")
    cursor = db.cursor()
    query = f"select otp from bank_customer_records where account_number is {int(account_number)}"
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()
    db.close()
    return record[0][0]