
from radiograph import frequencies, system, users, utilities
from data_generation import read_data
from algorithms.coloring import allocate_with_coloring

def allocate_freqs(spectrum, auths, cogs, verbose=True):
    willing_to_rent = []

    if verbose:
        print("Authorized users willing to rent out their frequency:")
    for auth in auths:
        if not auth.wants_to_broadcast_now:
            if verbose:
                print(f" - {auth}")
            willing_to_rent.append(auth)
        else:
            auth.begin_broadcasting(False)

    want_to_rent = []
    if verbose:
        print("Cognitive users who want to rent a frequency:")
    for cog in cogs:
        if cog.wants_to_broadcast_now:
            if verbose:
                print(f" - {cog}")
            want_to_rent.append(cog)
    if verbose:
        print("")

    allocate_with_coloring(willing_to_rent, want_to_rent, verbose)

def evaluate_allocation(users, frequencies):
    print("\n\n-- Allocation Evaluation --")
    print("\nUtilities:")
    util_sum = 0
    for user in users:
        util = utilities.calculate_utility(user, frequencies)
        print(f" - {user}: {util}")
        util_sum += util
    print(f" Social Welfare: {round(util_sum, 3)}")
    
    print(f"\nIs in Nash Equilibrium? {utilities.is_nash_equilibrium(users, frequencies)}")

    #TODO: check pareto optimality

    #TODO: plot utility graph

def try_it():

    sim = system.Simulation()

    freq0 = frequencies.RadioFrequency(sim, 0, 100.0)
    freq1 = frequencies.RadioFrequency(sim, 1, 101.1)
    freq2 = frequencies.RadioFrequency(sim, 2, 102.2)
    # freq3 = frequencies.RadioFrequency(sim, 3, 103.3)
    # freq4 = frequencies.RadioFrequency(sim, 4, 104.4)
    # freq5 = frequencies.RadioFrequency(sim, 5, 105.5)
    # freq6 = frequencies.RadioFrequency(sim, 6, 106.6)
    # freq7 = frequencies.RadioFrequency(sim, 7, 107.7)

    freqs = [freq0, freq1, freq2]#, freq3, freq4, freq5, freq6, freq7]

    spectrum = frequencies.RadioFrequencySpectrum(sim, freq0, freq1, freq2)#, freq3, freq4, freq5, freq6, freq7)

    auth0 = users.AuthorizedUser(sim, 2, 2, freq0, False)
    auth1 = users.AuthorizedUser(sim, 3, 3, freq1, True)
    auth2 = users.AuthorizedUser(sim, 5, 2, freq2, False)
    # auth3 = users.AuthorizedUser(sim, 6, 4, freq3)
    # auth4 = users.AuthorizedUser(sim, 1, 5, freq4)

    auths = [auth0, auth1, auth2]#, auth3, auth4]

    cog0 = users.CognitiveUser(sim, 3, 4, True)
    cog1 = users.CognitiveUser(sim, 2, 5, True)
    cog2 = users.CognitiveUser(sim, 4, 9, True)
    cog3 = users.CognitiveUser(sim, 1, 1, True)
    cog4 = users.CognitiveUser(sim, 9, 2, True)

    cogs = [cog0, cog1, cog2, cog3, cog4]

    system.display_sim_state(spectrum, auths, cogs)
    print("")

    allocate_freqs(spectrum, auths, cogs)

    system.display_sim_state(spectrum, auths, cogs)

    evaluate_allocation(cogs, freqs)

if __name__ == '__main__':
    try_it()

