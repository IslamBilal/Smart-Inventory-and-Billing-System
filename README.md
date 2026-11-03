# Smart Inventory and Billing System

A Python application for managing customers, products, stock, and sales. It includes a Streamlit web interface, a command-line interface, and a PostgreSQL database.

## Features

- **Dashboard:** Displays customer, product, and sales counts.
- **Customer management:** Create, view, update, search, and delete customers.
- **Product management:** Create, view, update, and delete products with prices and stock quantities.
- **Sales and billing:** Create sales, add sale items, and generate bills.
- **Inventory control:** Reduces stock when a sale item is added and checks that enough stock is available.
- **Analytics:** Sales summaries, date-range reports, top-selling products, low-stock alerts, and customer purchase history.
- **Two interfaces:** Streamlit web application and a terminal-based menu.

## Technology Stack

- Python 3.9+
- Streamlit
- PostgreSQL
- psycopg2
- python-dotenv
- SQL

## Project Structure

```text
Smart-Inventory-and-Billing-System/
├── app.py             # Streamlit application
├── main.py            # Command-line entry point
├── Database.py        # PostgreSQL connection configuration
├── customers.py       # Customer operations
├── products.py        # Product and inventory operations
├── sales.py           # Sales and reporting operations
├── sales_items.py     # Sale item and stock transaction logic
├── requirements.txt   # Python dependencies
├── .env.example       # Safe database configuration template
└── README.md
```

## Prerequisites

- Python 3.9 or later
- PostgreSQL installed and running
- A PostgreSQL database named `ecommerce`

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/IslamBilal/Smart-Inventory-and-Billing-System.git
cd Smart-Inventory-and-Billing-System
```

### 2. Create and activate a virtual environment

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a database named `ecommerce` in PostgreSQL. Copy the example configuration file:

Windows:
```powershell
Copy-Item .env.example .env
```

macOS/Linux:
```bash
cp .env.example .env
```

Edit `.env` with your local database settings:

- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`

The real `.env` file is ignored by Git. **Never commit database passwords or secrets.**

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

### 6. Run the command-line application

```bash
python main.py
```

The application creates the required tables when it starts. For a new database, start with the Streamlit application or use the table-creation options in the CLI.

## Database Tables

| Table | Purpose |
|---|---|
| `customers` | Customer names and contact information |
| `products` | Product details, prices, and available stock |
| `sales` | Sale date, customer, and total amount |
| `sale_items` | Products, quantities, and unit prices associated with a sale |

## Important Implementation Notes

- Customer and product update operations use parameterized SQL values.
- Sale-item insertion, stock reduction, and sale-total updates are handled in one database transaction.
- The application checks product availability before reducing inventory.
- Foreign-key and check constraints are included in the table definitions for newly created tables. Existing databases created with older table definitions may need a schema migration to gain those constraints.
- The database connection is currently shared by the imported modules. A connection pool or per-operation connection management would be a useful next architectural improvement.

## Limitations

- The project requires a locally configured PostgreSQL database.
- The Streamlit interface and CLI should be tested against a clean database before deployment.
- This is a learning project, not a production inventory or accounting platform.
- No automated test suite is currently included.

## Future Improvements

- Add automated unit and integration tests.
- Add database migrations for existing installations.
- Introduce connection pooling and stronger transaction boundaries for every workflow.
- Add user authentication and role-based permissions.
- Add exportable invoices and sales reports.
- Add screenshots and a short demo video.

## Author

**Mohammad Bilal**  
GitHub: [IslamBilal](https://github.com/IslamBilal)
