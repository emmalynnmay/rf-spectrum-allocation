TRANSMIT_DISTANCE = 3 #the max distance from a user that radio transmissions can still be picked up
#COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW]

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
            if freq == user.assignedFrequency:
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