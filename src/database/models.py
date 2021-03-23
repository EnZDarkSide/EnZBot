from tortoise.fields import IntField, CharField
from tortoise.models import Model


"""
A model was made to work with DatabaseBranch manager
Three fields are required: uid as integer, branch as string (near 20 symbols max)
and context as string (as big as possible) to store context json
"""


class UserState(Model):
    id = IntField(pk=True)  # Primary key is often recommended
    uid = IntField()
    branch = CharField(20)
    context = CharField(255)

    class Meta:
        database = "user_state"