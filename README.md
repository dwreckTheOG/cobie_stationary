---

# Online Stationery Inventory Management System

This project is an **Online Stationery Inventory Management System** designed for **Cobie Books & Stationers**. The system aims to streamline the process of ordering and managing stationery by allowing customers to browse, order, and pay online. Administrators and managers can manage inventory, update products, and track orders. The project was developed as part of an IT system proposal for a diploma course at **Jomo Kenyatta University of Agriculture and Technology**.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Development Approach](#development-approach)
- [License](#license)

## Introduction
The **Online Stationery Inventory Management System** addresses the inefficiencies of manual stationery ordering and stock management at **Cobie Books & Stationers**. By shifting to an online platform, the system reduces errors, improves record-keeping, and provides real-time visibility into product availability. Customers can place orders, and admins can efficiently manage stock levels.

The system is based on the **Rapid Application Development (RAD)** model, focusing on fast prototyping and iterative development to meet business needs.

## Features
- **Customer Features**:
  - User registration and login.
  - Browse available stationery products.
  - Add products to the cart and place orders.
  - View and track order history.
  - Payment on delivery or through integrated online gateways.
  
- **Admin Features**:
  - Manage users (add, update, delete).
  - Add, update, or remove products from the inventory.
  - View and manage orders placed by customers.
  - Generate reports on sales and inventory levels.

## Technologies Used
- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript (with optional jQuery for UI enhancements)
- **Authentication and Authorization**: Active Directory Naming Services (ADNS)
- **Development Tools**: Sublime Text, Adobe Photoshop (for design assets)
- **Database**: SQLite (or MySQL for production)
- **Platform Requirements**:
  - Operating System: Windows 7 or above
  - Web Browser: Google Chrome, Mozilla Firefox
  - Minimum Hardware: 1.6GHz Processor, 4GB RAM, 500GB Hard Disk

## Installation
To install and run the project on your local machine:

### Prerequisites
- Python 3.x installed.
- Flask and other dependencies installed (use `requirements.txt`).
- A web browser (e.g., Google Chrome).

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/stationery-inventory-management.git
    cd stationery-inventory-management
    ```

2. **Set up the virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    - Initialize the SQLite database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. **Run the application**:
    ```bash
    flask run
    ```

6. **Access the application**:
    Open `http://127.0.0.1:5000` in your browser.

7. **Admin Login**:
    - Use the default admin credentials (can be changed after logging in):
      - Username: `admin`
      - Password: `admin123`

## Usage

### Customer Workflow
1. **Register/Login**: Users can create an account or log in.
2. **Browse Products**: View the list of available stationery products.
3. **Add to Cart**: Select products and add them to the cart.
4. **Checkout**: Place the order, confirm the delivery address, and choose the payment method.
5. **Track Orders**: Customers can view the status of their placed orders.

### Admin Workflow
1. **Login**: Admins log in with their credentials.
2. **Manage Products**: Add new products, update details, or delete items.
3. **View Orders**: Track all customer orders and their statuses.
4. **Generate Reports**: Admins can view sales and inventory reports.

## Database Schema
Here’s a summary of the key database tables:

- **Users**:
  - `user_id`: Primary key
  - `username`, `email`, `password`, `address`, `phone_number`
  
- **Products**:
  - `product_id`: Primary key
  - `product_name`, `price`, `description`, `stock`, `image`
  
- **Orders**:
  - `order_id`: Primary key
  - `user_id`: Foreign key from Users
  - `order_date`, `total_amount`, `order_status`
  
- **Order_Items**:
  - `order_item_id`: Primary key
  - `order_id`: Foreign key from Orders
  - `product_id`: Foreign key from Products
  - `quantity`, `price`

## Development Approach
The project follows the **Rapid Application Development (RAD)** methodology to ensure:
- **Fast Prototyping**: Initial versions were quickly built and tested.
- **User Involvement**: Feedback from users was incorporated throughout the development process.
- **Modularity**: The system was divided into modules like user management, product management, and order processing for easier updates.

### RAD Phases:
1. **Analysis**: Understanding the business requirements at Cobie Books & Stationers.
2. **Design**: Developing user interfaces and system architecture.
3. **Development**: Coding in Flask (Python3) and integrating with the SQLite database.
4. **Testing**: Ensuring all system components work as expected.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
