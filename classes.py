class User:
    def __init__(self, id, name, channel):
        self.id = id
        self.name = name
        self.channel = channel


class Message:
    def __init__(self, author, message):
        self.author = author
        self.message = message


class Channel:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.messages = []
        self.users = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def add_user(self, user: User):
        self.users.append(user)
