import matplotlib.pyplot as plt

from radiograph.frequencies import RadioFrequency
from radiograph.users import AuthorizedUser, _UserBase
from radiograph.system import is_not_out_of_range

DISTANCE_UTILITY_MODIFIER = .25 #Fix for distance from the user renting from was having too much of an impact on utility.

def distance_utility(distance, rangef):
    return 101 ** -(distance / rangef) - 1


def calculate_utility(user: _UserBase, frequencies: list[RadioFrequency], sim):
    if user.wants_to_broadcast_now and user.is_broadcasting:
        # Base utility for broadcasting
        base_utility = 1.0

        # Penalize based on number of users sharing the frequency
        num_users_on_freq = len(user.active_frequency.assigned_to)
        sharing_penalty = 1.0 / max(num_users_on_freq, 1)

        # Calculate distance utility if renting from an authorized user
        renting_user = getattr(user, 'renting_from', None)
        if renting_user:
            distance_util = distance_utility(user.distance_from(renting_user), sim.get_transmit_distance())
        else:
            distance_util = 0

        # Combine utilities
        utility = (base_utility * sharing_penalty) + (distance_util * DISTANCE_UTILITY_MODIFIER)
        return max(utility, 0.0)
    return 0.0

def is_nash_equilibrium(users, frequencies, sim):
    """
    Determines if the current state of the users is a Nash equilibrium.
    """
    for user in users:
        current_utility = calculate_utility(user, frequencies, sim)
        # Test each alternative frequency for improvement in utility
        for frequency in frequencies:
            original_frequency = user.active_frequency
            is_potential_option = user.set_frequency(frequency, False)
            if not is_potential_option:
                # If this is not a possible solution, revert and continue to the next one
                user.set_frequency(original_frequency, False)
                continue
            if calculate_utility(user, frequencies, sim) > current_utility:
                # If utility improves, revert and return False (not Nash equilibrium)
                user.set_frequency(original_frequency, False)
                return False
            user.set_frequency(original_frequency, False)  # Revert to original
    return True


def is_pareto_optimal(users, frequencies, sim):
    """
    Determines if the current state of the users is on the Pareto frontier.
    A state is Pareto optimal if no user can improve their utility without
    reducing another user's utility.
    """
    current_utilities = [calculate_utility(user, frequencies, sim) for user in users]

    for user in users:
        for frequency in frequencies:
            original_frequency = user.active_frequency
            user.set_frequency(frequency, verbose=False)

            # Calculate new utilities
            new_utilities = [calculate_utility(u, frequencies, sim) for u in users]

            # Check if any user improves without harming others
            better_for_someone = any(new > old for new, old in zip(new_utilities, current_utilities))
            no_worse_for_others = all(new >= old for new, old in zip(new_utilities, current_utilities))

            # Revert to the original state
            user.set_frequency(original_frequency, verbose=False)

            if better_for_someone and no_worse_for_others:
                return False  # Not Pareto optimal

    return True


def calculate_social_welfare(users, frequencies):
    """
    Calculates the total social welfare as the sum of utilities.
    """
    return sum(calculate_utility(user, frequencies) for user in users if user.is_broadcasting)


def plot_utility_graph(users, frequencies, sim):
    """
    Plots the utilities of all users for visualization.
    """
    utilities = [calculate_utility(user, frequencies, sim) for user in users]
    labels = [str(user) for user in users]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, utilities)
    plt.xlabel('Users')
    plt.ylabel('Utility')
    plt.title('Utility Distribution Among Users')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_lots(users, frequencies, sim):
    utilities = [calculate_utility(user, frequencies, sim) for user in users]

    # Determine the users in Nash equilibrium
    nash_indices = [i for i, user in enumerate(users) if is_nash_equilibrium([user], frequencies, sim)]

    # Identify Pareto optimal points
    pareto_indices = [
        i for i, utility in enumerate(utilities)
        if all(utility >= other for j, other in enumerate(utilities) if j != i)
    ]
    pareto_utilities = [utilities[i] for i in pareto_indices]

    # Plot utilities for all users
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(utilities)), utilities, label='All Users', color='blue', alpha=0.7)

    # Highlight Pareto-optimal utilities
    plt.scatter(pareto_indices, pareto_utilities, color='red', label='Pareto Optimal')

    # Highlight users in Nash equilibrium with a different marker (e.g., 'x')
    plt.scatter(nash_indices, [utilities[i] for i in nash_indices], color='green', label='Nash Equilibrium', marker='x')

    # Draw Pareto Frontier Line
    pareto_indices, pareto_utilities = zip(*sorted(zip(pareto_indices, pareto_utilities)))
    plt.plot(pareto_indices, pareto_utilities, linestyle='--', color='red', label='Pareto Frontier')

    # Social welfare
    social_welfare = sum(utilities)
    plt.axhline(social_welfare, color='purple', linestyle='-.', label=f'Social Welfare: {social_welfare:.2f}')

    # Customize the plot
    plt.xlabel('User Index')
    plt.ylabel('Utility')
    plt.title('Pareto Frontier of Spectrum Allocation')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()
