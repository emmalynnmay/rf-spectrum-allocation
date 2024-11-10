import pandas as pd
from radiograph.users import CognitiveUser, AuthorizedUser
from radiograph.frequencies import RadioFrequency, RadioFrequencySpectrum

def load_users_from_csv(file_path):
    return pd.read_csv(file_path)

def process_users(dataframe, sim):
    users = []
    for _, row in dataframe.iterrows():
        if row['user_type'] == 'Authorized':
            frequency = RadioFrequency(sim, row['assigned_frequency'], row['assigned_frequency'])
            spectrum = RadioFrequencySpectrum(sim, frequency)
            user = AuthorizedUser(sim, row['x_position'], row['y_position'], spectrum)
        else:
            user = CognitiveUser(sim, row['x_position'], row['y_position'])
        users.append(user)
    return users

def get_small_dataset(sim):
    small_dataset = load_users_from_csv("data_files/small_dataset.csv")
    small_dataset_users = process_users(small_dataset, sim)
    return small_dataset_users

def get_large_dataset(sim):
    large_dataset = load_users_from_csv("data_files/large_dataset.csv")
    large_dataset_users = process_users(large_dataset, sim)
    return large_dataset_users
