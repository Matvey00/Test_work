# не понимаю как отобразить что в Products на главной в таблице вместе с Locations



from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Products %r>' % self.id


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    quantity = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    posts = Products.query.all()

    return render_template("index.html", posts=posts, )


@app.route('/prod/<int:id>')
def prod(id):
    post = Products.query.get(id)
    return render_template("prod.html", post=post)


@app.route('/prod/<int:id>/del')
def prod_del(id):
    post = Products.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении продукта произошла ошибка"


@app.route('/prod/<int:id>', methods=['POST', 'GET'])
def prod_update(id):
    post = Products.query.get(id)
    if request.method == "POST":
        post.name = request.form['name']
        post.description = request.form['description']
        post.price = request.form['price']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При редактировании продукта произошла ошибка"
    else:

        return render_template("prod.html", post=post)


@app.route('/creat', methods=['POST', 'GET'])
def creat():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        post = Products(name=name, description=description, price=price)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении продукта произошла ошибка"
    else:
        return render_template("creat.html")


@app.route('/location', methods=['POST', 'GET'])
def location():
    if request.method == "POST":
        name = request.form['name']

        post = Locations(name=name)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении локации произошла ошибка"
    else:
        return render_template("location.html")


if __name__ == "__main__":
    app.run(debug=True)
