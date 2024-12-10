from radiograph import frequencies, system, users
from simulation import allocate_freqs, evaluate_allocation
import random

def setup(): 
    sim = system.Simulation()

    freq0 = frequencies.RadioFrequency(sim, 0, 100.0)
    freq1 = frequencies.RadioFrequency(sim, 1, 101.1)
    freq2 = frequencies.RadioFrequency(sim, 2, 102.2)
    freq3 = frequencies.RadioFrequency(sim, 3, 103.3)
    freq4 = frequencies.RadioFrequency(sim, 4, 104.4)

    freqs = [freq0, freq1, freq2, freq3, freq4]

    spectrum = frequencies.RadioFrequencySpectrum(sim, freq0, freq1, freq2, freq3, freq4)

    auth0 = users.AuthorizedUser(sim, 2, 2, freq0, True)
    auth1 = users.AuthorizedUser(sim, 5, 2, freq2, False)
    auth2 = users.AuthorizedUser(sim, 6, 4, freq3, False)
    auth3 = users.AuthorizedUser(sim, 1, 5, freq4, True)

    auths = [auth0, auth1, auth2, auth3]

    cog0 = users.CognitiveUser(sim, 3, 4, True)
    cog1 = users.CognitiveUser(sim, 2, 5, True)
    cog2 = users.CognitiveUser(sim, 4, 9, True)
    cog3 = users.CognitiveUser(sim, 1, 1, True)
    cog4 = users.CognitiveUser(sim, 9, 2, True)
    cog5 = users.CognitiveUser(sim, 3, 5, True)

    cogs = [cog0, cog1, cog2, cog3, cog4, cog5]

    return (spectrum, freqs, auths, cogs)

def run_simulation(verbose, shuffle_order=False):
    (spectrum, freqs, auths, cogs) = setup()
    
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
    run_simulation(True)

    iterations = 10
    social_welfare_results = []
    for i in range(iterations):
        social_welfare_results.append(run_simulation(False, True))

    print(f"\nSocial welfare in {iterations} different arrangements of same situation:", social_welfare_results)
