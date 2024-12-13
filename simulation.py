from radiograph import frequencies, system, users, utilities
from algorithms.coloring import allocate_with_coloring
from radiograph.utilities import is_pareto_optimal, plot_utility_graph, refined_pareto_frontier


def allocate_freqs(spectrum, auths, cogs, verbose=True):
    if verbose:
        print("\n\n-- Allocating Frequencies to Users Wanting to Broadcast --\n")
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

def evaluate_allocation(users, frequencies, verbose=True):
    if verbose:
        print("\n\n-- Allocation Evaluation --")
        print("\nUtilities:")
    util_sum = 0
    for user in users:
        util = utilities.calculate_utility(user, frequencies)
        if verbose:
            print(f" - {user}: {util}")
        util_sum += util
    if verbose:
        print(f" Social Welfare: {round(util_sum, 3)}")
    
        print(f"\nIs in Nash Equilibrium? {utilities.is_nash_equilibrium(users, frequencies)}")

        print(f"Is Pareto Optimal? {is_pareto_optimal(users, frequencies)}")

        plot_utility_graph(users, frequencies)
        refined_pareto_frontier(users, frequencies)


    return round(util_sum, 3)
