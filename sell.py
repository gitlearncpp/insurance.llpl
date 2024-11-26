

class PropertyInsuranceCalculator:
    def __init__(self, house):
        self.house = house

    def calculate_factor(self):
        if self.house.price <= 200000:
            return 0.95
        elif self.house.price <= 400000:
            return 1.1
        elif self.house.price <= 600000:
            return 1.2
        else:
            return 1.4

    def age_factor(self):
        age = self.house.age()  # Wywołanie metody age
        if age <= 10:
            return 1.1
        elif age <= 20:
            return 1.2
        elif age <= 40:
            return 1.0
        elif age <= 200:
            return 0.9
        else:
            return 1.0  # Domyślny współczynnik

    def house_factor(self):
        if self.house.house_type == "house":
            return 1.1
        elif self.house.house_type in ["apartment", "flat"]:
            return 1.0
        elif self.house.house_type == "townhouse":
            return 1.2
        else:
            return 1.0

    def size_factor(self):
        if self.house.square_feet <= 70:
            return 1.0
        elif self.house.square_feet <= 90:
            return 1.1
        elif self.house.square_feet <= 110:
            return 1.2
        elif self.house.square_feet <= 130:
            return 1.3
        else:
            return 1.4



    def base(self):
        return round(
            500
            * self.house_factor()
            * self.age_factor()
            * self.calculate_factor()
            * self.size_factor()
        )
