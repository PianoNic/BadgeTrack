from peewee import CharField, ForeignKeyField, IntegerField, Model


class Badge(Model):
    tag = CharField(max_length=200, unique=True)
    visits = IntegerField(default=0)
    created = IntegerField()


class Cookie(Model):
    cookie_id = CharField(max_length=64)
    badge = ForeignKeyField(Badge, backref="cookies")
    last_visit = IntegerField()

    class Meta:
        indexes = ((("cookie_id", "badge"), True),)
