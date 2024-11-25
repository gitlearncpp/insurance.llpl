from flask import Flask, request, jsonify
from person import Person

app = Flask(__name__)


@app.route('/person', methods=['POST'])
def create_person():
    data = request.json
    person = Person(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
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


if __name__ == '__main__':
    app.run(debug=True)
