# 🛍️ Django E-commerce Web Application

A fully functional e-commerce web application built using **Django**, **HTML**, **CSS**, and **JavaScript**. 
This project supports user authentication, product browsing, cart management, order placement, and payment integration.

---

## 🚀 Features

### 👤 User Features

* User Signup & Login (Email / Phone)
* Secure password hashing
* Profile management with multiple addresses
* Session-based authentication

### 🛒 Shopping Features

* Browse products & categories
* Search products with suggestions
* Like / Wishlist products ❤️
* Add to cart & manage quantity
* Buy Now & Cart-based checkout

### 📦 Order Management

* Place orders using:

  * Cash on Delivery (COD)
  * Online Payment (Razorpay integration)
* View Order History
* Order Success Page

### 💳 Payment Integration

* Razorpay payment gateway integration
* Order creation via API

### 🔍 Search System

* Dynamic search suggestions
* Product & category search

### 🧑‍💼 Admin Features

* Add Categories
* Add Products with:

  * Main Image
  * Multiple Extra Images

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite3
* **Payment Gateway:** Razorpay
* **Storage:** Django Default Storage

---

## 📁 Project Structure

```
ecommerce/
│
├── models.py
├── views.py
├── templates/
├── static/
├── media/
└── db.sqlite3
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Akash-Patnamsetty/django-saree-ecommerce.git
cd django-saree-ecommerce
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Run server

```bash
python manage.py runserver
```

---

## 🔑 Important Notes

* Razorpay test keys are used in development.
* Replace with your own keys in production.
* Media files are stored locally using Django default storage.

---

## 📸 Screenshots

(Add your project screenshots here)

---

## 🎯 Future Improvements

* Add JWT authentication
* Add product reviews & ratings
* Improve UI/UX design
* Add pagination & filters
* Deploy on cloud (AWS / Render)

---

## 🙋‍♂️ Author

**Akash Patnamsetty**
B.Tech CSE Student | Aspiring Full Stack Developer & ML Engineer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
