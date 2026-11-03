# Smart Inventory and Billing System

A Python-based inventory and billing application with a Streamlit web interface and a PostgreSQL database. It provides management of customers, products, sales, and sale items, along with dashboard metrics and sales reporting.

## Features
- **Dashboard:** Displays total customers, products, and sales.
- **Customer management:** Add, view, update, and delete customer records.
- **Product management:** Add, view, update, and delete products, including price and stock quantity.
- **Sales management:** Record and view sales and generate bills from sale items.
- **Analytics:** Includes date-range sales totals, top-selling product queries, and sales-by-customer queries.
- **Two entry points:** A Streamlit interface (`app.py`) and a terminal menu (`main.py`).

## Technology Stack
- Python
- Streamlit
- PostgreSQL
- psycopg2
- SQL

## Project Structure
```text
Smart-Inventory-and-Billing-System/
├── app.py          # Streamlit web application and dashboard
├── main.py         # Command-line application entry point
├── Database.py     # PostgreSQL connection configuration
├── customers.py    # Customer table and CRUD operations
├── products.py     # Product table and CRUD operations
├── sales.py        # Sales operations, billing, and analytical queries
├── sales_items.py  # Sale-item operations
└── README.md
```

## Prerequisites
- Python 3.9 or later
- PostgreSQL installed and running
- A PostgreSQL database created for the application

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/IslamBilal/Smart-Inventory-and-Billing-System.git
   cd Smart-Inventory-and-Billing-System
   ```
2. Create and activate a virtual environment:
   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install streamlit psycopg2-binary
   ```
4. Create a PostgreSQL database (for example, `ecommerce`) and configure the connection settings in `Database.py` for your local host, database, username, password, and port.
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   Or run the command-line version:
   ```bash
   python main.py
   ```
The Streamlit application attempts to initialize the required tables when it starts.

## Database Tables
- `customers`: Customer names and contact information.
- `products`: Product names, descriptions, prices, and available quantities.
- `sales`: Customer reference, sale date, and total amount.
- `sale_items`: Sale reference, product reference, quantity, and unit price.

## Notes and Limitations
- The application expects a locally accessible PostgreSQL database; database setup is not automated.
- Configure database credentials locally. Do not commit real passwords, API keys, or other secrets to GitHub. Prefer environment variables or a local, untracked configuration file for credentials.
- The repository contains both a Streamlit interface and a separate command-line interface. Some operations and reporting functions may need further integration and testing.
- This README describes functionality visible in the repository; it does not claim that every workflow has been fully tested.

## Future Improvements
- Move database credentials to environment variables.
- Add database foreign-key constraints and stronger input validation.
- Use parameterized SQL for all update operations.
- Add automated tests and clearer error handling.
- Improve stock validation and transaction handling during billing.
- Add screenshots or a short demo of the Streamlit interface.

## Author
**Mohammad Bilal**
GitHub: [IslamBilal](https://github.com/IslamBilal)
