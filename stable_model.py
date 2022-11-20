class Stable:
    def __init__(self, adress, infrastructure):
        self.adress = adress
        self.infrastructure = infrastructure


class Adress:
    def __init__(self, city, district, state) -> None:
        self.city = city
        self.district = district
        self.state = state
