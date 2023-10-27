from address_book_handlers import *
from info import info


def main():


    """
The main function is the entry point of the program.
It creates an AddressBook object and loads it from a file, if possible.
Then it enters a loop that reads user input and executes commands until the user exits.

"""
    contacts = AddressBook()
    contacts.load_from_file('address_book.pkl')
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            contacts.save_to_file('address_book.pkl')
            print("Address book saved. Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "addbd":
            print(add_birthday(args, contacts))
        elif command == "showbd":
            print(show_birthday(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "del":
            print(remove_phone(args, contacts))
        elif command == "delete":
            print(remove_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "bd":
            print(birthdays(contacts))
        elif command == "boom":
            print(clear_all(contacts))
        elif command == "fake":
            print(fake_contacts(args, contacts))
        elif command == "help" or "info":
            print(info())
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
