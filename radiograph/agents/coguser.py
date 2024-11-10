from .frequencies import *
from ..system import *

import abc
import math

class _UserBase(abc.ABC):
    """`
    An abstract class to encompass the similarities of both cognitive and authorized users.
    """
    def __init__(self, sim, x, y):
        if x < 0 or y < 0:
            raise Exception("x & y positions must not be negative.")
        self.sim = sim
        self.id = self.sim.next_user_id()
        self.posX = x
        self.posY = y
        self.is_broadcasting = False

    @property
    def position(self):
        """
        Returns the coordinates of this user in traditional Cartesian form.
        """
        return (self.posX, self.posY)
    

    def distance_from(self, other):
        """
        Returns the Euclidean distance from some `other` user.
        """
        return math.sqrt((self.posX - other.posX) ** 2 + (self.posY - other.posY) ** 2)


class CognitiveUser(_UserBase):
    """
    Represents a cognitive user in the graph system.  A cognitive user, we have defined as
    a device user that can search for available frequency bands on which to communicate.
    """
    def __init__(self, sim: Simulation, x, y, freq: RadioFrequency=None):
        super().__init__(sim, x, y)
        self.activeFrequency = freq

    @property
    def isActive(self):
        """
        Indicates whether this user is on an active frequency band.
        """
        return self.activeFrequency is not None


    def set_frequency(self, frequency: RadioFrequency):
        if not frequency == None:
            frequency.assignedTo = self
        self.activeFrequency = frequency

    def begin_broadcasting(self):
        if (self.activeFrequency):
            self.is_broadcasting = True
            self.activeFrequency.is_active = True
            print(f"{self.id} has begun broadcasting on {self.activeFrequency}")
        else:
            raise Exception(f"{self.id} cannot begin broadcasting because it has no assigned frequency")

    def __str__(self):
        base = f"Cognitive User {self.id}"
        ext = f" on frequency {self.activeFrequency.frequency}" if self.activeFrequency else ""
        return f"[{base + ext}]"
    
    def stop_broadcasting(self):
        print(f"{self.id} has stopped broadcasting on {self.activeFrequency}")
        self.is_broadcasting = False
        self.activeFrequency.is_active = False



class AuthorizedUser(_UserBase):
    """
    Represents an authorized user in the graph system.  Contra a cognitive user, authorized
    users have dedicated frequencies assigned to them, which they are permitted to "lease"
    to other cognitive users when not in use.
    """
    def __init__(self, sim: Simulation, x, y, assigned_freq: RadioFrequency):
        super().__init__(sim, x, y)
        self.assignedFrequency = assigned_freq
        self.has_rented_frequency = False

    def grant_frequency(self, frequency: RadioFrequency, user: CognitiveUser):
        """
        Assigns to a `user` the given `frequency`, IF said frequency is assigned to this 
        authorized user.
        """
        if self.is_broadcasting:
            raise Exception("Frequency cannot be rented out when actively being broadcast on.")
        if frequency != self.assignedFrequency:
            raise IndexError(f"{frequency} is not assigned to this authorized user ({self.id})")
        user.set_frequency(frequency)
        self.has_rented_frequency = True

    def revoke_frequency(self, user: CognitiveUser):
        user.set_frequency(None)
        self.has_rented_frequency = False

    def begin_broadcasting(self):

        if self.is_broadcasting:
            print(f"{self.id} is already broadcasting...")
            return
        
        if self.try_freq(self.assignedFrequency):
            self.is_broadcasting = True
            print(f"{self.id} has begun broadcasting on {self.assignedFrequency}")
            self.assignedFrequency.assignedTo = self
            self.assignedFrequency.is_active = True
        else:
            print("Assigned frequency unavailable to begin broadcasting.")
        
    def try_freq(self, freq, steal=True):
        #Check to see if the requested frequency has been rented out
        #    If it is and isn't being used, take it back
        #    If it is and is being used, we can't take it

        if not self.has_rented_frequency:
            return True
        else:
            if steal:
                if freq.is_active:
                    print(f"{self.id} has rented out this frequency and it is being used, so we cannot broadcast on it.")
                    return False
                else:
                    print(f"{self.id} has rented out this frequency but it is not being used, so we'll take it back.")
                    self.revoke_frequency(freq.assignedTo)
                    return True
            else:
                print(f"{self.id} has rented out this frequency and it is being used, checking other options")
            
    
    def stop_broadcasting(self):
        print(f"{self.id} has stopped broadcasting on {self.assignedFrequency}")
        self.is_broadcasting = False
        self.assignedFrequency.is_active = False

    def __str__(self):
        return f"[Authorized User {self.id}]"
