"""Flask app for Cupcakes"""
from forms import AddCupcakeForm
from flask import Flask, jsonify, request, render_template, redirect, flash
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'password123!'

# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():

    form = AddCupcakeForm()

    return render_template("index.html", form=form)


@app.route('/api/cupcakes')
def all_cupcakes():
    """ Get data about all cupcakes """

    cupcakes = Cupcake.query.all()

    cupcakes_json = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=cupcakes_json), 200


@app.route('/api/cupcakes/<int:cupcake_id>')
def one_cupcake_by_id(cupcake_id):
    """ Get data about a cupcake by id """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake_json = cupcake.serialize()

    return jsonify(cupcake=cupcake_json), 200


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """ Create a cupcake """

    form = AddCupcakeForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data

        if not image:
            image = Cupcake.default_image

        new_cupcake = Cupcake(flavor=flavor, size=size,
                              rating=rating, image=image)

        db.session.add(new_cupcake)
        db.session.commit()

        return redirect('/')

    try:
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
        image = request.json.get("image")

        new_cupcake = Cupcake(flavor=flavor, size=size,
                              rating=rating, image=image)

        db.session.add(new_cupcake)
        db.session.commit()

    except TypeError and KeyError:
        return jsonify({"status": 400, "error": "Bad Request",
                        "message": "Check json payload for errors."}), 400

    cupcake = new_cupcake.serialize()

    return jsonify(cupcake=cupcake), 201


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def edit_cupcake(cupcake_id):
    """ Update a cupcake """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    try:
        cupcake.flavor = request.json["flavor"]
        cupcake.size = request.json["size"]
        cupcake.rating = request.json["rating"]
        cupcake.image = request.json.get("image", Cupcake.default_image)

        db.session.commit()

    except TypeError and KeyError:
        return jsonify({"status": 400, "error": "Bad Request",
                        "message": "Check json payload for errors."}), 400

    cupcake = cupcake.serialize()

    return jsonify(cupcake=cupcake), 200


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete a cupcake """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake Deleted"), 200
