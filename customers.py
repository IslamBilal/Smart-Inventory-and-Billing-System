"""Customer data access operations for the inventory application."""
from Database import conn


class Customer:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    @staticmethod
    def create_table():
        cur = conn.cursor()
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                contact VARCHAR(100) NOT NULL
            )""")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def insert_customer(name, contact):
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO customers (name, contact) VALUES (%s, %s)",
                (name, contact),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def update_customer(customer_id, name=None, contact=None):
        updates = []
        values = []
        if name is not None:
            updates.append("name = %s")
            values.append(name)
        if contact is not None:
            updates.append("contact = %s")
            values.append(contact)
        if not updates:
            return False

        cur = conn.cursor()
        try:
            values.append(customer_id)
            cur.execute(
                f"UPDATE customers SET {', '.join(updates)} WHERE id = %s",
                tuple(values),
            )
            updated = cur.rowcount > 0
            conn.commit()
            return updated
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def delete_customer(customer_id):
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def get_all_customers():
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM customers ORDER BY id")
            return cur.fetchall()
        finally:
            cur.close()

    @staticmethod
    def view_customers():
        for customer in Customer.get_all_customers():
            print(customer)

    @staticmethod
    def view_customer_by_id(customer_id):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            customer = cur.fetchone()
            print(customer if customer else "Customer not found")
            return customer
        finally:
            cur.close()

    @staticmethod
    def get_sales_by_customer(customer_id):
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT s.id, s.date, s.total_amount FROM sales s
                   WHERE s.customer_id = %s ORDER BY s.date DESC""",
                (customer_id,),
            )
            sales = cur.fetchall()
            for sale in sales:
                print(sale)
            return sales
        finally:
            cur.close()

    @staticmethod
    def search_customer(name):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM customers WHERE name ILIKE %s", (f"%{name}%",))
            customers = cur.fetchall()
            for customer in customers:
                print(customer)
            return customers
        finally:
            cur.close()

    @staticmethod
    def customer_menu():
        while True:
            print("1. Create Table\n2. Insert Customer\n3. Update Customer\n4. Delete Customer")
            print("5. View Customers\n6. View Customer by ID\n7. Get Sales by Customer\n8. Search Customer\n0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                Customer.create_table()
                print("Table created")
            elif choice == "2":
                Customer.insert_customer(input("Enter customer name: ").strip(), input("Enter customer contact: ").strip())
                print("Customer inserted")
            elif choice == "3":
                customer_id = int(input("Enter customer id: "))
                name = input("Enter customer name (blank to keep current): ").strip()
                contact = input("Enter customer contact (blank to keep current): ").strip()
                Customer.update_customer(customer_id, name or None, contact or None)
                print("Customer update processed")
            elif choice == "4":
                Customer.delete_customer(int(input("Enter customer id: ")))
                print("Customer deletion processed")
            elif choice == "5":
                Customer.view_customers()
            elif choice == "6":
                Customer.view_customer_by_id(int(input("Enter customer id: ")))
            elif choice == "7":
                Customer.get_sales_by_customer(int(input("Enter customer id: ")))
            elif choice == "8":
                Customer.search_customer(input("Enter customer name: ").strip())
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
