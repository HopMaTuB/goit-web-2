from datetime import datetime, timedelta
import datetime as dt
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value
    
    def is_valid(self,value):
        return True
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def if_valid(self,value):
        return bool(value)


class Phone(Field):
    def is_valid(self,value):
        return len(value)==10 and value.isdigit()

        
class Birthsday(Field):        
    def is_valid(self,value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except:
            return False
        return True
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = datetime.strptime(value, "%d.%m.%Y").date()
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        number=Phone(value) 
        if len(value) == 10 and value.isdigit():
            self.phones.append(number)

    def add_birthday(self,birthday):
        self.birthday = Birthsday(birthday)
        return self.birthday

    def remove_phone(self,phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
    
    def edit_phone(self, phone: str, new_phone: str):
        if self.find_phone(phone):
            self.remove_phone(phone)
            self.add_phone(new_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p                  

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {(self.birthday)}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)


    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        tdate=datetime.today().date()
        birthdays=[]

        for user in self.data.values():
            if user.birthday:
                birthday = user.birthday.value.replace(year=tdate.year)
                if birthday < tdate:
                    birthday = birthday.replace(year=tdate.year + 1)

                days_until_birthday = (birthday - tdate).days

                if 0 <= days_until_birthday < 7:
                    if birthday.weekday() >= 5:
                        birthday += timedelta(days=(7 - birthday.weekday()))

                    birthdays.append({
                        'name': user.name.value,
                        'congratulation': birthday.strftime('%d.%m.%Y')
                        })
        return birthdays      

        

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())




