from math import sqrt

TRANSMIT_DISTANCE = 25#3 #the max distance from a user that radio transmissions can still be picked up
#COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW]

class Simulation:
    def __init__(self):
        self.user_ids = []
        self.user_positions = []

    def check_pos(self, x, y):
        if (x, y) in self.user_positions:
            raise Exception(f"More than one user cannot be placed in the same position. ({x}, {y}) is already occupied.")
        else:
            self.user_positions.append((x, y))

    def next_user_id(self):
        new_id = len(self.user_ids)
        self.user_ids.append(new_id)
        return new_id


def get_transmit_distance():
    return TRANSMIT_DISTANCE


def user_distance(user1, user2):
    x_dist = user1.pos_x - user2.pos_x
    y_dist = user1.pox_y - user2.pox_y
    return sqrt((x_dist ** 2) + (y_dist ** 2))


def is_not_out_of_range(user1, user2, rangef=TRANSMIT_DISTANCE):
    return user_distance(user1, user2) <= rangef


def display_sim_state(spectrum, auth_users, cog_users):
    print(print("\n\n-- System State --"))
    #TODO: add colors

    all_users = auth_users + cog_users

    print("\nUsers:")
    for user in all_users:
        print(f" - {user}", end="")
        if user.wants_to_broadcast_now:
            if user.is_broadcasting:
                emoji = "✅"
            else:
                emoji = "❌"
            print(f" wants to broadcast {emoji}")
        else:
            print("")

    #Display real space with the ranges of each user
    print("\nReal Space (not entirely mathematically accurate):")

    # Determine grid size for real space
    max_x = max(user.pos_x for user in all_users) + TRANSMIT_DISTANCE
    max_y = max(user.pox_y for user in all_users) + TRANSMIT_DISTANCE
    grid_size = max(max_x, max_y) + 1

    real_space = [["  " for _ in range(grid_size)] for _ in range(grid_size)]

    real_space[0][0] = "+"

    def check_in_range(val):
        return val < grid_size and val >= 0
    
    def plot_range(x, y):
        real_space[y][x] = ". "
        #real_space_colors[x][y] = color

    for user in all_users:

        for dist in range(1, TRANSMIT_DISTANCE + 1):
            new_x_pos = user.pos_x + dist
            new_y_pos = user.pox_y + dist
            new_x_neg = user.pos_x - dist
            new_y_neg = user.pox_y - dist
            if check_in_range(new_x_pos):
                plot_range(new_x_pos, user.pox_y)
            if check_in_range(new_x_neg):
                plot_range(new_x_neg, user.pox_y)
            if check_in_range(new_y_pos):
                plot_range(user.pos_x, new_y_pos)
            if check_in_range(new_y_neg):
                plot_range(user.pos_x, new_y_neg)

            if check_in_range(new_y_neg) and check_in_range(new_x_neg):
                plot_range(new_x_neg, new_y_neg)
            if check_in_range(new_y_neg) and check_in_range(new_x_pos):
                plot_range(new_x_pos, new_y_neg)
            if check_in_range(new_y_pos) and check_in_range(new_x_neg):
                plot_range(new_x_neg, new_y_pos)
            if check_in_range(new_y_pos) and check_in_range(new_x_pos):
                plot_range(new_x_pos, new_y_pos)

    for user in all_users:
        real_space[user.pox_y][user.pos_x] = user.id
        #real_space_colors[user.pos_x][user.pox_y] = COLORS[color]
    
    print_cartesian(real_space)

    #Display the rf spectrum, who owns which frequency, and who is currently broadcasting on it
    print("\nRadio Spectrum:")
    for freq in spectrum.frequencies:
        print(freq.frequency)
        if len(freq.assigned_to) > 0:
            for user in freq.assigned_to:
                print(f"   - User {user.id} is actively broadcasting")
        else:
            print(f"   - No active broadcast")
        for user in auth_users:
            if freq == user.assigned_frequency:
                print(f"   - Frequency owned by authorized user {user.id}")

def print_cartesian(input_data):

    for row in input_data:
        print("--", end ="-")
    print("")

    for row in reversed(input_data):
        for cell in row:
            print("", end ="")
            print(cell, end =" ")
        print("|")
    
    print("", end ="")
    for row in input_data:
        print("--", end ="-")
    print("")