from flask import Flask, render_template

app = Flask(__name__)

PRODUCTS = [
    {"id": "classic-tee", "name": "Spazz classic tee", "price": 150,
     "category": "T-shirts", "blurb": "Heavyweight cotton, clean collar, relaxed fit."},
    {"id": "graphic-tee", "name": "Spazz graphic tee", "price": 200,
     "category": "T-shirts", "blurb": "Geometric chest print on a dark base."},
    {"id": "hooded-sweatshirt", "name": "Spazz hooded sweatshirt", "price": 300,
     "category": "Hoodies", "blurb": "Brushed fleece pullover with a deep pocket."},
    {"id": "hoodie-shirt", "name": "Spazz hoodie shirt", "price": 400,
     "category": "Hoodies", "blurb": "Full-zip layer for cooler evenings."},
    {"id": "tank-top", "name": "Spazz tank top", "price": 120,
     "category": "Tops", "blurb": "Light, breathable and easy to layer."},
    {"id": "long-sleeve", "name": "Spazz long sleeve", "price": 250,
     "category": "Tops", "blurb": "Fitted long sleeve with ribbed cuffs."},
]


@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)


if __name__ == "__main__":
    app.run(debug=True)
