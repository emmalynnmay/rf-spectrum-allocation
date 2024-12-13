from radiograph import frequencies, system, users
from simulation import allocate_freqs, evaluate_allocation
from data_generation.read_data import get_small_dataset, get_large_dataset
import random


def setup(use_csv=False, dataset="small"):
    sim = system.Simulation()

    if use_csv:
        if dataset == "small":
            users_list, spectrum = get_small_dataset(sim)
        elif dataset == "large":
            users_list, spectrum = get_large_dataset(sim)
        else:
            raise ValueError("Invalid dataset choice: must be 'small' or 'large'.")

        auths = [user for user in users_list if isinstance(user, users.AuthorizedUser)]
        cogs = [user for user in users_list if isinstance(user, users.CognitiveUser)]

        freqs = spectrum.frequencies

    else:
        if dataset == "large":
            freq0 = frequencies.RadioFrequency(sim, 0, 100.0)
            freq1 = frequencies.RadioFrequency(sim, 1, 101.1)
            freq2 = frequencies.RadioFrequency(sim, 2, 102.2)
            freq3 = frequencies.RadioFrequency(sim, 3, 103.3)
            freq4 = frequencies.RadioFrequency(sim, 4, 104.4)
            freq5 = frequencies.RadioFrequency(sim, 5, 105.5)
            freq6 = frequencies.RadioFrequency(sim, 6, 106.6)
            freq7 = frequencies.RadioFrequency(sim, 7, 107.7)
            freq8 = frequencies.RadioFrequency(sim, 8, 108.8)
            freq9 = frequencies.RadioFrequency(sim, 9, 109.9)
            freq10 = frequencies.RadioFrequency(sim, 10, 110.0)
            freq11 = frequencies.RadioFrequency(sim, 11, 111.1)
            freq12 = frequencies.RadioFrequency(sim, 12, 112.2)
            freq13 = frequencies.RadioFrequency(sim, 13, 113.3)
            freq14 = frequencies.RadioFrequency(sim, 14, 114.4)

            spectrum = frequencies.RadioFrequencySpectrum(
                sim, freq0, freq1, freq2, freq3, freq4, freq5, freq6, freq7, freq8, freq9, freq10, freq11, freq12,
                freq13, freq14
            )
            freqs = [freq0, freq1, freq2, freq3, freq4, freq5, freq6, freq7, freq8, freq9, freq10, freq11, freq12,
                     freq13, freq14]

            auths = [
                users.AuthorizedUser(sim, 2, 2, freq0, False),
                users.AuthorizedUser(sim, 5, 3, freq1, False),
                users.AuthorizedUser(sim, 7, 5, freq2, False),
                users.AuthorizedUser(sim, 3, 6, freq3, True),
                users.AuthorizedUser(sim, 6, 1, freq4, False),
                users.AuthorizedUser(sim, 8, 0, freq5, False),
                users.AuthorizedUser(sim, 10, 3, freq6, False),
                users.AuthorizedUser(sim, 1, 7, freq7, False),
                users.AuthorizedUser(sim, 9, 4, freq8, False),
                users.AuthorizedUser(sim, 0, 8, freq9, True),
                users.AuthorizedUser(sim, 11, 6, freq10, True),
                users.AuthorizedUser(sim, 4, 9, freq11, False),
                users.AuthorizedUser(sim, 13, 2, freq12, False),
                users.AuthorizedUser(sim, 12, 7, freq13, True),
                users.AuthorizedUser(sim, 6, 11, freq14, False),
            ]

            cogs = [
                users.CognitiveUser(sim, 3, 4, True),
                users.CognitiveUser(sim, 2, 5, True),
                users.CognitiveUser(sim, 5, 6, False),
                users.CognitiveUser(sim, 4, 3, True),
                users.CognitiveUser(sim, 9, 7, False),
                users.CognitiveUser(sim, 3, 8, True),
                users.CognitiveUser(sim, 6, 5, True),
                users.CognitiveUser(sim, 7, 9, False),
                users.CognitiveUser(sim, 8, 2, True),
                users.CognitiveUser(sim, 1, 4, True),
                users.CognitiveUser(sim, 11, 3, True),
                users.CognitiveUser(sim, 12, 10, False),
                users.CognitiveUser(sim, 13, 1, True),
                users.CognitiveUser(sim, 0, 11, True),
                users.CognitiveUser(sim, 10, 7, False),
                users.CognitiveUser(sim, 14, 5, True),
                users.CognitiveUser(sim, 9, 11, True),
                users.CognitiveUser(sim, 4, 12, False),
            ]

        else:
            freq0 = frequencies.RadioFrequency(sim, 0, 100.0)
            freq1 = frequencies.RadioFrequency(sim, 1, 101.1)
            freq2 = frequencies.RadioFrequency(sim, 2, 102.2)
            freq3 = frequencies.RadioFrequency(sim, 3, 103.3)
            freq4 = frequencies.RadioFrequency(sim, 4, 104.4)

            spectrum = frequencies.RadioFrequencySpectrum(sim, freq0, freq1, freq2, freq3, freq4)
            freqs = [freq0, freq1, freq2, freq3, freq4]

            auths = [
                users.AuthorizedUser(sim, 2, 2, freq0, True),
                users.AuthorizedUser(sim, 5, 2, freq2, False),
                users.AuthorizedUser(sim, 6, 4, freq3, False),
                users.AuthorizedUser(sim, 1, 5, freq4, True),
            ]

            cogs = [
                users.CognitiveUser(sim, 3, 4, True),
                users.CognitiveUser(sim, 2, 5, True),
                users.CognitiveUser(sim, 4, 9, True),
                users.CognitiveUser(sim, 1, 1, True),
                users.CognitiveUser(sim, 9, 2, True),
                users.CognitiveUser(sim, 3, 5, True),
            ]

    return spectrum, freqs, auths, cogs


def run_simulation(verbose, shuffle_order=False, use_csv=False, dataset="small"):
    """
    Run the simulation with options to use dynamic datasets or hardcoded data.
    """
    (spectrum, freqs, auths, cogs) = setup(use_csv, dataset)

    if shuffle_order:
        random.shuffle(cogs)

    if verbose:
        system.display_sim_state(spectrum, auths, cogs)
        print("")

    allocate_freqs(spectrum, auths, cogs, verbose)

    if verbose:
        system.display_sim_state(spectrum, auths, cogs)

    social_welfare = evaluate_allocation(cogs, freqs, verbose)
    return social_welfare


if __name__ == '__main__':
    use_csv_input = input("Use CSV for setup? (yes/no): ").strip().lower() == "yes"
    dataset_choice = "small"

    if not use_csv_input:
        dataset_choice = input("Choose dataset for hardcoded setup (small/large): ").strip().lower()

    run_simulation(True, use_csv=use_csv_input, dataset=dataset_choice)

    iterations = 10
    social_welfare_results = []
    for i in range(iterations):
        social_welfare_results.append(run_simulation(False, True, use_csv=use_csv_input, dataset=dataset_choice))

    print(f"\nSocial welfare in {iterations} different arrangements of same situation:", social_welfare_results)
