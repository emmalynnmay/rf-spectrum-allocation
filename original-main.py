#from colorama import Fore, Style

from radiograph import frequencies, system, users, utilities
from data_generation import read_data

def calvin_tests():
    sim = system.Simulation()
    f1 = frequencies.RadioFrequency(sim, 1, 107.9)
    f2 = frequencies.RadioFrequency(sim, 2, 103.5)
    f3 = frequencies.RadioFrequency(sim, 3, 99.9)
    print(f1)
    print(f2)
    print(f3)

    sp = frequencies.RadioFrequencySpectrum(sim, f1, f2, f3)
    c = users.CognitiveUser(sim, 3, 4)
    print(c, f"located at {c.position}")
    a = users.AuthorizedUser(sim, 2, 2, f3)
    print(a, f"located at {a.position}")
    c.set_frequency(f1)
    print(c)
    a.grant_frequency(f3, c)
    print(c)

    f4 = users.RadioFrequency(sim, 4, 87.9)
    assert c.active_frequency is f3
    try:
        a.grant_frequency(f4, c)
    except IndexError:
        print("Good!  This call was SUPPOSED to fail.")
    else:
        raise IndexError("Something's wrong, I can feel it!")
    
calvin_tests()

def emma_tests():

    sim = system.Simulation()

    print("Creating 3 radio frequencies")
    freq1 = frequencies.RadioFrequency(sim, 1, 107.9)
    freq2 = frequencies.RadioFrequency(sim, 2, 103.5)
    freq3 = frequencies.RadioFrequency(sim, 3, 99.9)
    print(freq1, freq2, freq3)
    print("\nCreating a radio spectrum out of the frequencies")
    spectrum = frequencies.RadioFrequencySpectrum(sim, freq1, freq2, freq3)

    print("\nCreating a cognitive user")
    cog = users.CognitiveUser(sim, 3, 4)
    print(cog, f"located at {cog.position}")

    print("\nCreating a cognitive user")
    other_cog = users.CognitiveUser(sim, 5, 12)
    print(other_cog, f"located at {cog.position}")

    print("\nCreating an authorized user")
    auth = users.AuthorizedUser(sim, 2, 2, freq3)
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
    system.display_sim_state(spectrum, [auth], [cog, other_cog])

#emma_tests()
    
def test_data_files():
    sim = system.Simulation()
    data = read_data.get_small_dataset(sim)
    print(data)

#test_data_files()
