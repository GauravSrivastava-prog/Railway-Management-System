from flask import Flask, request, render_template
import webbrowser
import threading

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def payment():
    print("Payment route accessed")
    print("Request form data:", request.form)
    payment_info = request.form
    mod_of_payment = payment_info.get('paymentType')
    cardNumber = payment_info.get('cardNumber')
    cvv = payment_info.get('cvv')
    print("Payment Information:")
    print("Payment Type:", mod_of_payment)
    print("Card Number:", cardNumber)
    print("CVV:", cvv)
    return 'Payment information received successfully!'

@app.route('/')
def home():
    template_path = 'boilerplate.html'
    return render_template(template_path)

def run_flask(use_reloader=True):
    app.run(debug=True, port=5002, use_reloader=use_reloader)

if __name__ == "__main__":
    # Check if running in the main thread
    if threading.current_thread() is threading.main_thread():
        # Open browser only if running in the main thread
        webbrowser.open("http://127.0.0.1:5002/")
    run_flask(use_reloader=False)