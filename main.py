from flask import Flask, request
import requests

app = Flask(__name__)

# Set your PayPal settings
PAYPAL_VERIFY_URL = 'https://ipnpb.paypal.com/cgi-bin/webscr'
# For testing purposes, you can use the sandbox URL:
# PAYPAL_VERIFY_URL = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'


@app.route('/paypal-ipn', methods=['POST'])
def paypal_ipn_listener():
    # PayPal sends back all data from the original POST with an extra `_notify-validate` parameter
    ipn_data = request.form.to_dict()
    ipn_data['cmd'] = '_notify-validate'
    
    # Send the data back to PayPal to verify
    response = requests.post(PAYPAL_VERIFY_URL, data=ipn_data)
    
    # Check PayPal's response
    if response.text == 'VERIFIED':
        # Process the payment
        # Check IPN data fields such as `payment_status`, `txn_id`, and `receiver_email`
        if ipn_data['payment_status'] == "Completed":
            # Here you would typically update the order status in your database.
            # Example fields:
            # - ipn_data['txn_id'] to verify unique transaction
            # - ipn_data['mc_gross'] to verify the payment amount
            # - ipn_data['payer_email'] to record the payer’s email
            print("Payment verified and completed.")
            return "Verified", 200
        else:
            print("Payment was not completed.")
    else:
        print("Invalid IPN transaction.")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
