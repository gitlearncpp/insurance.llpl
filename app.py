from flask import Flask, request, jsonify
from house import House
from person import Person
from sell import PropertyInsuranceCalculator
from db import create_connection
from psycopg2.extras import RealDictCursor
from functools import wraps
import base64

app = Flask(__name__)

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

@app.route("/calculate_price", methods=["POST"])
@requires_auth
def calculate_price():
    try:
        data = request.json

        # import data about house and person
        house_data = data.get("house")
        person_data = data.get("person")

        if not house_data or not person_data:
            raise ValueError("Dane domu i osoby są wymagane.")

        # House object create
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
            house_type=house_data.get("house_type", "house")
        )

        # Object Person
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

        # Verification did client exist in db
        client = get_client_by_pesel(person.pesel)
        if client:
            # if not, update
            update_client_data(client["id"], person_data)
            client_id = client["id"]
        else:
            # New client
            client_id = create_client(person_data)

        # Price calculation
        calculator = PropertyInsuranceCalculator(house)
        price = calculator.base()

        # Save calculation in db
        save_calculation(client_id, house, price)


        return jsonify({
            "price": price,
            "house_details": house.complete_adress().title(),
            "person_name": person.full_name().title()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
