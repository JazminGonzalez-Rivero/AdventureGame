from wobject import *
from player import *

class Room (WObject): #,Container):

    rooms = []

    def __init__ (self,name, description):
        WObject.__init__(self,name)
        self._description = description
        self._exits = {}
        self._contents = []
        Room.rooms.append(self)

    def exits (self):
        return self._exits

    def description(self):
        return self._description

    def contents (self):
        return self._contents

    # You see room reports only if you are in the same room
    # or if you have enabled god mode

    def report (self,msg):
        if Player.me.location() is self:
            print msg
        elif Player.god_mode:
            print '(At', self.name(), msg+')'

    def broadcast (self,msg):
        print msg

    def is_room (self):
        return True

    #Rooms are now checked in verbs, 
    #so we had to make sure they couldn't be taken or error the program
    def take(self, actor):
        actor.say("I can't take a room")

    def have_thing (self,t):
        for c in self.contents():
            if c is t:
                return True
        return False

    def add_thing (self,t):
        self._contents.append(t)

    def del_thing (self,t):
        self._contents = [x for x in self._contents if x is not t]
