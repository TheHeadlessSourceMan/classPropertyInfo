from ._classPropertyInfo import getClassPropertyComments


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