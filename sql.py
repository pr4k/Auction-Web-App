import sqlite3
db=sqlite3.connect("devnew.db")
cursor=db.cursor()
cursor.execute('''CREATE TABLE User(
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT,
    bio TEXT,
    conf_key TEXT,
    emailconf TEXT,
    picturefilename TEXT);''')
cursor.execute('''CREATE TABLE Product(
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    picturefilename TEXT,
    user TEXT,
    minbid INT,
    deadline TEXT);''')
cursor.execute('''CREATE TABLE Bids(
    id TEXT PRIMARY KEY,
    user TEXT,
    product TEXT,
    bidamount INT);'''
    )
db.commit()
db.close()
