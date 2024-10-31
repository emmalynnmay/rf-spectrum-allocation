from .frequencies import *

import abc
import math

class _UserBase(abc.ABC):
    """`
    An abstract class to encompass the similarities of both cognitive and authorized users.
    """
    def __init__(self, id, x, y):
        self.id = id
        self.posX = x
        self.posY = y

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
    a device user that can search for available frequency bands to
    """
    def __init__(self, id, x, y, freq: RadioFrequency=None):
        super().__init__(id, x, y)
        self.activeFrequency = freq

    @property
    def isActive(self):
        """
        Indicates whether this user is on an active frequency band.
        """
        return self.activeFrequency is not None


    def set_frequency(self, frequency: RadioFrequency):
        frequency.assignedTo = self
        self.activeFrequency = frequency
    

    def __str__(self):
        base = f"Cognitive User {self.id}"
        ext = f" on frequency {self.activeFrequency.frequency}" if self.activeFrequency else ""
        return f"[{base + ext}]"



class AuthorizedUser(_UserBase):
    """
    Represents an authorized user in the graph system.  Contra a cognitive user, authorized
    users have dedicated frequencies assigned to them, which they are permitted to "lease"
    to other cognitive users when not in use.
    """
    def __init__(self, id, x, y, freqs: RadioFrequencySpectrum):
        super().__init__(id, x, y)
        self.assignedFrequencies = freqs

    def grant_frequency(self, frequency: RadioFrequency, user: CognitiveUser):
        """
        Assigns to a `user` the given `frequency`, IF said frequency is assigned to this 
        authorized user.
        """
        if frequency not in self.assignedFrequencies:
            raise IndexError(f"{frequency} is not assigned to this authorized user ({self.id})")
        user.set_frequency(frequency)

    def __str__(self):
        return f"[Authorized User {self.id}]"
