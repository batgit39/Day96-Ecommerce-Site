from flask import Flask, render_template, request, redirect
import stripe

app = Flask(__name__)

# Set your Stripe API keys
stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'
stripe_publishable_key = 'YOUR_STRIPE_PUBLISHABLE_KEY'

# Sample product data
products = [
    {'name': 'Product 1', 'price': 10.99},
    {'name': 'Product 2', 'price': 19.99},
    {'name': 'Product 3', 'price': 14.99}
]

# Cart to store added items
cart = []

# Home Page
@app.route('/')
def home():
    # Render the home page template with products and Stripe keys
    return render_template('index.html', products=products, publishable_key=stripe_publishable_key)

# Add item to cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_index = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    product = products[product_index]
    total = product['price'] * quantity
    cart.append({'product': product, 'quantity': quantity, 'total': total})
    return redirect('/cart')  # Redirect to the cart page

# Cart Page
@app.route('/cart')
def view_cart():
    cart_total = sum(item['total'] for item in cart)
    return render_template('cart.html', cart_items=cart, cart_total=cart_total)


# Checkout Page
# Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Get the payment token from the request
        token = request.form['stripeToken']

        # Get the total amount from the cart
        total_amount = sum(item['total'] for item in cart)
        
        try:
            # Convert the total amount to cents
            amount_in_cents = int(total_amount * 100)

            # Create a charge or perform payment processing
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency='usd',
                source=token,
                description='Payment for Products'
            )
            
            # Payment successful, clear the cart and redirect to success page
            cart.clear()
            return render_template('payment_success.html')
        except stripe.error.CardError as e:
            # Payment failed, handle the error
            error_message = e.error.message
            return render_template('payment_failed.html', error_message=error_message)

    # Render the checkout page with Stripe keys and cart information
    cart_total = sum(item['total'] for item in cart)
    return render_template('checkout.html', publishable_key=stripe_publishable_key, cart_items=cart, cart_total=cart_total)


# Login Page
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

