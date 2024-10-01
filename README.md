---

# Herbal Ordering System

The **Herbal Ordering System** is an online platform that allows customers to browse, order, and pay for herbal products. The system is built using Flask (Python) for the backend and is designed to simplify the process of ordering herbs while providing an easy-to-use interface for both customers and administrators.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## Features
- **User Registration & Login**: Customers can sign up, log in, and manage their accounts.
- **Product Browsing**: Customers can view available herbal products, including descriptions and prices.
- **Cart Management**: Customers can add products to a cart and modify their orders.
- **Order Placement**: Customers can place orders and track their status.
- **Admin Panel**: Administrators can manage products, view orders, and manage users.
- **Payment Integration**: Integrated online payment system for secure transactions.
- **Responsive Design**: Optimized for both desktop and mobile users.

## Technologies Used
- **Backend**: Python 3 with Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (or MySQL, depending on your setup)
- **Payment Gateway**: (e.g., Stripe, PayPal - update according to your implementation)
- **Others**: Jinja2 (for templating), Flask-WTF (for forms), Flask-Login (for user sessions)

## Installation
To set up the project locally, follow these steps:

### Prerequisites
- Python 3.x
- pip (Python package manager)
- (Optional) Virtual environment tool, like `venv`

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/herbal-ordering-system.git
    cd herbal-ordering-system
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the environment variables**:
    Create a `.env` file in the root directory and add the following keys (update values accordingly):
    ```
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///site.db  # or mysql+pymysql://username:password@localhost/db_name for MySQL
    ```

5. **Initialize the database**:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. **Run the application**:
    ```bash
    flask run
    ```

7. **Access the application**:
    Open `http://127.0.0.1:5000` in your browser.

## Usage
- **Customer**: 
  - Sign up/log in to view available products.
  - Add products to the cart.
  - Proceed to checkout and make a payment.
  - View order history and track delivery status.
  
- **Admin**: 
  - Log in to the admin panel.
  - Add, update, or delete herbal products.
  - View all customer orders and manage them.

## Database Schema
Here’s a brief overview of the database tables:

- **Users**: Stores user details (name, email, password).
- **Products**: Stores product details (name, price, description, stock).
- **Orders**: Tracks orders placed by customers (order status, payment details).
- **Order_Items**: Holds information about products in each order (order ID, product ID, quantity).

## Contributing
We welcome contributions! Here's how you can help:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
