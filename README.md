# Procure-to-Pay (P2P) ERP System
### Capstone Project | KIIT SAP Batch

A full-stack web application simulating a **Procure-to-Pay ERP workflow** built with Python (Flask) backend and HTML/CSS/JavaScript frontend.

---

## Features

| Module | Capabilities |
|--------|-------------|
| **Dashboard** | KPI stats, recent POs, quick navigation |
| **Vendor Management** | Add / delete vendors, category & status tracking |
| **Purchase Orders** | Create POs, update status (Pending → In Transit → Received) |
| **Invoice Management** | View invoices, mark invoices as paid |
| **Inventory** | Track stock, low-stock alerts, add items |

---

## Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Data:** JSON file-based storage (`data.json`)
- **Icons:** Font Awesome 6

---

## Project Structure

```
capstone_project/
├── app.py                  # Flask application & REST API routes
├── requirements.txt        # Python dependencies
├── data.json               # Auto-generated data store
├── templates/
│   ├── base.html           # Base layout with sidebar
│   ├── index.html          # Dashboard
│   ├── vendors.html        # Vendor management
│   ├── purchase_orders.html
│   ├── invoices.html
│   └── inventory.html
└── static/
    ├── css/style.css       # All styles
    └── js/main.js          # Modal helpers
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask server
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Dashboard stats |
| GET/POST | `/api/vendors` | List / add vendors |
| DELETE | `/api/vendors/<id>` | Remove a vendor |
| GET/POST | `/api/purchase-orders` | List / create POs |
| PATCH | `/api/purchase-orders/<id>/status` | Update PO status |
| GET | `/api/invoices` | List invoices |
| PATCH | `/api/invoices/<id>/pay` | Mark invoice paid |
| GET/POST | `/api/inventory` | List / add inventory items |

---

## Student Details

- **Name:** ___________________
- **Roll Number:** ___________________
- **Batch/Program:** ___________________

---

*Submitted for KIIT Capstone Project — April 2026*
