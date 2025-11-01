# -----------------------------------------------------------------------
# -------------------------TASK DESCRIPTION------------------------------
# -----------------------------------------------------------------------
'''
Розробіть систему для управління адресною книгою.



Сутності:

Field: Базовий клас для полів запису.
Name: Клас для зберігання імені контакту. Обов'язкове поле.
Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
AddressBook: Клас для зберігання та управління записами.


Функціональність:

AddressBook:Додавання записів.
Пошук записів за іменем.
Видалення записів за іменем.
Record:Додавання телефонів.
Видалення телефонів.
Редагування телефонів.
Пошук телефону.

Критерії оцінювання

Клас AddressBook:

Реалізовано метод add_record, який додає запис до self.data.
Реалізовано метод find, який знаходить запис за ім'ям.
Реалізовано метод delete, який видаляє запис за ім'ям.


Клас Record:

Реалізовано зберігання об'єкта Name в окремому атрибуті.
Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
Реалізовано методи для додавання - add_phone/видалення - remove_phone/редагування - edit_phone/пошуку об'єктів Phone - find_phone.


Клас Phone:

Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр).

'''
# -----------------------------------------------------------------------
# -------------------------TASK SOLUTION---------------------------------
# -----------------------------------------------------------------------

import re
from collections import UserDict

# -----------------------------------------------------------------------
# ---------------------------Classes-----------------------------------
# -----------------------------------------------------------------------

# Base Field class
class Field:
    def __init__(self, value):
        self.value = self._normalize(value)

    def _normalize(self, v):
        return v

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.value == other.value

# Name field with validation
class Name(Field):
    ALLOWED = re.compile(r'^[A-Za-z]{3,}\s+[A-Za-z]{3,}$')

    def _normalize(self, raw):
        s = re.sub(r'\s+', ' ', raw.strip())
        if not s:
            raise ValueError("Name is empty")
        if not self.ALLOWED.fullmatch(s):
            raise ValueError("Name must be in full format, for example 'Albert Einstein'")
        return " ".join(p.capitalize() for p in s.split(" "))
    
      
# Phone field with validation
class Phone(Field):
    def _normalize(self, raw: str) -> str:
        s = raw.strip()
        digits = re.sub(r"\D", "", s)
        if len(digits) != 10:
            raise ValueError("Phone must have 10 digits")
        return digits
       

# Record class
# stores Name and list of Phones    
class Record:
    def __init__(self, name_str: str):
        self.name = Name(name_str)
        self._phones: list[Phone] = [] # incapsulated list of Phone objects

    def get_phones(self) -> tuple[Phone, ...]:
        # return a copy to prevent direct modification
        return tuple(self._phones)

    def add_phone(self, phone_str: str) -> None:        
        phone = Phone(phone_str)
        if phone in self._phones:
            raise ValueError("Such number exists for contact")
        else:
            self._phones.append(phone)

    def remove_phone(self, phone_str: str):
        phone = Phone(phone_str)
        if not phone in self._phones:
            raise ValueError("Such number doesn't exist for contact")
        else:
            self._phones.remove(phone)

    def edit_phone(self, phone_str: str, new_phone_str: str):
        phone = Phone(phone_str)
        new_phone = Phone(new_phone_str)
        if phone not in self._phones:
            raise ValueError("Such number doesn't exist for contact")
        if new_phone in self._phones:
            raise ValueError("New phone number already exists for contact")
        self._phones.remove(phone)
        self._phones.append(new_phone)

    def find_phone(self, phone_str: str) -> Phone:
        phone = Phone(phone_str)
        if not phone in self._phones:
            raise ValueError("Such number doesn't exist for contact")
        else:
            return self._phones[self._phones.index(phone)]

    def __str__(self):
        nums = "; ".join(p.value for p in self._phones)
        nums = nums if nums else "—"
        return f"Contact name: {self.name.value}, phones: {nums}"

# AddressBook class
# stores Records in UserDict
class AddressBook(UserDict):

    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise ValueError("Such name already exists in address book")
        
        self.data[record.name.value] = record

    def find(self, name_str:str) -> Record:
        try:
            key = Name(name_str).value
        except ValueError:
            raise KeyError("No such name in address book")
        return self.data[key]
    
    def delete(self, name_str:str):
        try:
            key = Name(name_str).value
        except ValueError:
            raise KeyError("No such name in address book")
        del self.data[key]

# -----------------------------------------------------------------------
# ---------------------------Example Usage-------------------------------
# -----------------------------------------------------------------------

def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John Johnson")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane Johnson")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for _, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John Johnson")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane Johnson")

if __name__ == "__main__":
    main()
    