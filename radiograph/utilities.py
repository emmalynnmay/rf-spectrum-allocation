import matplotlib.pyplot as plt

from radiograph.frequencies import RadioFrequency
from radiograph.users import AuthorizedUser, _UserBase
from radiograph.system import TRANSMIT_DISTANCE, is_not_out_of_range


def distance_utility(distance, rangef=TRANSMIT_DISTANCE):
    return 101 ** -(distance / rangef) - 1



def calculate_utility(user: _UserBase, frequencies: list[RadioFrequency], trans_range=TRANSMIT_DISTANCE):
    if user.is_broadcasting and getattr(user, 'active_frequency'):
        # Base utility for broadcasting
        base_utility = 1.0

        # Penalize based on number of users sharing the frequency
        num_users_on_freq = len(user.active_frequency.assigned_to)
        sharing_penalty = 1.0 / max(num_users_on_freq, 1)

        # Calculate distance utility if renting from an authorized user
        renting_user = getattr(user, 'renting_from', None)
        if renting_user:
            distance_util = distance_utility(user.distance_from(renting_user), trans_range)
        else:
            distance_util = 0

        # Combine utilities
        utility = base_utility * sharing_penalty + distance_util
        return max(utility, 0.0)
    return 0.0

def is_nash_equilibrium(users, frequencies):
    """
    Determines if the current state of the users is a Nash equilibrium.
    """
    for user in users:
        current_utility = calculate_utility(user, frequencies)
        # Test each alternative frequency for improvement in utility
        for frequency in frequencies:
            original_frequency = user.active_frequency
            is_potential_option = user.set_frequency(frequency, False)
            if not is_potential_option:
                # If this is not a possible solution, revert and continue to the next one
                user.set_frequency(original_frequency, False)
                continue
            if calculate_utility(user, frequencies) > current_utility:
                # If utility improves, revert and return False (not Nash equilibrium)
                user.set_frequency(original_frequency, False)
                return False
            user.set_frequency(original_frequency, False)  # Revert to original
    return True


def is_pareto_optimal(users, frequencies):
    """
    Determines if the current state of the users is on the Pareto frontier.
    A state is Pareto optimal if no user can improve their utility without
    reducing another user's utility.
    """
    current_utilities = [calculate_utility(user, frequencies) for user in users]

    for user in users:
        for frequency in frequencies:
            original_frequency = user.active_frequency
            user.set_frequency(frequency, verbose=False)

            # Calculate new utilities
            new_utilities = [calculate_utility(u, frequencies) for u in users]

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


def plot_utility_graph(users, frequencies):
    """
    Plots the utilities of all users for visualization.
    """
    utilities = [calculate_utility(user, frequencies) for user in users]
    labels = [str(user) for user in users]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, utilities)
    plt.xlabel('Users')
    plt.ylabel('Utility')
    plt.title('Utility Distribution Among Users')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def refined_pareto_frontier(users, frequencies):
    """
    Refined Pareto Frontier visualization with corrected line plotting.
    """
    # Calculate utilities for all users
    utilities = [calculate_utility(user, frequencies) for user in users]
    user_labels = [str(user) for user in users]
    user_types = ['Authorized' if isinstance(user, AuthorizedUser) else 'Cognitive' for user in users]

    # Identify Pareto-optimal points
    pareto_indices = []
    for i, utility in enumerate(utilities):
        if all(utility >= other for j, other in enumerate(utilities) if j != i):
            pareto_indices.append(i)

    # Extract utilities and indices for Pareto points
    pareto_utilities = [utilities[i] for i in pareto_indices]
    pareto_x = pareto_indices  # Keep the original x-coordinates (user indices)

    # Sort Pareto points for proper plotting
    sorted_pareto = sorted(zip(pareto_x, pareto_utilities), key=lambda x: x[0])
    pareto_x, pareto_y = zip(*sorted_pareto)

    # Plot utilities for all users
    plt.figure(figsize=(10, 7))
    plt.scatter(range(len(utilities)), utilities, label='Utilities (All Users)', alpha=0.7, color='blue')

    # Highlight Pareto-optimal utilities
    plt.scatter(pareto_x, pareto_y, color='red', label='Pareto Optimal', zorder=5)

    # Draw Pareto Frontier Line
    plt.plot(pareto_x, pareto_y, linestyle='--', color='red', label='Pareto Frontier')

    # Annotate each point with user labels
    for i, utility in enumerate(utilities):
        plt.text(
            i, utility + 0.02, user_labels[i], fontsize=8, ha='center'
        )

    # Add indicators for user types (authorized vs. cognitive)
    authorized_indices = [i for i, u in enumerate(user_types) if u == 'Authorized']
    cognitive_indices = [i for i, u in enumerate(user_types) if u == 'Cognitive']
    plt.scatter(
        authorized_indices,
        [utilities[i] for i in authorized_indices],
        label='Authorized Users',
        color='green',
        marker='s',
        alpha=0.7
    )
    plt.scatter(
        cognitive_indices,
        [utilities[i] for i in cognitive_indices],
        label='Cognitive Users',
        color='blue',
        marker='o',
        alpha=0.7
    )

    # Add total social welfare as a horizontal line
    social_welfare = sum(utilities)
    plt.axhline(social_welfare, color='purple', linestyle='-.', label=f'Social Welfare: {social_welfare:.2f}')

    # Enhance plot appearance
    plt.xlabel('User Index (Sorted by Utility)')
    plt.ylabel('Utility')
    plt.title('Refined Pareto Frontier of Spectrum Allocation')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

