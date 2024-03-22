from classes import AddressBook, Record
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Enter the argument for the command"
        except Exception as e:
            return f"{e}"
    return inner
     
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def save_data(book,filename="addressbook.pkl"): 
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 
    
@input_error
def add_birthday(args, book:AddressBook):
    name, date = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(date)
    return 'Birthday added'

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Name Not Found"
    return record.birthday

@input_error
def birthdays(args,book: AddressBook):
    return book.get_upcoming_birthdays()    

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)              
        book.add_record(record)        
    record.add_phone(phone)
    return "Contact added"

@input_error
def change_contact(args, book:AddressBook):
    name,old_phone,new_phone = args
    record = book.find(name)
    if not record:
        return "Name Not Found"    
    record.edit_phone(old_phone,new_phone)
    return "Contact updated"

@input_error   
def phone_username(args, book:AddressBook):
    phone = args[0]
    record = book.find(phone)
    if not record:
        return "Contact Not Found"
    return '; '.join(str(phone) for phone in record.phones)

@input_error
def show_all(args,book:AddressBook):
    return book   


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "all":
            print(show_all(args,book))
        elif command == "hello":
            print("How can I help you?")
        elif command == "change":
            print(change_contact(args, book))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "phone":
            print(phone_username(args,book))
        elif command == "birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))        
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()