"""Sale item operations with inventory and sale-total consistency."""
from Database import conn


class SaleItem:
    def __init__(self, sale_id, product_id, quantity, price):
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    @staticmethod
    def create_table():
        cur = conn.cursor()
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price DECIMAL(10, 2) NOT NULL CHECK (price >= 0)
            )""")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def add_item(sale_id, product_id, quantity, price):
        quantity = int(quantity)
        price = float(price)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM sales WHERE id = %s FOR UPDATE", (sale_id,))
            if cur.fetchone() is None:
                raise ValueError("Sale was not found.")

            cur.execute("SELECT quantity FROM products WHERE id = %s FOR UPDATE", (product_id,))
            product = cur.fetchone()
            if product is None:
                raise ValueError("Product was not found.")
            if product[0] < quantity:
                raise ValueError("Insufficient stock for the requested quantity.")

            cur.execute(
                "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (sale_id, product_id, quantity, price),
            )
            cur.execute(
                "UPDATE products SET quantity = quantity - %s WHERE id = %s",
                (quantity, product_id),
            )
            cur.execute(
                "UPDATE sales SET total_amount = total_amount + %s WHERE id = %s",
                (quantity * price, sale_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def get_items_by_sale(sale_id):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sale_items WHERE sale_id = %s ORDER BY id", (sale_id,))
            return cur.fetchall()
        finally:
            cur.close()

    @staticmethod
    def view_sale_items(sale_id):
        items = SaleItem.get_items_by_sale(sale_id)
        total_amount = 0
        for item in items:
            print(item)
            total_amount += item[3] * item[4]
        print("Total Amount for Sale ID", sale_id, ":", total_amount)
        return total_amount

    @staticmethod
    def sale_item_menu():
        while True:
            print("1. Add Item to Sale\n2. View Sale Items\n0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                SaleItem.add_item(
                    int(input("Enter sale id: ")),
                    int(input("Enter product id: ")),
                    int(input("Enter quantity: ")),
                    float(input("Enter price: ")),
                )
                print("Item added and inventory updated")
            elif choice == "2":
                SaleItem.view_sale_items(int(input("Enter sale id: ")))
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
