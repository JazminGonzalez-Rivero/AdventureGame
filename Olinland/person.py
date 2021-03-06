from mobile import *

class Person (MobileThing):    # Container...

    def __init__ (self,name,loc,description):
        MobileThing.__init__(self,name,loc,description)
        self._max_health = 3
        self._health = self._max_health
        self._inventory = []

    def health (self):
        return self._health

    def inventory (self):
        return self._inventory

    def add_thing(self, t):
        self._inventory.append(t)

    def del_thing (self,t):
        self._inventory = [x for x in self._inventory if x is not t]

    def reset_health (self):
        self._health = self._maxHealth

    def say (self,msg):
        loc = self.location()
        loc.report(self.name()+' says -- '+msg)

    #To account for objects leaving your inventory (like a teleporter)
    def report(self,msg):
        self.say(msg)

    def have_fit (self):
        self.say('Yaaaaah! I am upset!')

    def people_around (self):
        return [x for x in self.location().contents()
                    if x.is_person() and x is not self]

    def trolls_around(self):
        return [x for x in self.location().contents() if x.is_troll()]

    def stuff_around (self):
        if self.location().contents() != None:  #Fixing a glitch, maybe?
            return [x for x in self.location().contents() if not x.is_person()]


    # this function should return everything that everyone in the
    # same location as this person are holding/carrying

    def peek_around (self):
        things_around = []
        if self.people_around():
            for person in self.people_around():
                if person.inventory():
                    for item in person.inventory():
                        things_around.append(item)
        return things_around


    def lose (self,t,loseto):
        self.say('I lose ' + t.name())
        self.have_fit()
        t.move(loseto)
    
    def go (self,direction):
        loc = self.location()
        exits = loc.exits()
        if direction in exits:
            t = exits[direction]
            self.leave_room()
            loc.report(self.name()+' moves from '+ loc.name()+' to '+t.name())
            self.move(t)
            self.enter_room()
            return True
        else:
            print 'No exit in direction', direction
            return False


    def suffer (self,hits):
        self.say('Ouch! '+str(hits)+' hits is more than I want!')
        self._health -= hits
        if (self.health() < 0):
            self.die()
        else:
            self.say('My health is now '+str(self.health()))

    def die (self):
        self.location().broadcast('An earth-shattering, soul-piercing scream is heard...')
        if self._inventory:
            for item in self._inventory:
                item.drop(self)
        self.destroy()   
        self.deregister()   

    def deregister(self):
        pass

    def enter_room (self):
        people = self.people_around()
        if people:
            self.say('Hi ' + ', '.join([x.name() for x in people]))

    def leave_room (self):
        pass   # do nothing to reduce verbiage

    def have_thing (self,t):
        for c in self.inventory():
            if c is t:
                return True
        return False

    def take (self,actor):
        actor.say('I am not strong enough to just take '+self.name())

    def drop (self,actor):
        print actor.name(),'is not carrying',self.name()

    def give (self,actor,target):
        print actor.name(),'is not carrying',self.name()
        
    def accept (self,obj,source):
        obj.move(self)
        self.say('Thanks, ' + source.name())

    def is_person (self):
        return True
