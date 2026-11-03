"""Sales operations and reporting queries."""
from Database import conn


class Sale:
    def __init__(self, customer_id, date, total_amount=0):
        self.customer_id = customer_id
        self.date = date
        self.total_amount = total_amount

    @staticmethod
    def create_table():
        cur = conn.cursor()
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
                date DATE NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0)
            )""")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def insert_sale(customer_id, date, total_amount=0):
        if float(total_amount) < 0:
            raise ValueError("Sale total cannot be negative.")
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO sales (customer_id, date, total_amount) VALUES (%s, %s, %s) RETURNING id",
                (customer_id, date, total_amount),
            )
            sale_id = cur.fetchone()[0]
            conn.commit()
            return sale_id
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def view_sales():
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales ORDER BY date DESC, id DESC")
            sales = cur.fetchall()
            for sale in sales:
                print(sale)
            return sales
        finally:
            cur.close()

    @staticmethod
    def view_sale_by_id(sale_id):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
            sale = cur.fetchone()
            print(sale if sale else "Sale not found")
            return sale
        finally:
            cur.close()

    @staticmethod
    def add_sale_items(sale_id, product_id, quantity, price):
        from sales_items import SaleItem
        return SaleItem.add_item(sale_id, product_id, quantity, price)

    @staticmethod
    def update_inventory(product_id, quantity_sold):
        quantity_sold = int(quantity_sold)
        if quantity_sold <= 0:
            raise ValueError("Quantity sold must be greater than zero.")
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE products SET quantity = quantity - %s WHERE id = %s AND quantity >= %s",
                (quantity_sold, product_id, quantity_sold),
            )
            if cur.rowcount == 0:
                raise ValueError("Product not found or insufficient stock.")
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def generate_bill(sale_id):
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT si.product_id, si.quantity, si.price, (si.quantity * si.price) AS line_total
                   FROM sale_items si WHERE si.sale_id = %s ORDER BY si.id""",
                (sale_id,),
            )
            sale_items = cur.fetchall()
            print("Bill for Sale ID:", sale_id)
            total_amount = 0
            for item in sale_items:
                print("Product ID:", item[0], "Quantity:", item[1], "Price:", item[2])
                total_amount += item[3]
            print("Total Amount:", total_amount)
            cur.execute("UPDATE sales SET total_amount = %s WHERE id = %s", (total_amount, sale_id))
            conn.commit()
            return total_amount
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def get_total_sales_by_date(start_date, end_date):
        cur = conn.cursor()
        try:
            cur.execute("SELECT COALESCE(SUM(total_amount), 0) FROM sales WHERE date BETWEEN %s AND %s", (start_date, end_date))
            return cur.fetchone()[0]
        finally:
            cur.close()

    @staticmethod
    def get_top_selling_products():
        cur = conn.cursor()
        try:
            cur.execute("""SELECT product_id, SUM(quantity) AS total_quantity
                           FROM sale_items GROUP BY product_id
                           ORDER BY total_quantity DESC LIMIT 5""")
            return cur.fetchall()
        finally:
            cur.close()

    @staticmethod
    def get_sales_by_customer(customer_id):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE customer_id = %s ORDER BY date DESC", (customer_id,))
            sales = cur.fetchall()
            for sale in sales:
                print(sale)
            return sales
        finally:
            cur.close()

    @staticmethod
    def sale_menu():
        while True:
            print("1. Create Table\n2. Insert Sale\n3. View Sales\n4. View Sale by ID")
            print("5. Add Sale Items\n6. Update Inventory\n7. Generate Bill\n8. Get Total Sales by Date")
            print("9. Get Top Selling Products\n10. Get Sales by Customer\n0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                Sale.create_table()
                print("Table created")
            elif choice == "2":
                Sale.insert_sale(int(input("Enter customer id: ")), input("Enter date (YYYY-MM-DD): "), float(input("Enter total amount: ")))
                print("Sale inserted")
            elif choice == "3":
                Sale.view_sales()
            elif choice == "4":
                Sale.view_sale_by_id(int(input("Enter sale id: ")))
            elif choice == "5":
                Sale.add_sale_items(int(input("Enter sale id: ")), int(input("Enter product id: ")), int(input("Enter quantity: ")), float(input("Enter price: ")))
                print("Sale item added and inventory updated")
            elif choice == "6":
                Sale.update_inventory(int(input("Enter product id: ")), int(input("Enter quantity sold: ")))
                print("Inventory updated")
            elif choice == "7":
                Sale.generate_bill(int(input("Enter sale id: ")))
            elif choice == "8":
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                print("Total sales:", Sale.get_total_sales_by_date(start_date, end_date))
            elif choice == "9":
                for product in Sale.get_top_selling_products():
                    print("Product ID:", product[0], "Total Quantity Sold:", product[1])
            elif choice == "10":
                customer_id = int(input("Enter customer id: "))
                for sale in Sale.get_sales_by_customer(customer_id):
                    print(sale)
                    print("Total Amount:", Sale.generate_bill(sale[0]))
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
