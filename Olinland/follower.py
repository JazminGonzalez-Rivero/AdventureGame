from player import *
from person import *
import random

class Follower (Person):
    def __init__ (self,name,loc,restlessness,miserly,leader,health,inventory,description):
        Person.__init__(self,name,loc,description)
        self._restlessness = restlessness
        self._miserly = miserly
        self._leader = leader
        self._recentlyLeft = True

        self._health = health
        self._inventory = inventory

        Player.clock.register(self.move_and_take_stuff, 6)
        
    def move_and_take_stuff (self,time):
        if not self.is_in_limbo() and self._restlessness != 0:
            if random.randrange(self._restlessness) == 0:
                self.move_somewhere()
            elif self._recentlyLeft == True and self._leader.location() != self.location():
                self._recentlyLeft = False
                self._leader.say("Finally, I've left " + self.name() + " behind!")
            if random.randrange(self._miserly) == 0:
                self.take_something()

    def take_something (self):
        everything = []
        everything.extend(self.stuff_around())
        everything.extend(self.peek_around())
        if everything:
            something = random.choice(everything)
            something.take(self)

    def move_somewhere(self):
        if self._leader.location() != self.location():
            self.location().del_thing(self)
            self._leader.location().add_thing(self)
            self._location = self._leader.location()
            self.say("Wait for me " + self._leader.name() + "-sempai!")
            self._recentlyLeft = True
        else:
            self.say("Can we go " + self._leader.name() + "-sempai?")
            self.say("Please?")
            self.say("Please?")
            self.say("Please?")
            self.say("Please?")
            self.say("I'm boooooorreeeeeddddd!!!!")

    def die (self):
        self.say('SHREEEEEK! I, uh, suddenly feel very faint...')
        self._leader.say("Alas, poor " + self.name() + " has died.")
        Person.die(self)