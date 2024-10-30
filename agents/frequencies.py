class RadioFrequency:
    """
    Represents a radio frequency band for use by different users in the grid.
    """
    def __init__(self, id, freq, user=None):
        self.id = id
        self.frequency = freq
        self.assignedTo = user
    
    def __str__(self):
        return f"[Frequency {self.frequency} ({self.id})]"



class RadioFrequencySpectrum:
    """
    Represents a range of frequency bands.  Generally intended for authorized
    users to indicate their assigned bands which they may lease out.
    """
    def __init__(self, *freqs):
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
