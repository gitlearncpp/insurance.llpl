from person import Person
from datetime import datetime

class CheckPesel:
    def __init__(self, person: Person):  # Typowanie dla większej jasności
        self.person = person

    def check_pesel(self):
        pesel = str(self.person.pesel)  # Konwertujemy pesel na string
        if len(pesel) != 11:  # Sprawdzamy długość
            return False
        if not pesel.isdigit():  # Sprawdzamy, czy zawiera tylko cyfry
            return False
        return True

    def check_age(self):
        pesel = str(self.person.pesel)
        if not self.check_pesel():
            raise ValueError("Nieprawidłowy numer PESEL")

        # Rozkodowanie daty urodzenia
        year = int(pesel[0:2])
        month = int(pesel[2:4])
        day = int(pesel[4:6])

        # Ustalanie stulecia
        if 1 <= month <= 12:
            year += 1900
        elif 21 <= month <= 32:
            year += 2000
            month -= 20
        elif 41 <= month <= 52:
            year += 2100
            month -= 40
        elif 61 <= month <= 72:
            year += 2200
            month -= 60
        elif 81 <= month <= 92:
            year += 1800
            month -= 80
        else:
            raise ValueError("Nieprawidłowy miesiąc w numerze PESEL")

        # Obliczanie wieku
        birth_date = datetime(year, month, day)
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        return age
