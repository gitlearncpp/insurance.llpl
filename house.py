class House:
    def __init__(self, price, bedrooms, bathrooms, square_feet, lot_size,
                 year_built, city, state, address, number, things_inside):
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.square_feet = square_feet
        self.lot_size = lot_size
        self.year_built = year_built
        self.address = address
        self.number = number
        self.city = city
        self.state = state
        self.things_inside = things_inside

    def complete_adress(self):
        return f"{self.state}, {self.address}, {self.number}, {self.city}"

    def insurance_sum(self):
        return f"{self.price}, {self.things_inside}"
