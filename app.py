from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from flask_session import Session
from ai.search_engine import search_products
from database.db import get_connection
from ai.huggingface_client import generate_ai_explanation
import re
app = Flask(__name__)

app.secret_key = "shopsmart_secret_key"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# HOME PAGE

@app.route("/")
def home():

    db = get_connection()

    featured_products = db.fetch_all("""
        SELECT *
        FROM products
        ORDER BY rating_avg DESC, review_count DESC
        LIMIT 8
    """)

    trending_products = db.fetch_all("""
        SELECT *
        FROM products
        ORDER BY discount_percent DESC,
                 rating_avg DESC
        LIMIT 8
    """)

    best_sellers = db.fetch_all("""
        SELECT *
        FROM products
        WHERE badge='Best Seller'
        ORDER BY rating_avg DESC,
                 review_count DESC
    """)
    categories = db.fetch_all("""
    SELECT
        category,
        MIN(image_url) AS image_url
    FROM products
    WHERE image_url IS NOT NULL
    GROUP BY category
    ORDER BY category
""")

    db.close()

    return render_template(
    "index.html",
    featured_products=featured_products,
    trending_products=trending_products,
    best_sellers=best_sellers,
    categories=categories
)

# CATEGORY PAGE

@app.route("/category/<category>")
def category(category):

    db = get_connection()

    products = db.fetch_all("""
        SELECT *
        FROM products
        WHERE category = %s
        ORDER BY
            rating_avg DESC,
            review_count DESC
    """, (category,))

    db.close()

    return render_template(
        "category.html",
        category=category,
        products=products
    )

# PRODUCT DETAILS

@app.route("/product/<product_id>")
def product(product_id):

    db = get_connection()

    # Get selected product
    product = db.fetch_one("""
        SELECT *
        FROM products
        WHERE product_id = %s
    """, (product_id,))

    # Product not found
    if not product:
        db.close()
        flash("Product not found.", "warning")
        return redirect(url_for("home"))

    # Related products
    related_products = db.fetch_all("""
        SELECT *
        FROM products
        WHERE category = %s
        AND product_id != %s
        ORDER BY
            rating_avg DESC,
            review_count DESC
        LIMIT 4
    """, (
        product["category"],
        product_id
    ))

    # AI PRODUCT INSIGHT

    ai_insight = ""

    category = product["category"]

    if category == "Laptops":

        ai_insight = (
            f"{product['product_name']} is an excellent choice for students, programmers "
            "and office professionals. It offers a strong balance of performance, "
            "customer satisfaction and overall value."
        )

    elif category == "Smartphones":

        ai_insight = (
            f"{product['product_name']} is recommended for everyday use, photography "
            "and entertainment. It stands out because of its good ratings, reliable "
            "performance and positive customer feedback."
        )

    elif category == "Headphones":

        ai_insight = (
            f"{product['product_name']} delivers a comfortable listening experience "
            "for music, gaming and online meetings. Customers appreciate its sound "
            "quality and overall reliability."
        )

    elif category == "Shoes":

        ai_insight = (
            f"{product['product_name']} is designed for comfort and durability, making "
            "it a great option for walking, running and everyday use."
        )

    elif category == "Beauty":

        ai_insight = (
            f"{product['product_name']} is a trusted beauty product with strong customer "
            "ratings and consistent user satisfaction."
        )

    elif category == "Books":

        ai_insight = (
            f"{product['product_name']} is recommended for readers who want to build "
            "their knowledge in this subject. It has received positive feedback from "
            "many customers."
        )

    elif category == "Cycles":

        ai_insight = (
        f"{product['product_name']} is ideal for cycling enthusiasts and outdoor activities. "
        "It is highly rated for durability, comfort, and overall performance."
    )

    else:

        ai_insight = (
            "This product is recommended based on its customer ratings, reviews and popularity."
        )

    db.close()

    return render_template(
        "product.html",
        product=product,
        related_products=related_products,
        ai_insight=ai_insight
    )

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    db = get_connection()

    user = db.fetch_one("""
        SELECT *
        FROM users
        WHERE email = %s
    """, (email,))

    db.close()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("login"))

    # TODO: Replace with password hashing later
    if user["password"] != password:
        flash("Incorrect password.", "danger")
        return redirect(url_for("login"))

    session["user_id"] = user["user_id"]
    session["user_name"] = user["name"]

    flash(f"Welcome, {user['name']}!", "success")

    return redirect(url_for("home"))

# SIGNUP

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not name or not email or not password:
        flash("Please fill in all fields.", "warning")
        return redirect(url_for("signup"))

    db = get_connection()

    existing = db.fetch_one("""
        SELECT user_id
        FROM users
        WHERE email = %s
    """, (email,))

    if existing:
        db.close()
        flash("Email already exists.", "warning")
        return redirect(url_for("signup"))

    db.execute("""
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
    """, (
        name,
        email,
        password
    ))

    db.close()

    flash("Registration successful! Please log in.", "success")

    return redirect(url_for("login"))

# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("home"))

# PROFILE

@app.route("/profile")
def profile():

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    db = get_connection()

    user = db.fetch_one("""
        SELECT *
        FROM users
        WHERE user_id = %s
    """, (session["user_id"],))

    cart_count = db.fetch_one("""
        SELECT COUNT(*) AS total
        FROM cart
        WHERE user_id = %s
    """, (session["user_id"],))

    db.close()

    return render_template(
        "profile.html",
        user=user,
        cart_count=cart_count["total"]
    )

# ADD TO CART

@app.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    db = get_connection()

    existing = db.fetch_one("""
        SELECT *
        FROM cart
        WHERE user_id=%s
        AND product_id=%s
    """, (
        session["user_id"],
        product_id
    ))

    if existing:

        db.execute("""
            UPDATE cart
            SET quantity = quantity + 1
            WHERE cart_id=%s
        """, (existing["cart_id"],))

    else:

        db.execute("""
            INSERT INTO cart(user_id, product_id, quantity)
            VALUES(%s, %s, %s)
        """, (
            session["user_id"],
            product_id,
            1
        ))

    db.close()

    flash("Product added to cart!", "success")

    return redirect(request.referrer or url_for("home"))

# BUY NOW


@app.route("/buy-now/<product_id>", methods=["POST"])
def buy_now(product_id):

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    db = get_connection()

    # Remove any existing cart items
    db.execute("""
        DELETE FROM cart
        WHERE user_id = %s
    """, (session["user_id"],))

    # Add this product to the cart
    db.execute("""
        INSERT INTO cart (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
    """, (
        session["user_id"],
        product_id,
        1
    ))

    db.close()

    return redirect(url_for("checkout"))

# CART PAGE

@app.route("/cart")
def cart():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    db = get_connection()

    cart_items = db.fetch_all("""
        SELECT
            c.cart_id,
            c.quantity,
            p.*
        FROM cart c
        JOIN products p
        ON c.product_id = p.product_id
        WHERE c.user_id=%s
    """, (session["user_id"],))

    total = 0

    for item in cart_items:

        item["subtotal"] = item["price"] * item["quantity"]
        total += item["subtotal"]

    db.close()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=round(total, 2)
    )

# UPDATE CART

@app.route("/cart/update/<int:cart_id>", methods=["POST"])
def update_cart(cart_id):

    quantity = int(request.form.get("quantity", 1))

    if quantity < 1:
        quantity = 1

    db = get_connection()

    db.execute("""
        UPDATE cart
        SET quantity=%s
        WHERE cart_id=%s
    """, (
        quantity,
        cart_id
    ))

    db.close()

    flash("Cart updated successfully.", "success")

    return redirect(url_for("cart"))

# REMOVE FROM CART

@app.route("/cart/remove/<int:cart_id>")
def remove_cart(cart_id):

    db = get_connection()

    db.execute("""
        DELETE FROM cart
        WHERE cart_id=%s
    """, (cart_id,))

    db.close()

    flash("Product removed from cart.", "success")

    return redirect(url_for("cart"))

# CHECKOUT

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    db = get_connection()

    cart_items = db.fetch_all("""
        SELECT
            c.cart_id,
            c.quantity,
            p.*
        FROM cart c
        JOIN products p
            ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (session["user_id"],))

    total = 0

    for item in cart_items:
        item["subtotal"] = item["price"] * item["quantity"]
        total += item["subtotal"]

    if request.method == "POST":

        # Create Order
        db.execute("""
            INSERT INTO orders (user_id, total_amount)
            VALUES (%s, %s)
        """, (
            session["user_id"],
            round(total, 2)
        ))

        # Get Order ID
        order_id = db.last_insert_id()
        print("Order ID:", order_id)
        print("Cart Items:", cart_items)

        # Save Order Items
        for item in cart_items:
            print("Saving item:", item)

            db.execute("""
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES
                (%s, %s, %s, %s)
            """, (
                order_id,
                item["product_id"],
                item["quantity"],
                item["price"]
            ))

        # Clear Cart
        db.execute("""
            DELETE FROM cart
            WHERE user_id = %s
        """, (session["user_id"],))

        db.close()

        flash("Order placed successfully!", "success")

        return redirect(url_for("orders"))

    db.close()

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=round(total, 2)
    )
# MY ORDERS

@app.route("/orders")
def orders():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    db = get_connection()

    orders = db.fetch_all("""
        SELECT *
        FROM orders
        WHERE user_id=%s
        ORDER BY order_date DESC
    """, (session["user_id"],))

    db.close()

    return render_template(
        "orders.html",
        orders=orders
    )

# AI SHOPPING COPILOT

@app.route("/ai-search", methods=["POST"])
def ai_search():

    query = request.form.get("query", "").strip()

    if not query:
        flash("Please enter something to search.", "warning")
        return redirect(url_for("home"))

    db = get_connection()

    products = db.fetch_all("SELECT * FROM products")

    results = search_products(products, query)

    db.close()
    
    # Top 5 Products

    recommendations = results[:5]

    if recommendations:

        explanation = generate_ai_explanation(
        query,
        recommendations
    )

    else:

        explanation = (
        "No matching products were found."
        )

    return render_template(
        "search_results.html",
        query=query,
        products=recommendations,
        explanation=explanation
    )

# NORMAL SEARCH
@app.route("/search")
def search():

    query = request.args.get("q","").strip()

    if not query:
        return redirect(url_for("home"))

    db = get_connection()

    products = db.fetch_all("SELECT * FROM products")

    db.close()

    products = search_products(products, query)

    return render_template(
        "search_results.html",
        query=query,
        products=products,
        explanation=None
    )
# PRODUCTS API

@app.route("/api/products")
def api_products():

    db = get_connection()

    products = db.fetch_all("""
        SELECT *
        FROM products
        ORDER BY
            rating_avg DESC,
            review_count DESC
    """)

    db.close()

    return jsonify(products)

# ERROR PAGES

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template("500.html"), 500


# MAIN

if __name__ == "__main__":

    app.run(
        debug=True
    )