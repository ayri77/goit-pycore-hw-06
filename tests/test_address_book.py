# test_address_book.py

import pytest
from src.bot import Field, Name, Phone, Record, AddressBook

# ---------- Name tests ----------

@pytest.mark.parametrize("raw,expected", [
    ("john johnson", "John Johnson"),
    ("  john   johnson  ", "John Johnson"),
    ("ALBERT EINSTEIN", "Albert Einstein"),
])
def test_name_normalization_basic(raw, expected):
    n = Name(raw)
    assert n.value == expected

@pytest.mark.parametrize("raw", [
    "", " ", "Jo", "John", "John  ", "Jo n", "J  J", "John 1", "John_J", "John-Johnson"
])
def test_name_validation_errors(raw):
    with pytest.raises(ValueError):
        Name(raw)

def test_name_equality_same_type_only():
    n1 = Name("John Johnson")
    n2 = Name("john  johnson")
    p = Phone("1234567890")
    assert n1 == n2
    assert not (n1 == p)

# ---------- Phone tests (exactly 10 digits) ----------

@pytest.mark.parametrize("raw,expected", [
    ("1234567890", "1234567890"),
    (" 123 456 7890 ", "1234567890"),
    ("(123) 456-7890", "1234567890"),
    ("123.456.7890", "1234567890"),
    ("+1 (234) 567-890", "1234567890"),
])
def test_phone_normalization(raw, expected):
    ph = Phone(raw)
    assert ph.value == expected

@pytest.mark.parametrize("raw", [
    "", "abcdef", "123456789", "12345678901", "123-456-78 9O"  # letter O at end
])
def test_phone_validation_errors(raw):
    with pytest.raises(ValueError):
        Phone(raw)

def test_phone_equality_same_type_only():
    p1 = Phone("123 456 7890")
    p2 = Phone("(123)456-7890")
    n = Name("John Johnson")
    assert p1 == p2
    assert not (p1 == n)

# ---------- Record tests ----------

def test_record_add_and_list_phones():
    r = Record("John Johnson")
    r.add_phone("1234567890")
    r.add_phone("555 555 5555")
    assert [p.value for p in r._phones] == ["1234567890", "5555555555"]

def test_record_add_duplicate_phone():
    r = Record("John Johnson")
    r.add_phone("1234567890")
    with pytest.raises(ValueError):
        r.add_phone("123 456 7890")  # duplicate after normalization

def test_record_remove_phone_success_and_fail():
    r = Record("John Johnson")
    r.add_phone("1234567890")
    r.remove_phone("123 456 7890")
    assert r._phones == []
    with pytest.raises(ValueError):
        r.remove_phone("1234567890")

def test_record_edit_phone_success():
    r = Record("John Johnson")
    r.add_phone("1234567890")
    r.edit_phone("1234567890", "1112223333")
    assert [p.value for p in r._phones] == ["1112223333"]

def test_record_edit_phone_to_existing_duplicate_rejected():
    r = Record("John Johnson")
    r.add_phone("1234567890")
    r.add_phone("5555555555")
    with pytest.raises(ValueError):
        r.edit_phone("1234567890", "555 555 5555")

def test_record_find_phone_returns_existing_instance():
    r = Record("John Johnson")
    r.add_phone("1234567890")
    found = r.find_phone("123 456 7890")
    # Must return the same object residing in r._phones
    assert found is r._phones[0]

# ---------- AddressBook tests ----------

def test_address_book_add_and_find_record():
    book = AddressBook()
    rec = Record("John Johnson")
    rec.add_phone("1234567890")
    book.add_record(rec)
    found = book.find("john   johnson")
    assert found is rec

def test_address_book_rejects_duplicate_name():
    book = AddressBook()
    book.add_record(Record("John Johnson"))
    with pytest.raises(ValueError):
        book.add_record(Record("john  johnson"))

def test_address_book_delete_success():
    book = AddressBook()
    book.add_record(Record("John Johnson"))
    book.delete("John Johnson")
    with pytest.raises(KeyError):
        _ = book.find("John Johnson")

def test_address_book_find_nonexistent_raises_keyerror():
    book = AddressBook()
    with pytest.raises(KeyError):
        _ = book.find("No Such Person")

def test_address_book_delete_nonexistent_raises_keyerror():
    book = AddressBook()
    with pytest.raises(KeyError):
        book.delete("No Such Person")
