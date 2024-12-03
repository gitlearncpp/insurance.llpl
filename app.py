from flask import Flask, request, jsonify, render_template
from house import House
from person import Person
from checkPesel import CheckPesel
from sell import PropertyInsuranceCalculator
from sell2 import PropertyInsuranceCalculator2
from db import create_connection
from psycopg2.extras import RealDictCursor
from functools import wraps
import base64
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
# Easy function for authentication

def check_auth(username, password):
    """Sprawdza poprawność username i password."""
    return username == "admin" and password == "securepassword"

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Authorization header missing"}), 401
        try:
            method, encoded = auth.split()
            if method.lower() != "basic":
                raise ValueError("Invalid auth method")
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":")
            print(f"Decoded credentials: {username}, {password}")  # DEBUG
        except Exception as e:
            print(f"Authorization error: {e}")  # DEBUG
            return jsonify({"error": "Invalid authorization header"}), 401
        if not check_auth(username, password):
            print(f"Invalid credentials: {username}, {password}")  # DEBUG
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# DataBase function
def get_client_by_pesel(pesel):
    conn = create_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM clients WHERE pesel = %s", (pesel,))
    client = cursor.fetchone()
    conn.close()
    return client

def update_client_data(client_id, data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET first_name = %s, last_name = %s, street = %s, city = %s,
            number = %s, postal_code = %s, phone = %s, vip = %s, updated_at = NOW()
        WHERE id = %s
    """, (data['first_name'], data['last_name'], data['street'], data['city'],
          data['number'], data['postal_code'], data['phone'], data['vip'], client_id))
    conn.commit()
    conn.close()

def create_client(data):
    text_fields = ['first_name', 'last_name', 'pesel', 'street', 'city',
                   'postal_code', 'phone']
    for field in text_fields:
        if field in data and isinstance(data[field], str):
            data[field] = data[field].lower()

# DB connection and send data
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (first_name, last_name, pesel, street, city, number, postal_code, phone, vip)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (data['first_name'], data['last_name'], data['pesel'], data['street'], data['city'],
          data['number'], data['postal_code'], data['phone'], data['vip']))
    client_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return client_id

# SaveCalc into DB
def save_calculation(client_id, house, result):
    conn = create_connection()
    cursor = conn.cursor()
    age = house.age()
    cursor.execute("""
        INSERT INTO calculations (client_id, house_price, house_type, house_age, calculation_result)
        VALUES (%s, %s, %s, %s, %s)
    """, (client_id, house.price, house.house_type, age, result))
    conn.commit()
    conn.close()

# Main thing - price calc and response
@app.route("/calculate_price", methods=["POST"])
@requires_auth
def calculate_price():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")

        # Sprawdzanie danych wejściowych
        house_data = data.get("house")
        person_data = data.get("person")

        if not house_data or not person_data:
            raise ValueError("Dane domu i osoby są wymagane.")

        # House object create
        app.logger.debug(f"Creating House object with data: {house_data}")
        house = House(
            price=int(house_data["price"]),
            bedrooms=int(house_data["bedrooms"]),
            bathrooms=int(house_data["bathrooms"]),
            square_feet=int(house_data["square_feet"]),
            lot_size=int(house_data["lot_size"]),
            year_built=int(house_data["year_built"]),
            city=house_data["city"],
            state=house_data["state"],
            address=house_data["address"],
            number=int(house_data["number"]),
            things_inside=house_data["things_inside"],
            house_type=house_data.get("house_type", "house")
        )

        # Object Person create
        app.logger.debug(f"Creating Person object with data: {person_data}")
        person = Person(
            first_name=person_data["first_name"],
            last_name=person_data["last_name"],
            pesel=int(person_data["pesel"]),
            street=person_data.get("street"),
            city=person_data.get("city"),
            number=int(person_data.get("number")),
            postal_code=person_data.get("postal_code"),
            phone=person_data.get("phone"),
            vip=person_data.get("vip", False)
        )

        # Verification did client exist in db
        client = get_client_by_pesel(person.pesel)
        app.logger.debug(f"Client found in DB: {client}")

        if client:
            update_client_data(client["id"], person_data)
            client_id = client["id"]
        else:
            client_id = create_client(person_data)

        # Price calculation
        app.logger.debug(f"Calculating price for house: {house}")
        calculator = PropertyInsuranceCalculator(house)
        calculator2 = PropertyInsuranceCalculator2(house)
        price = calculator.base()   #Place for price
        price2 = calculator2.base2()

        # Check age based on PESEL
        check_pesel_instance = CheckPesel(person)
        check_pesel = check_pesel_instance.check_age()

        # Save calculation in db
        save_calculation(client_id, house, price)

        return jsonify({
            "price": price,
            "price_2": price2,
            "house_details": house.complete_adress().title(),
            "house_insurance_sum": house.insurance_sum(),
            "person_name": person.full_name().title(),
            "check_pesel": check_pesel
        }), 200

    except Exception as e:
        app.logger.error(f"Error occurred during price calculation: {str(e)}")
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)

