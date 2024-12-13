import pandas as pd
from radiograph.users import CognitiveUser, AuthorizedUser
from radiograph.frequencies import RadioFrequency, RadioFrequencySpectrum

def load_users_from_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dataset file not found: {file_path}") from e

def process_users(dataframe, sim):
    users = []
    frequencies = []

    for _, row in dataframe.iterrows():
        x_pos = row['x_position']
        y_pos = row['y_position']
        assigned_frequency = row.get('assigned_frequency', None)
        willing_to_rent = row.get('willing_to_rent', False)
        wants_to_broadcast = row.get('wants_to_broadcast', False)

        if row['user_type'] == 'Authorized':
            if pd.notna(assigned_frequency):
                frequency = RadioFrequency(sim, float(assigned_frequency), float(assigned_frequency))
                frequencies.append(frequency)
                user = AuthorizedUser(sim, x_pos, y_pos, frequency, willing_to_rent)
                users.append(user)
            else:
                raise ValueError(f"Authorized user missing an assigned frequency: {row}")
        elif row['user_type'] == 'Cognitive':
            user = CognitiveUser(sim, x_pos, y_pos, wants_to_broadcast)
            users.append(user)
        else:
            print(f"Unknown user type: {row['user_type']} in row: {row}")
    spectrum = RadioFrequencySpectrum(sim, *frequencies)
    return users, spectrum

def get_small_dataset(sim):
    small_dataset = load_users_from_csv("data_files/small_dataset.csv")
    return process_users(small_dataset, sim)

def get_large_dataset(sim):
    large_dataset = load_users_from_csv("data_files/large_dataset.csv")
    return process_users(large_dataset, sim)