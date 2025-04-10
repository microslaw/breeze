from backend.datatypes import NodeType

# data in .csv files will create a following workflow:
# +--+
# |n0|->\
# +--+   \     +--+
#         +--> |n2|->\
# +--+   /     +--+   \   +--+
# |n1|->/              +->|n4|
# +--+         +--+   /   +--+
#              |n3|->/
#              +--+
# +--+
# |n6|->\
# +--+   \     +--+
#         +--> |n7|->\
# +--+   /     +--+   \   +--+
# |n5|->+--------------+->|n8|
# +--+                    +--+
#
#


@NodeType
def add_int(a: int, b: int) -> int:
    return a + b


@NodeType
def const_1():
    return 1


@NodeType
def const_2():
    return 2


@NodeType
def const_a():
    return "a"
