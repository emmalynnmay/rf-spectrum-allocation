import matplotlib.pyplot as plt

def calculate_utility(user, frequencies):
    """
    Calculates the utility of a user based on active frequency and broadcasting status.
    Utility might depend on factors like frequency allocation, interference, and broadcasting status.
    """
    if user.is_broadcasting and user.active_frequency:
        # Sample utility calculation: based on frequency and distance to avoid interference
        # Adjust based on actual simulation parameters
        return round(1.0 / len(user.active_frequency.assigned_to), 3)  # Example: inverse of number of users sharing frequency
    else:
        return 0.0  # No utility if not broadcasting


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


def is_pareto_optimal(users, frequencies, all_possible_states):
    """
    Determines if the current state is on the Pareto frontier.
    """
    current_utilities = [calculate_utility(user, frequencies) for user in users]
    for other_state in all_possible_states:
        other_utilities = [calculate_utility(user, other_state) for user in users]
        # Check if other state dominates the current state
        better_for_someone = any(o > c for o, c in zip(other_utilities, current_utilities))
        no_worse_for_others = all(o >= c for o, c in zip(other_utilities, current_utilities))
        if better_for_someone and no_worse_for_others:
            return False
    return True


def calculate_social_welfare(users, frequencies):
    """
    Calculates the total social welfare as the sum of utilities.
    """
    return sum(calculate_utility(user, frequencies) for user in users)


def plot_utility_graph(users, frequencies, nash_states, pareto_states, max_social_welfare_state):
    """
    Plots a utility graph highlighting Nash equilibrium, Pareto frontier, and max social welfare.
    """
    utilities = [(calculate_utility(users[0], frequencies), calculate_utility(users[1], frequencies)) for state in
                 nash_states + pareto_states + [max_social_welfare_state]]
    x, y = zip(*utilities)

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='grey', label='All States', alpha=0.5)

    # Highlight Nash equilibria
    nash_utilities = [(calculate_utility(users[0], frequencies), calculate_utility(users[1], frequencies)) for state in
                      nash_states]
    if nash_utilities:
        nx, ny = zip(*nash_utilities)
        plt.scatter(nx, ny, color='blue', label='Nash Equilibrium')

    # Highlight Pareto frontier
    pareto_utilities = [(calculate_utility(users[0], frequencies), calculate_utility(users[1], frequencies)) for state
                        in pareto_states]
    if pareto_utilities:
        px, py = zip(*pareto_utilities)
        plt.scatter(px, py, color='green', label='Pareto Frontier')

    # Highlight max social welfare
    sw_x, sw_y = calculate_utility(users[0], max_social_welfare_state), calculate_utility(users[1],
                                                                                          max_social_welfare_state)
    plt.scatter([sw_x], [sw_y], color='red', label='Max Social Welfare')

    plt.xlabel('Utility of User 1')
    plt.ylabel('Utility of User 2')
    plt.legend()
    plt.title('Utility Plan of Interference Channel Game')
    plt.grid(True)
    plt.show()