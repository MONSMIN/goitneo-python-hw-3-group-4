from faker import Faker
from classes import AddressBook, Record, Name, Phone, Birthday
from prettytable import PrettyTable


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Not enough params. Print help"
        except KeyError:
            return "Contact not found."

    return inner


@input_error
def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args, contacts):
    name, *phones = args
    new_record = Record(name)
    for phone in phones:
        new_record.add_phones(phone)
    contacts.add_record(new_record)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated phone: {old_phone} -> {new_phone}"
    else:
        raise KeyError


@input_error
def remove_phone(args, contacts):
    name, phone_to_remove = args
    record = contacts.find(name)
    if record:
        if record.del_phone(phone_to_remove):
            return f"Phone {phone_to_remove} removed from contact {name}."
        else:
            return f"Phone {phone_to_remove} not found in contact {name}."
    else:
        raise KeyError


@input_error
def remove_contact(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record:
        contacts.delete(name)
        return f"Contact {name} removed from Address Book!"
    else:
        raise KeyError


@input_error
def show_phone(args, contacts):
    name, *_phones = args
    record = contacts.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return f"Phones: {phones}, contact {name}!"
    else:
        raise KeyError


def show_all(contacts):
    if not contacts.data:
        return "Address book is empty."
    else:
        table = PrettyTable()
        table.field_names = ["\033[92mName\033[0m", "\033[92mPhones\033[0m", "\033[92mBirthday\033[0m"]
        table.align["Name"] = "l"

        for record in contacts.values():
            phones = ', '.join(p.value for p in record.phones)
            birthday = getattr(record, 'birthday', '')
            table.add_row([record.name, phones, birthday])

        return str(table)


@input_error
def add_birthday(args, contacts):
    name, birthday = args
    record = contacts.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}: {birthday}"
    else:
        raise KeyError


@input_error
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record and hasattr(record, 'birthday'):
        return f"Birthday of {name}: {record.birthday.value}"
    else:
        raise KeyError(f"Contact {name} not found or birthday not set.")


@input_error
def birthdays(contacts):
    upcoming_birthdays = contacts.get_birthdays_per_week()
    if upcoming_birthdays:
        return f"Upcoming birthdays: {', '.join(upcoming_birthdays)}"
    else:
        return "No upcoming birthdays in the next week."


@input_error
def clear_all(contacts, *args):
    yes_no = input('Are you sure you want to delete all users? (y/n) ')
    if yes_no == 'y':
        contacts.clear()
        contacts.save_to_file('address_book.pkl')
        return 'Address book is empty'
    else:
        return 'Removal canceled'


def fake_contacts(args, contacts):
    num_contacts = int(args[0])

    fake = Faker()
    for _ in range(num_contacts):
        name = fake.first_name()
        phone = str(fake.random_int(min=1000000000, max=9999999999))
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=100)
        formatted_birthday = birthday.strftime('%d.%m.%Y')
        new_record = Record(name, Birthday(formatted_birthday))
        new_record.add_phones(phone)
        contacts.add_record(new_record)

    return f"Generated {num_contacts} fake contacts."
