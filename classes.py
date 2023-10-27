import pickle

from collections import UserDict, defaultdict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return super().__str__()


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Invalid phone number format")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phones(self, *phones):
        for phone in phones:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)

    def del_phone(self, phone_to_remove) -> bool:
        for phone_obj in self.phones:
            if phone_obj.value == phone_to_remove:
                self.phones.remove(phone_obj)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", Birthday: {self.birthday.value}" if hasattr(self, 'birthday') else ""
        return f"Contact {self.name}, Phones: {phone_str}{birthday_str}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
        except Exception as e:
            print(f"An error occurred while loading the address book: {e}")

    def get_birthdays_per_week(self):
        birthdays_by_day = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            if hasattr(record, 'birthday'):
                name = record.name.value
                birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                birthday_this_year = birthday.replace(year=today.year)

                if today <= birthday_this_year <= today + timedelta(days=6):
                    birthday_day = birthday_this_year.strftime("%A")

                    if birthday_day in ["Saturday", "Sunday"]:
                        birthday_day = "Monday"
                    birthdays_by_day[birthday_day].append(name)

        upcoming_birthdays = []
        for day, names in birthdays_by_day.items():
            upcoming_birthdays.append(f"{day}: {', '.join(names)}")

        return upcoming_birthdays
