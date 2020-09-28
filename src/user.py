from src.db import Users


class User:
    def __init__(self):
        self._id = None
        self._full_name = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        if not Users.contains(new_id):
            Users.create_new(new_id)
            self._id = new_id

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, new_full_name):
        Users.update_full_name(self.id, new_full_name)
