from flask import Flask, request, render_template, redirect, url_for, flash, jsonify

import sell
from house import House
from person import Person

app = Flask(__name__)
app.secret_key = '770-818-154'

@app.route('/person', methods=['POST'])
def create_person():
    data = request.json
    person = Person(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        pesel=data.get('pesel'),
        street=data.get('street'),
        city=data.get('city'),
        number=data.get('number'),
        postal_code=data.get('postal_code'),
        phone=data.get('phone'),
        vip=data.get('vip', False)
    )

    response = {
      #  'input_data': data,
        'full_name': person.full_name(),
        'address': person.adress(),
        'phone': person.phone,
        'vip_status': 'VIP' if person.vip else 'Non-VIP'

    }
    return jsonify(response), 201

@app.route('/house', methods=['POST'])
def create_house():
    data = request.json
    house = House(
        price=data.get('price'),
        bedrooms=data.get('bedrooms'),
        bathrooms=data.get('bathrooms'),
        square_feet=data.get('square_feet'),
        lot_size=data.get('lot_size'),
        year_built=data.get('year_built'),
        city=data.get('city'),
        state=data.get('state'),
        address=data.get('address'),
        number=data.get('number'),
        things_inside=data.get('things_inside'),
        house_type=data.get('house_type'),
    )

    response = {
        'complete_adress':house.complete_adress(),
        'insurance_sum': house.insurance_sum(),

    }

    return jsonify(response), 201


if __name__ == '__main__':
    app.run(debug=True)
