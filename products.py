"""Product data access operations for the inventory application."""
from Database import conn


class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @staticmethod
    def create_table():
        cur = conn.cursor()
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
                quantity INTEGER NOT NULL CHECK (quantity >= 0)
            )""")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def insert_product(name, description, price, quantity):
        if float(price) < 0 or int(quantity) < 0:
            raise ValueError("Price and quantity cannot be negative.")
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
                (name, description, price, quantity),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def update_product(product_id, name=None, description=None, price=None, quantity=None):
        updates = []
        values = []
        if name is not None:
            updates.append("name = %s")
            values.append(name)
        if description is not None:
            updates.append("description = %s")
            values.append(description)
        if price is not None:
            if float(price) < 0:
                raise ValueError("Price cannot be negative.")
            updates.append("price = %s")
            values.append(price)
        if quantity is not None:
            if int(quantity) < 0:
                raise ValueError("Quantity cannot be negative.")
            updates.append("quantity = %s")
            values.append(quantity)
        if not updates:
            return False

        cur = conn.cursor()
        try:
            values.append(product_id)
            cur.execute(
                f"UPDATE products SET {', '.join(updates)} WHERE id = %s",
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
    def delete_product(product_id):
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    @staticmethod
    def view_products():
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products ORDER BY id")
            return cur.fetchall()
        finally:
            cur.close()

    @staticmethod
    def view_product_id(product_id):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return cur.fetchone()
        finally:
            cur.close()

    @staticmethod
    def product_menu():
        while True:
            print("1. Create Table\n2. Insert Product\n3. Update Product\n4. Delete Product\n5. View Products\n6. View Product by ID\n0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                Product.create_table()
                print("Table created")
            elif choice == "2":
                name = input("Enter product name: ").strip()
                description = input("Enter product description: ").strip()
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Product.insert_product(name, description, price, quantity)
                print("Product inserted")
            elif choice == "3":
                product_id = int(input("Enter product id: "))
                name = input("Enter product name: ").strip()
                description = input("Enter product description: ").strip()
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Product.update_product(product_id, name, description, price, quantity)
                print("Product update processed")
            elif choice == "4":
                Product.delete_product(int(input("Enter product id: ")))
                print("Product deletion processed")
            elif choice == "5":
                for product in Product.view_products():
                    print(product)
            elif choice == "6":
                print(Product.view_product_id(int(input("Enter product id: "))))
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
