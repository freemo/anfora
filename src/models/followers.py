import datetime

from peewee import (ForeignKeyField, BooleanField, DateTimeField)

from models.base import BaseModel
from models.user import User

class FollowerRelation(BaseModel):

    user = ForeignKeyField(User)
    follows = ForeignKeyField(User)
    valid = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
        (('user', 'follows'), True),
        )

    def __str__(self):
        return "{} follows {}".format(self.user.username, self.follows.username)
