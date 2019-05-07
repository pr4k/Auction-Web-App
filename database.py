from peewee import *
db = SqliteDatabase("devnew.db")

class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	id=CharField()
	name = CharField()
	email = CharField()
	password = CharField()
	bio = TextField()
	conf_key = CharField()
	emailconf = BooleanField(default=False)
	picturefilename = CharField()

class Product(BaseModel):
	id=TextField()
	name = CharField()
	description = TextField()
	picturefilename = CharField()
	user = CharField()
	minbid=IntegerField()
	deadline = CharField()

class Bids(BaseModel):
	id=TextField()
	user = CharField() #id of user placing bid
	product = TextField() #id of product
	bidamount = IntegerField()