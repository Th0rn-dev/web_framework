import sqlite3
import os
import pytest

from bumboo.orm import Database, Table, Column, ForeignKey

# tests


def test_create_db(db):
    db = Database("./test.db")

    assert isinstance(db.conn, sqlite3.Connection)
    assert db.tables == []


def test_define_tables(db, Author, Book):
    assert Author.name.type == str
    assert Book.author.table == Author

    assert Author.name.sql_type == "TEXT"
    assert Author.age.sql_type == "INTEGER"


def test_create_tables(Author, Book):
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    db = Database("./test.db")

    db.create(Author)
    db.create(Book)

    assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
    assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"

    for table in ("author", "book"):
        assert table in db.tables


def test_create_author_instance(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=38)

    assert john.name == "John Doe"
    assert john.age == 38
    assert john.id is None


def test_save_author_instance(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=23)
    db.save(john)

    assert john._get_insert_sql() == (
        "INSERT INTO author (age, name) VALUES (?, ?);",
        [23, "John Doe"]
    )

    assert john.id == 1

    man = Author(name="Man Harsh", age=28)
    db.save(man)
    assert man.id == 2

    vik = Author(name="Vik Star", age=43)
    db.save(vik)
    assert vik.id == 3

    jack = Author(name="Jack Ma", age=39)
    db.save(jack)
    assert jack.id == 4


def test_query_all_authors(db, Author):
    db.create(Author)
    jack = Author(name="Jack Ma", age=39)
    vik = Author(name="Vik Star", age=43)
    db.save(jack)
    db.save(vik)

    authors = db.all(Author)

    assert Author._get_select_all_sql() == (
        "SELECT id, age, name FROM author;",
        ["id", "age", "name"]
    )
    assert len(authors) == 2
    assert type(authors[0]) == Author
    assert {a.age for a in authors} == {39, 43}
    assert {a.name for a in authors} == {"Jack Ma", "Vik Star"}


def test_get_author(db, Author):
    db.create(Author)
    roman = Author(name="Roman Auth", age="48")
    db.save(roman)

    roman_from_db = db.get(Author, id=1)

    assert Author._get_select_where_sql(id=1) == (
        "SELECT id, age, name FROM author WHERE id=?;",
        ["id", "age", "name"],
        [1]
    )

    assert type(roman_from_db) == Author
    assert roman_from_db.age == 48
    assert roman_from_db.name == "Roman Auth"
    assert roman_from_db.id == 1


def test_get_book(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name="John Doe", age=45)
    arash = Author(name="Arach Kun", age=60)

    book1 = Book(title="Building an ORM", published=False, author=john)
    book2 = Book(title="Scoring Goals", published=False, author=arash)

    db.save(john)
    db.save(arash)
    db.save(book1)
    db.save(book2)

    book_from_db = db.get(Book, 2)

    assert book_from_db.title == "Scoring Goals"
    assert book_from_db.author.name == "Arach Kun"
    assert book_from_db.id == 2


def test_update_author(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=45)
    db.save(john)

    john.age = 50
    john.name = "John Update"
    db.update(john)

    john_from_db = db.get(Author, id=john.id)

    assert john_from_db.age == 50
    assert john_from_db.name == "John Update"


def test_delete_author(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=45)
    db.save(john)

    db.delete(Author, id=1)

    with pytest.raises(Exception):
        db.get(Author, 1)