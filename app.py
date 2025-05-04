from flask import Flask, request, jsonify, send_from_directory
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Directory to store PDF files
PDF_FOLDER = 'cab-bookings'
os.makedirs(PDF_FOLDER, exist_ok=True)

# Function to generate PDF using ReportLab
def generate_pdf(booking_id, customer_name, pickup, drop, car, email, image_path):
    pdf_path = os.path.join(PDF_FOLDER, f"{booking_id}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Booking details
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 750, "🚖 Cab Booking Confirmation")

    c.setFont("Helvetica", 12)
    c.drawString(30, 720, f"📅 Booking ID: {booking_id}")
    c.drawString(30, 700, f"👤 Customer Name: {customer_name}")
    c.drawString(30, 680, f"📍 Pickup Location: {pickup}")
    c.drawString(30, 660, f"📍 Drop Location: {drop}")
    c.drawString(30, 640, f"🚗 Car Details: {car}")
    c.drawString(30, 620, f"📧 Confirmation sent to: {email}")

    # Add image if it exists
    if os.path.exists(image_path):
        c.drawImage(image_path, 400, 600, width=120, height=120)

    c.save()
    return pdf_path

@app.route('/cab-bookings/<booking_id>', methods=['POST'])
def create_pdf(booking_id):
    data = request.json

    # Generate PDF
    pdf_path = generate_pdf(
        booking_id,
        data.get('customer_name'),
        data.get('pickup'),
        data.get('drop'),
        data.get('car'),
        data.get('email'),
        os.path.abspath("static/download.png")  # Adjust if needed
    )

    # Return dynamic local link
    download_url = f"{request.host_url}cab-bookings/{booking_id}.pdf"
    return jsonify({'message': 'PDF created successfully', 'pdf_url': download_url})

@app.route('/cab-bookings/<filename>.pdf', methods=['GET'])
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, f"{filename}.pdf")  # <== inline viewing

if __name__ == '__main__':
    # Get the port from the environment variable, default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  # Listen on dynamic port provided by Render
