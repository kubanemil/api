from datetime import datetime
from enum import Enum

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class Grade(Enum):
    Third = "Third"
    Second = "Second"
    First = "First"
    Special = "Special"


class Reach(Enum):
    Melee = "Melee"
    Ranged = "Ranged"


class User(Model):
    class Meta:
        table_name = "users"
        region = "ap-south-1"

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    age = NumberAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)


class Card(Model):
    class Meta:
        table_name = "cards"
        region = "ap-south-1"
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    image = UnicodeAttribute()
    attack = NumberAttribute()
    defense = NumberAttribute()
    ability = UnicodeAttribute()
    grade = UnicodeAttribute()
    reach = UnicodeAttribute()

    def save(self, conditional_operator=None, **expected_values):
        if self.grade not in [e.value for e in Grade]:
            raise ValueError("Invalid grade")
        if self.reach not in [e.value for e in Reach]:
            raise ValueError("Invalid reach")
        super(Card, self).save()


card = Card(
    id="123",
    name="Test",
    image="Test",
    attack=1,
    defense=1,
    ability="Test",
    grade=Grade.Third.value,
    reach=Reach.Melee.value,
)
