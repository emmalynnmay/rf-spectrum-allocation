#from colorama import Fore, Style

from radiograph.agents.coguser import *
from radiograph.agents.frequencies import *

TRANSMIT_DISTANCE = 3 #the max distance from a user that radio transmissions can still be picked up
#COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW]

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
    
def display_sim_state(spectrum, auth_users, cog_users):
    #TODO: add colors

    all_users = auth_users + cog_users

    #Display real space with the ranges of each user
    print("\nReal Space (not entirely mathematically accurate):")

    # Determine grid size for real space
    max_x = max(user.posX for user in all_users) + TRANSMIT_DISTANCE
    max_y = max(user.posY for user in all_users) + TRANSMIT_DISTANCE
    grid_size = max(max_x, max_y) + 1

    real_space = [[" " for _ in range(grid_size)] for _ in range(grid_size)]

    real_space[0][0] = "+"

    def check_in_range(val):
        return val < grid_size and val >= 0
    
    def plot_range(x, y):
        real_space[x][y] = "."
        #real_space_colors[x][y] = color

    for user in all_users:
        real_space[user.posX][user.posY] = user.id
        #real_space_colors[user.posX][user.posY] = COLORS[color]

        for dist in range(1, TRANSMIT_DISTANCE + 1):
            newXPos = user.posX + dist
            newYPos = user.posY + dist
            newXNeg = user.posX - dist
            newYNeg = user.posY - dist
            if check_in_range(newXPos):
                plot_range(newXPos, user.posY)
            if check_in_range(newXNeg):
                plot_range(newXNeg, user.posY)
            if check_in_range(newYPos):
                plot_range(user.posX, newYPos)
            if check_in_range(newYNeg):
                plot_range(user.posX, newYNeg)

            if check_in_range(newYNeg) and check_in_range(newXNeg):
                plot_range(newXNeg, newYNeg)
            if check_in_range(newYNeg) and check_in_range(newXPos):
                plot_range(newXPos, newYNeg)
            if check_in_range(newYPos) and check_in_range(newXNeg):
                plot_range(newXNeg, newYPos)
            if check_in_range(newYPos) and check_in_range(newXPos):
                plot_range(newXPos, newYPos)
    
    print_cartesian(real_space)

    #Display the rf spectrum, who owns which frequency, and who is currently broadcasting on it
    print("\nRadio Spectrum:")
    for freq in spectrum.frequencies:
        print(freq.frequency)
        if freq.assignedTo:
            print(f"   - User {freq.assignedTo.id} is actively broadcasting")
        else:
            print(f"   - No active broadcast")
        for user in auth_users:
            if freq in user.assignedFrequencies:
                print(f"   - Frequency owned by authorized user {user.id}")

def print_cartesian(input_data):
    for row in input_data:
        print("-", end ="-")
    print("")

    for row in reversed(input_data):
        for cell in row:
            print("", end ="")
            print(cell, end =" ")
        print("|")
    
    print("", end ="")
    for row in input_data:
        print("-", end ="-")
    print("")

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

    print("\nCreating an authorized user with control over all frequencies in spectrum")
    auth = AuthorizedUser(2, 2, 2, spectrum)
    print(auth, f"located at {auth.position}")

    #Authorized users have dedicated frequencies and can “rent” them out to cognitive users when they are not using them
    print(f"\nAuthorized user is renting out {freq3} to {cog}")
    auth.grant_frequency(freq3, cog)
    print(cog)

    last_cog = CognitiveUser(4, 5, 12)
    auth.grant_frequency(freq1, last_cog)

    #Users can broadcast on frequencies
    cog.begin_broadcasting()
    auth.begin_broadcasting()

    cog.stop_broadcasting()

    #We can visualize the state of the simulation easily
    #We can look at the rf spectrum and see who is using what at any given time 
         #(including which authorized users are renting to which cognitive users)
    display_sim_state(spectrum, [auth], [cog, other_cog])

    #Multiple users can broadcast on the same frequency if they are further apart than a defined constant distance in real space


emma_tests()