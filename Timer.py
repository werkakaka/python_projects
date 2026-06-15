class Time_descriptor:
    def __init__(self,name, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} musi byc int!!!")
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"Wartosc {self.name} musi byc pomiedzy {self.min_val} a {self.max_val}")
        instance.__dict__[self.name] = value

class Date_descriptor:
    def __init__(self,name, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} musi byc int!!!")
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"Wartosc {self.name} musi byc pomiedzy {self.min_val} a {self.max_val}")
        instance.__dict__[self.name] = value

class Clock:
    hours = Time_descriptor("hours", 0, 23)
    minutes = Time_descriptor("minutes", 0, 59)
    seconds = Time_descriptor("seconds", 0, 59)

    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def set(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def tick(self):
        if self.seconds < 59:
            self.seconds += 1
        else:
            self.seconds = 0
            if self.minutes < 59:
                self.minutes += 1
            else:
                self.minutes = 0
                if self.hours < 23:
                    self.hours += 1
                else:
                    self.hours = 0
    def __str__(self):
        return f"{self.hours}-{self.minutes}-{self.seconds}"

    def __repr__(self):
        return f"Clock(hours={self.hours}, minutes={self.minutes}, seconds={self.seconds})"

    SEGMENTS = {
        '0': [" _ ",
              "| |",
              "|_|"],
        '1': ["   ",
              "  |",
              "  |"],
        '2': [" _ ",
              " _|",
              "|_ "],
        '3': [" _ ",
              " _|",
              " _|"],
        '4': ["   ",
              "|_|",
              "  |"],
        '5': [" _ ",
              "|_ ",
              " _|"],
        '6': [" _ ",
              "|_ ",
              "|_|"],
        '7': [" _ ",
              "  |",
              "  |"],
        '8': [" _ ",
              "|_|",
              "|_|"],
        '9': [" _ ",
              "|_|",
              " _|"],
        ':': ["   ",
              " . ",
              " . "]
    }

    def display(self):
        time_str = f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
        lines = ["", "", ""]
        for ch in time_str:
            seg = self.SEGMENTS[ch]
            for i in range(3):
                lines[i] += seg[i] + " "
        for line in lines:
            print(line)





print("=== Clock Test ===")
c = Clock(23, 59, 58)
print("Current time:", c)
c.display()
c.tick()
print("After tick:", c)
c.display()
c.tick()
print("After tick:", c)
c.display()
