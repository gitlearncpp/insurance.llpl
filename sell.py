import psycopg2
from psycopg2 import sql

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

  #  def age_factor(self):
   #     if self.house.age <= 10:
    #        return 3.0
     #   elif self.house.age <= 20:
      #      return 1.3
       ##    return 1.1
        #elif self.house.age <= 40:
         #   return 1.0
      #  else:
       #     return 0.9

    def house_factor(self):
        if self.house.house_type == "house":
            return 1.1
        elif self.house.house_type == "apartment":
            return 1.0
        elif self.house.house_type == "flat":
            return 1.0
        elif self.house.house_type == "townhouse":
            return 1.2

    def base(self):
        return (
            500
            * self.house_factor()
         #   * self.age_factor()
            * self.calculate_factor()
        )
