# InventoryGPT

AI-Powered Inventory Management System built with Flask, React, SQLite, JWT Authentication, and Google Gemini AI.

---

## Features

### Inventory Management

* Add Products
* Update Products
* Delete Products
* Stock In
* Stock Out
* Inventory Tracking

### Dashboard Analytics

* Total Products
* Inventory Value
* Transaction Statistics
* Low Stock Alerts
* Interactive Charts

### Purchase Orders

* Create Purchase Orders
* Approve Purchase Orders
* Automatic Inventory Updates

### Sales Management

* Sales Orders
* Customer Tracking
* Revenue Tracking

### Supplier Management

* Add Suppliers
* Manage Supplier Information

### Customer Management

* Customer Records
* Sales History

### AI Assistant

Powered by Google Gemini AI

* Inventory Questions
* Product Insights
* Business Analytics
* Inventory Recommendations

### Security

* JWT Authentication
* Role-Based Access
* Protected Routes

---

## Technology Stack

### Frontend

* React
* Vite
* React Router
* Chart.js

### Backend

* Flask
* SQLAlchemy
* Flask JWT Extended
* Alembic

### Database

* SQLite

### AI

* Google Gemini API

---

## Project Structure

InventoryGPT/

├── backend/

├── frontend/

├── README.md

└── .gitignore

---

## Installation

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

flask db upgrade

python app.py
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Create:

backend/.env

```env
GEMINI_API_KEY=your_api_key
JWT_SECRET_KEY=your_secret_key
```

---

## Screenshots

Dashboard

Products

Inventory Management

Purchase Orders

AI Assistant

---

## Future Enhancements

* Email Notifications
* Barcode Scanner
* Multi Warehouse Support
* Forecasting AI
* Demand Prediction
* Cloud Deployment

---

## Author

Dileep Biradha

GitHub:
https://github.com/Dileepbiradha
