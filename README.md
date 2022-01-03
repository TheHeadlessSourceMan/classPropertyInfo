# classPropertyInfo
Programmatically get information (such as comments) from python class member properties.

Even though the inspect module has useful-sounding tools such as inspect.getcomments(), the comments are actually not part of the syntax tree, and therefore, inaccessible.

I came across a need to get the comments for object properties such as

    myVal:int=4 # this describes what the value does

Therefore, I wrote this tool to be able to achieve that.

It does respect inheritence and class-level defined values, as well as pep484 type annotations and quotes.

    myVal:str=" # this is not actually a comment because its in quotes"

It has not yet been extensively tested.

Example useage:

    from classPropertyInfo import getClassPropertyComments

    class TestParent1:
        parent1ClassProperty=7 # good
    class TestParent2:
        parent2ClassProperty=7 # good
        def __init__(self):
            self.parent2MemberProperty=7 # good
            self.parent2OverriddenProperty=7 # bad
    class TestChild(TestParent1,TestParent2):
        childClassProperty=7 # good
        def __init__(self):
            self.childMemberProperty=7 # good
            self.parent2OverriddenProperty=7 # good
    # NOTE: should have 6 "good" comments
    print(getClassPropertyComments(TestChild()))
