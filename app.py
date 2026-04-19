from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__)

# ─── In-memory data store (acts like a lightweight DB) ───────────────────────
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "vendors": [
            {"id": "V001", "name": "Alpha Supplies Pvt Ltd", "contact": "9876543210", "email": "alpha@supplies.com", "category": "Raw Materials", "status": "Active"},
            {"id": "V002", "name": "Beta Tech Solutions",    "contact": "9812345670", "email": "beta@tech.com",     "category": "IT Equipment",   "status": "Active"},
            {"id": "V003", "name": "Gamma Logistics",        "contact": "9754321098", "email": "gamma@logist.com",  "category": "Logistics",       "status": "Inactive"},
        ],
        "purchase_orders": [
            {"id": "PO-001", "vendor_id": "V001", "vendor_name": "Alpha Supplies Pvt Ltd", "item": "Steel Rods",       "qty": 500, "unit_price": 120, "total": 60000,  "date": "2026-04-01", "status": "Received"},
            {"id": "PO-002", "vendor_id": "V002", "vendor_name": "Beta Tech Solutions",    "item": "Laptops",          "qty": 10,  "unit_price": 45000, "total": 450000, "date": "2026-04-05", "status": "Pending"},
            {"id": "PO-003", "vendor_id": "V001", "vendor_name": "Alpha Supplies Pvt Ltd", "item": "Copper Wire",      "qty": 200, "unit_price": 350,  "total": 70000,  "date": "2026-04-10", "status": "In Transit"},
        ],
        "invoices": [
            {"id": "INV-001", "po_id": "PO-001", "vendor_name": "Alpha Supplies Pvt Ltd", "amount": 60000,  "due_date": "2026-04-20", "status": "Paid"},
            {"id": "INV-002", "po_id": "PO-003", "vendor_name": "Alpha Supplies Pvt Ltd", "amount": 70000,  "due_date": "2026-04-28", "status": "Unpaid"},
        ],
        "inventory": [
            {"id": "ITM-001", "name": "Steel Rods",   "category": "Raw Materials", "qty": 500, "unit": "pcs",  "reorder_level": 100, "warehouse": "WH-A"},
            {"id": "ITM-002", "name": "Copper Wire",  "category": "Raw Materials", "qty": 200, "unit": "mtrs", "reorder_level": 50,  "warehouse": "WH-A"},
            {"id": "ITM-003", "name": "Laptops",      "category": "IT Equipment",  "qty": 0,   "unit": "pcs",  "reorder_level": 5,   "warehouse": "WH-B"},
        ]
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─── Pages ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vendors")
def vendors_page():
    return render_template("vendors.html")

@app.route("/purchase-orders")
def po_page():
    return render_template("purchase_orders.html")

@app.route("/invoices")
def invoices_page():
    return render_template("invoices.html")

@app.route("/inventory")
def inventory_page():
    return render_template("inventory.html")

# ─── API: Dashboard ───────────────────────────────────────────────────────────
@app.route("/api/dashboard")
def api_dashboard():
    data = load_data()
    total_po_value = sum(p["total"] for p in data["purchase_orders"])
    unpaid_invoices = sum(i["amount"] for i in data["invoices"] if i["status"] == "Unpaid")
    low_stock = [i for i in data["inventory"] if i["qty"] <= i["reorder_level"]]
    return jsonify({
        "total_vendors": len(data["vendors"]),
        "active_vendors": len([v for v in data["vendors"] if v["status"] == "Active"]),
        "total_pos": len(data["purchase_orders"]),
        "pending_pos": len([p for p in data["purchase_orders"] if p["status"] == "Pending"]),
        "total_po_value": total_po_value,
        "unpaid_invoices": unpaid_invoices,
        "low_stock_count": len(low_stock),
        "recent_pos": data["purchase_orders"][-3:][::-1],
    })

# ─── API: Vendors ─────────────────────────────────────────────────────────────
@app.route("/api/vendors", methods=["GET"])
def api_vendors():
    data = load_data()
    return jsonify(data["vendors"])

@app.route("/api/vendors", methods=["POST"])
def add_vendor():
    data = load_data()
    body = request.json
    new_vendor = {
        "id": f"V{str(len(data['vendors'])+1).zfill(3)}",
        "name": body["name"],
        "contact": body["contact"],
        "email": body["email"],
        "category": body["category"],
        "status": "Active"
    }
    data["vendors"].append(new_vendor)
    save_data(data)
    return jsonify({"success": True, "vendor": new_vendor}), 201

@app.route("/api/vendors/<vid>", methods=["DELETE"])
def delete_vendor(vid):
    data = load_data()
    data["vendors"] = [v for v in data["vendors"] if v["id"] != vid]
    save_data(data)
    return jsonify({"success": True})

# ─── API: Purchase Orders ─────────────────────────────────────────────────────
@app.route("/api/purchase-orders", methods=["GET"])
def api_pos():
    data = load_data()
    return jsonify(data["purchase_orders"])

@app.route("/api/purchase-orders", methods=["POST"])
def add_po():
    data = load_data()
    body = request.json
    vendor = next((v for v in data["vendors"] if v["id"] == body["vendor_id"]), None)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    total = float(body["qty"]) * float(body["unit_price"])
    new_po = {
        "id": f"PO-{str(len(data['purchase_orders'])+1).zfill(3)}",
        "vendor_id": body["vendor_id"],
        "vendor_name": vendor["name"],
        "item": body["item"],
        "qty": int(body["qty"]),
        "unit_price": float(body["unit_price"]),
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Pending"
    }
    data["purchase_orders"].append(new_po)
    save_data(data)
    return jsonify({"success": True, "po": new_po}), 201

@app.route("/api/purchase-orders/<po_id>/status", methods=["PATCH"])
def update_po_status(po_id):
    data = load_data()
    body = request.json
    for po in data["purchase_orders"]:
        if po["id"] == po_id:
            po["status"] = body["status"]
            break
    save_data(data)
    return jsonify({"success": True})

# ─── API: Invoices ────────────────────────────────────────────────────────────
@app.route("/api/invoices", methods=["GET"])
def api_invoices():
    data = load_data()
    return jsonify(data["invoices"])

@app.route("/api/invoices/<inv_id>/pay", methods=["PATCH"])
def pay_invoice(inv_id):
    data = load_data()
    for inv in data["invoices"]:
        if inv["id"] == inv_id:
            inv["status"] = "Paid"
            break
    save_data(data)
    return jsonify({"success": True})

# ─── API: Inventory ───────────────────────────────────────────────────────────
@app.route("/api/inventory", methods=["GET"])
def api_inventory():
    data = load_data()
    return jsonify(data["inventory"])

@app.route("/api/inventory", methods=["POST"])
def add_inventory():
    data = load_data()
    body = request.json
    new_item = {
        "id": f"ITM-{str(len(data['inventory'])+1).zfill(3)}",
        "name": body["name"],
        "category": body["category"],
        "qty": int(body["qty"]),
        "unit": body["unit"],
        "reorder_level": int(body["reorder_level"]),
        "warehouse": body["warehouse"]
    }
    data["inventory"].append(new_item)
    save_data(data)
    return jsonify({"success": True, "item": new_item}), 201

if __name__ == "__main__":
    app.run(debug=True)
