from flask import Flask, render_template, request, redirect, url_for, Response, send_file
import sqlite3
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from ocr import extract_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database Connection
def get_db_connection():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home Page - Upload Prescription & Process Medicines


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        patient_name = request.form["patient_name"]
        file = request.files["prescription"]
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            extracted_text = extract_text(filepath)
            matched_meds = match_medicine(extracted_text)
            matched_meds_str = ", ".join(matched_meds) if matched_meds else "Not Found"

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (patient_name, prescription, matched_medicine, status)
                VALUES (?, ?, ?, ?)
            """, (patient_name, extracted_text, matched_meds_str, "Pending"))
            conn.commit()
            conn.close()

            return redirect(url_for("orders"))

    return render_template("index.html")

# Function to Match Medicines from Prescription
def match_medicine(extracted_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    words = extracted_text.split()
    matched_meds = []

    for word in words:
        cursor.execute("SELECT name, disease, power FROM medicines WHERE name LIKE ?", ('%' + word + '%',))
        result = cursor.fetchone()
        if result:
            med_name, disease, power = result
            matched_meds.append(f"{med_name} ({power}) - Used for {disease}")

    conn.close()
    return matched_meds



# Orders Page - View & Manage Orders

@app.route("/orders")
def orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return render_template("orders.html", orders=orders)

@app.route("/update_status/<int:order_id>", methods=["POST"])
def update_status(order_id):
    new_status = request.form.get("status")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

    return redirect(url_for("orders"))

@app.route("/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("orders"))


# Generate PDF Receipt for Orders

@app.route("/generate_receipt/<int:order_id>")
def generate_receipt(order_id):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    conn.close()

    if not order:
        return "Order not found!", 404

    pdf_filename = f"receipt_{order_id}.pdf"
    pdf_path = os.path.join("uploads", pdf_filename)

    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title = Paragraph("Pharmacy Receipt", styles["Title"])
    spacer = Spacer(1, 12)

    wrap_style = styles["BodyText"]

    order_data = [
        ["Patient Name:", Paragraph(order[1], wrap_style)],
        ["Prescription:", Paragraph(order[2], wrap_style)],
        ["Matched Medicine:", Paragraph(order[3], wrap_style)], 
        ["Status:", Paragraph(order[4], wrap_style)],
    ]

    table = Table(order_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    footer = Paragraph("Thank you for choosing our pharmacy!", styles["Italic"])

    elements = [title, spacer, table, spacer, footer]
    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)



# Admin Panel - Manage Medicines

@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    conn.close()
    return render_template("admin.html", medicines=medicines)

@app.route("/add_medicine", methods=["POST"])
def add_medicine():
    name = request.form["name"]
    disease = request.form["disease"]
    power = request.form["power"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medicines (name, disease, power) VALUES (?, ?, ?)", (name, disease, power))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin"))

@app.route("/edit_medicine/<int:med_id>", methods=["POST"])
def edit_medicine(med_id):
    name = request.form["name"]
    disease = request.form["disease"]
    power = request.form["power"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET name = ?, disease = ?, power = ? WHERE id = ?", (name, disease, power, med_id))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

@app.route("/delete_medicine/<int:med_id>", methods=["POST"])
def delete_medicine(med_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

# Run the Flask App

if __name__ == "__main__":
    app.run(debug=True)
