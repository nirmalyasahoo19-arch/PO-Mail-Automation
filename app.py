import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# ========== CONFIGURATION ==========
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# IMPORTANT:
# These values will come from environment variables
app.config['MAIL_USERNAME'] = os.getenv("OUTLOOK_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("OUTLOOK_APP_PASSWORD")

mail = Mail(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========== ROUTES ==========

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-po', methods=['POST'])
def send_po():
    po_number = request.form['po_number']
    vendor_email = request.form['vendor_email']
    po_pdf = request.files['po_pdf']

    # Save PDF
    filename = f"{po_number}.pdf"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    po_pdf.save(file_path)

    # Create Email
    msg = Message(
        subject=f"Released Purchase Order – PO No: {po_number}",
        sender=app.config['MAIL_USERNAME'],
        recipients=[vendor_email]
    )

    msg.body = f"""
Dear Sir/Madam,

Please find attached the released Purchase Order
PO No: {po_number} for your kind reference.

Kindly acknowledge receipt and confirm the delivery schedule.

Regards,
Nirmalya Sahoo
Purchase Department
Company Name
"""

    with open(file_path, 'rb') as f:
        msg.attach(filename, "application/pdf", f.read())

    mail.send(msg)

    return "PO Email Sent Successfully!"


if __name__ == '__main__':
    app.run(debug=True)

