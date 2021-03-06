class User:
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

    # 在检查是否重复时，用于比较两个uesr相等与否
    def __eq__(self, other):
        return self.name == other.name


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

        # 每个频道最多保留100条消息
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]

    def add_user(self, user: User):
        self.users.append(user)

    # 在检查是否重复时，用于比较两个chanel相等与否
    def __eq__(self, other):
        return self.index == other.index
