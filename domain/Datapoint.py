
class Datapoint:
    datetime = None
    price = None

    def __init__(self, datetime, price):
        self.datetime = datetime
        self.price = price

    def __str__(self):
        return str(self.price)