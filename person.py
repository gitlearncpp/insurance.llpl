class Person:
    def __init__(self, first_name, last_name, pesel,street=None, city=None, number=None, postal_code=None, phone=None, vip=False):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel
        self.street = street
        self.city = city
        self.number = number
        self.postal_code = postal_code
        self.phone = phone
        self.vip = vip

    def full_name(self):
            return f"{self.first_name.title()} {self.last_name.title()}"

    def adress(self):
        return f"{self.street.title()}, {self.number}, {self.city.title()} {self.postal_code.upper()}"

    def phone(self):
        return {self.phone}

    def vip(self):
        return "VIP" if self.vip else "Zostań klientem VIP!"

    def pesel(self):
        return self.pesel

    def __repr__(self):
        return f"<Person {self.full_name()}>"


