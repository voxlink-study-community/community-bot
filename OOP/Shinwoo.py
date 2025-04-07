class Laptop():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def print_price(self):
        print(f"{self.name}'s price : {self.price} ")

class Macbook(Laptop):

    def only_Mac(self):
        print("Macbook is the only valid ticket for Starbucks")


class Coke():
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.cal = "high"
    
    def print_cal(self):
        print(f"{self.name}'s calories is {self.cal}")

class ZeroCoke(Coke):
    def __init__(self, name, price):
        super().__init__(name, price)
        self.cal = "zero"


myzero = ZeroCoke("myzero","800")
myzero.print_cal()


class Animal():
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

class Dog(Animal):
    def speak(self):  # 오버라이딩
        print(f"{self.name} says: Woof!")

    def fetch(self):
        print(f"{self.name} is fetching the ball.")


class Game():
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre

    def play(self):
        print(f"Playing {self.title}, genre: {self.genre}")

class FPSGame(Game):
    def __init__(self, title, weapon):
        super().__init__(title, genre="FPS")
        self.weapon = weapon

    def play(self):  # 오버라이딩
        print(f"Shooting in {self.title} with a {self.weapon}!")
