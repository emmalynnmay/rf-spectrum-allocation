import pandas as pd
from radiograph.agents.coguser import CognitiveUser, AuthorizedUser
from radiograph.agents.frequencies import RadioFrequency, RadioFrequencySpectrum

def load_users_from_csv(file_path):
    return pd.read_csv(file_path)

def process_users(dataframe):
    users = []
    for _, row in dataframe.iterrows():
        if row['user_type'] == 'Authorized':
            frequency = RadioFrequency(row['assigned_frequency'], row['assigned_frequency'])
            spectrum = RadioFrequencySpectrum(frequency)
            user = AuthorizedUser(row['user_id'], row['x_position'], row['y_position'], spectrum)
        else:
            user = CognitiveUser(row['user_id'], row['x_position'], row['y_position'])
        users.append(user)
    return users

small_dataset = load_users_from_csv("../data_files/small_dataset.csv")
small_dataset_users = process_users(small_dataset)

large_dataset = load_users_from_csv("../data_files/large_dataset.csv")
large_dataset_users = process_users(large_dataset)
