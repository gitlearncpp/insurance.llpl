from flask import Flask, request, jsonify
from house import House
from person import Person
from sell import PropertyInsuranceCalculator

app = Flask(__name__)

@app.route("/calculate_price", methods=["POST"])
def calculate_price():
    try:
        data = request.json

        # Pobieranie danych o domu i osobie
        house_data = data.get("house")
        person_data = data.get("person")

        # Tworzenie obiektu House
        house = House(
            price=house_data["price"],
            bedrooms=house_data["bedrooms"],
            bathrooms=house_data["bathrooms"],
            square_feet=house_data["square_feet"],
            lot_size=house_data["lot_size"],
            year_built=house_data["year_built"],
            city=house_data["city"],
            state=house_data["state"],
            address=house_data["address"],
            number=house_data["number"],
            things_inside=house_data["things_inside"],
            house_type=house_data.get("house_type", "house")  # Domyślnie "house"
        )

        # Tworzenie obiektu Person (opcjonalne dla tego przykładu)
        person = Person(
            first_name=person_data["first_name"],
            last_name=person_data["last_name"],
            pesel=person_data["pesel"],
            street=person_data.get("street"),
            city=person_data.get("city"),
            number=person_data.get("number"),
            postal_code=person_data.get("postal_code"),
            phone=person_data.get("phone"),
            vip=person_data.get("vip", False)
        )

        # Kalkulacja ceny
        calculator = PropertyInsuranceCalculator(house)
        price = calculator.base()

        return jsonify({
            "price": price,
            "house_details": house.complete_adress(),
            "person_name": person.full_name()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
