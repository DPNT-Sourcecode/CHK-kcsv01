

# noinspection PyUnusedLocal
# friend_name = unicode string
# "Hello, John!"
def hello(friend_name):
    title_name = ' '.join([x.title() for x in str(friend_name).split()])
    return "Hello, {}!".format(title_name)
