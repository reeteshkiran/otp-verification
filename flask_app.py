from flask import Flask, request, jsonify
from twilio.rest import Client
import random

app = Flask(__name__)

# Twilio credentials and phone number (replace with your own)
ACCOUNT_SID = 'AC82fb445d30608912dd939230392c2158'
AUTH_TOKEN = 'b32c2ab02aed03a7d1c1b2643464242b'
TWILIO_PHONE_NUMBER = '+12565948470'

# Create a Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# In-memory dictionary to store phone numbers and OTPs
otp_store = {}

# Endpoint for generating and sending OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    phone_number = data['phone_number']

    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)

    # Store the OTP for the phone number
    otp_store[phone_number] = otp

    # Send the OTP via SMS using Twilio
    client.messages.create(
        body=f"Your OTP code is {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return jsonify({"message": "OTP sent via SMS."})

# Endpoint for validating OTP
@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.json
    phone_number = data['phone_number']
    input_otp = int(data['otp'])

    # Retrieve the stored OTP for the phone number
    stored_otp = otp_store.get(phone_number)

    # Check if the input OTP matches the stored OTP
    if stored_otp == input_otp:
        # Successful validation
        # Remove the OTP from the store
        del otp_store[phone_number]
        return jsonify({"valid": True, "message": "OTP validated successfully."})
    else:
        # Validation failed
        return jsonify({"valid": False, "message": "Invalid OTP."})

if __name__ == '__main__':
    app.run(debug=True)
