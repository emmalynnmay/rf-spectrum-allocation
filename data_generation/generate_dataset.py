import csv
import random


def generate_dataset(file_name, num_users, num_authorized, max_position, max_frequency):
    """
    Generates a dataset and saves it as a CSV file.
    - file_name: Name of the output CSV file.
    - num_users: Total number of users.
    - num_authorized: Number of authorized users (remaining will be cognitive).
    - max_position: Maximum coordinate values for user positions.
    - max_frequency: Maximum frequency ID to assign to authorized users.
    """
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "user_type", "x_position", "y_position", "assigned_frequency"])

        for user_id in range(1, num_users + 1):
            x_position = random.randint(0, max_position)
            y_position = random.randint(0, max_position)
            if user_id <= num_authorized:
                frequency = random.randint(1, max_frequency)
                writer.writerow([user_id, "Authorized", x_position, y_position, frequency])
            else:
                writer.writerow([user_id, "Cognitive", x_position, y_position, ""])

generate_dataset("../data_files/small_dataset.csv", num_users=10, num_authorized=3, max_position=50, max_frequency=5)
generate_dataset("../data_files/large_dataset.csv", num_users=100, num_authorized=20, max_position=1000, max_frequency=50)
