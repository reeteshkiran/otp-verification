import streamlit as st
import requests

# Define the hardcoded phone number (replace with your own)
hardcoded_phone_number = '+917348889244'

# URLs of the Flask app's endpoints
flask_send_otp_url = 'http://127.0.0.1:5000/send_otp'
flask_app_url = 'http://127.0.0.1:5000/validate_otp'

# Streamlit app
st.title('OTP Verification')

# Button to request OTP
if st.button('Request OTP'):
    # Make a POST request to the Flask app's /send_otp endpoint
    response = requests.post(flask_send_otp_url, json={'phone_number': hardcoded_phone_number})
    data = response.json()
    
    # Show a message based on the response
    st.write(data.get('message', 'An error occurred.'))

# Input field for OTP
otp = st.text_input('Enter OTP')

# Button to submit OTP for validation
if st.button('Submit'):
    # Make a POST request to the Flask app's validation endpoint
    response = requests.post(flask_app_url, json={
        'phone_number': hardcoded_phone_number,
        'otp': otp
    })

    # Parse the response JSON
    data = response.json()

    # Display a success or error message based on the validation result
    if data['valid']:
        st.success('OTP validated successfully!')
    else:
        st.error('Invalid OTP. Please try again.')
