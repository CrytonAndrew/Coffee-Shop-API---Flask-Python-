from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

#   Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'sfhldkjfjorfpoejpofaelkf'


#   Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    location = request.args.get("loc")
    cafes = Cafe.query.filter_by(location=f"{location}")
    if cafes:
        cafes_dict = {}
        for record in cafes:
            new_dict = {'id': record.id, 'name': record.name, 'img_url': record.img_url, 'location': record.location,
                        'map_url': record.map_url, 'seats': record.seats, 'can_take_calls': record.can_take_calls,
                        'coffee_price': record.coffee_price, 'has_sockets': record.has_sockets,
                        'has_toilet': record.has_toilet, 'has_wifi': record.has_wifi}
            cafes_dict[f'{record.id}'] = new_dict

        return jsonify(cafes=cafes_dict)
    else:
        error_object = {"error": {f"The location {location} does not exist in the database"}}
        return jsonify(failed=error_object)


@app.route("/random", methods=["GET", "POST"])
def random_cafe():
    random_id = random.randint(0, 20)
    cafe = Cafe.query.filter_by(id=f'{random_id}').first()
    print(cafe)
    if request.method == "GET":

        can_take_calls = cafe.can_take_calls

        coffee_price = cafe.coffee_price

        has_sockets = cafe.has_sockets

        has_toilets = cafe.has_toilet

        has_wifi = cafe.has_wifi

        id = cafe.id

        img_url = cafe.img_url
        location = cafe.location
        map_url = cafe.map_url
        name = cafe.name
        seats = cafe.seats

        return jsonify(
            can_take_calls=can_take_calls,
            coffee_price=coffee_price,
            has_sockets=has_sockets,
            has_toilets=has_toilets,
            has_wifi=has_wifi,
            id=id,
            img_url=img_url,
            location=location,
            map_url=map_url,
            name=name,
            seats=seats,
        )


@app.route("/all")
def all_cafes():
    cafes = Cafe.query.all()
    dict_cafes = {}

    print(cafes)

    for record in cafes:
        new_dict = {'id': record.id, 'name': record.name, 'img_url': record.img_url, 'location': record.location,
                    'map_url': record.map_url, 'seats': record.seats, 'can_take_calls': record.can_take_calls,
                    'coffee_price': record.coffee_price, 'has_sockets': record.has_sockets,
                    'has_toilet': record.has_toilet, 'has_wifi': record.has_wifi}
        dict_cafes[f'{record.id}'] = new_dict

    print(dict_cafes)
    return jsonify(
        dict_cafes
    )


@app.route("/update_price/<cafe_id>", methods=["GET", "POST", "PUT", "PATCH"])
def update_cafe_price(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()

    if request.method == "PATCH":
        if cafe:
            cafe.coffee_price = f'${request.form.get("coffee_price")}'
            print(request.form.get("coffee_price"))
            db.session.commit()
            return jsonify(
                response={"Success": f"Cafe with id: {cafe.id} coffee price was successfully updated"}
            ), 200

        return jsonify(
            response={"Not Found": "Cafe object was not found in the database"}
        ), 404


@app.route("/delete/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    authentication_key = "aksfhkjshfkdhfiowehfodhf"
    if request.args.get("auth_key") == authentication_key:
        Cafe.query.filter_by(id=cafe_id).delete()
        db.session.commit()
        return jsonify(
            reponse={f"Success": f"Cafe with id: {cafe_id} was deleted"}
        ), 200

    return jsonify(
        response={f"Auth failed": f"Not authenticated to make such an action"}
    ), 404


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        can_take_calls = request.form["can_take_calls"]
        coffee_price = request.form["coffee_price"]
        has_sockets = request.form["has_sockets"]
        has_toilet = request.form["has_toilet"]
        has_wifi = request.form["has_wifi"]
        location = request.form["location"]
        map_url = request.form["map_url"]
        name = request.form["name"]
        seats = request.form["seats"]
        img_url = request.form["img_url"]

        new_cafe = Cafe(
            location=location,
            img_url=img_url,
            map_url=map_url,
            name=name,
            seats=seats,
            has_wifi=bool(has_wifi),
            has_toilet=bool(has_toilet),
            has_sockets=bool(has_sockets),
            coffee_price=float(coffee_price),
            can_take_calls=bool(can_take_calls)
        )
        db.session.add(new_cafe)
        db.session.commit()

        return jsonify(
            success=f"Successfully added cafe record"
        )


if __name__ == '__main__':
    app.run(debug=True)
