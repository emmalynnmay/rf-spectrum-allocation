from radiograph.system import *

class RadioFrequency:
    """
    Represents a radio frequency band for use by different users in the grid.
    """
    def __init__(self, sim: Simulation, id, freq, user=None):
        self.id = id
        self.frequency = freq
        if user:
            self.assigned_to = [user]
        else:
            self.assigned_to = []
        self.is_active = False
    
    def __str__(self):
        return f"[Frequency {self.frequency} ({self.id})]"
    
    def new_user_assigned(self, user, verbose=True):
        for existing_user in self.assigned_to:
            if is_not_out_of_range(user, existing_user):
                if verbose:
                    print(f"{user} cannot transmit on this frequency because they are within range of {existing_user}.")
                return False
        self.assigned_to.append(user)
        return True

    def user_unassigned(self, user):
        if user in self.assigned_to:
            self.assigned_to.remove(user)

class RadioFrequencySpectrum:
    """
    Represents a range of frequency bands.  Generally intended for authorized
    users to indicate their assigned bands which they may lease out.
    """
    def __init__(self, sim: Simulation, *freqs):
        self.frequencies = freqs


    def __getitem__(self, index):
        return self.frequencies[index]


    def __contains__(self, item):
        return item in self.frequencies


    def get_frequency(self, id):
        """
        Search for a radio frequency by `id` and returns that frequency, 
        or `None` if not found.
        """
        for f in self.frequencies:
            if f.id == id:
                return f
        return None
