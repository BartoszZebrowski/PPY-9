from car import Car

class Booking:
    
    def __init__(self, userId, car, dateFrom, days):
        self.car = car
        self.userId = userId
        self.dateFrom = dateFrom
        self.days = days
        self.cost = self.car.costPerDay * days
        
        
    def getJson(self):
        return {
            "carId": self.car.id,
            "userId": self.userId,
            "dateFrom": str(self.dateFrom),
            "days": self.days,
            "cost": self.cost
        }
        
    @staticmethod    
    def mapFromJson(json, cars):
        car = cars[int(json["carId"]) - 1]
        return Booking(json["userId"],car, json["dateFrom"], json["days"])