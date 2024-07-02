import sqlite3

def get_all_bank_cutomers():
    db = sqlite3.connect("Bank_DB.sqlite")
    db.execute("create table if not exists bank_customer_records(account_number integer, name text, pan_card text, age integer, account_type text, amount integer, email text, otp text)")
    db.commit()
    cursor = db.cursor()
    query = f"select account_number, name, pan_card, age, account_type, amount, email from bank_customer_records"
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()
    db.close()
    return record

data = get_all_bank_cutomers()

print("\t\t\t\t\t\t\tBankWithUs\n")
print("+--------------\t\t----\t\t-------\t\t---\t\t------------\t\t------\t\t----+")
print("Acccount Number\t\tName\t\tPancard\t\tAge\t\tAccount Type\t\tAmount\t\tEmail")
print("+--------------\t\t----\t\t-------\t\t---\t\t------------\t\t------\t\t----+")

for customer in data:
    for customer_entry in customer:
        print(customer_entry,end="\t\t")
    print()

print("+--------------\t\t----\t\t-------\t\t---\t\t------------\t\t------\t\t----+")