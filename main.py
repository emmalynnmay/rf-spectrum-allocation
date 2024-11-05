#from colorama import Fore, Style

from radiograph.agents.coguser import *
from radiograph.agents.frequencies import *
from radiograph.system import *

def calvin_tests():
    f1 = RadioFrequency(1, 107.9)
    f2 = RadioFrequency(2, 103.5)
    f3 = RadioFrequency(3, 99.9)
    print(f1)
    print(f2)
    print(f3)

    sp = RadioFrequencySpectrum(f1, f2, f3)
    c = CognitiveUser(1, -3, 4)
    print(c, f"located at {c.position}")
    a = AuthorizedUser(2, 2, -2, sp)
    print(a, f"located at {a.position}")
    c.set_frequency(f1)
    print(c)
    a.grant_frequency(f3, c)
    print(c)

    f4 = RadioFrequency(4, 87.9)
    assert c.activeFrequency is f3
    try:
        a.grant_frequency(f4, c)
    except IndexError:
        print("Good!  This call was SUPPOSED to fail.")
    else:
        raise IndexError("Something's wrong, I can feel it!")
    
#calvin_tests()

def emma_tests():
    print("Creating 3 radio frequencies")
    freq1 = RadioFrequency(1, 107.9)
    freq2 = RadioFrequency(2, 103.5)
    freq3 = RadioFrequency(3, 99.9)
    print(freq1, freq2, freq3)
    print("\nCreating a radio spectrum out of the frequencies")
    spectrum = RadioFrequencySpectrum(freq1, freq2, freq3)

    print("\nCreating a cognitive user")
    cog = CognitiveUser(1, 3, 4)
    print(cog, f"located at {cog.position}")

    print("\nCreating a cognitive user")
    other_cog = CognitiveUser(3, 5, 12)
    print(cog, f"located at {cog.position}")

    print("\nCreating an authorized user")
    auth = AuthorizedUser(2, 2, 2, freq3)
    print(auth, f"located at {auth.position}")

    #Authorized users have dedicated frequencies and can “rent” them out to cognitive users when they are not using them
    print(f"\nAuthorized user is renting out {freq3} to {cog}")
    auth.grant_frequency(freq3, cog)
    print(cog)

    #Users can broadcast on frequencies
    cog.begin_broadcasting()
    auth.begin_broadcasting()

    cog.stop_broadcasting()
    auth.begin_broadcasting()

    #We can visualize the state of the simulation easily
    #We can look at the rf spectrum and see who is using what at any given time 
         #(including which authorized users are renting to which cognitive users)
    display_sim_state(spectrum, [auth], [cog, other_cog])

    #Multiple users can broadcast on the same frequency if they are further apart than a defined constant distance in real space


emma_tests()