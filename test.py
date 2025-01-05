import unittest
from radiograph.users import *
from radiograph.frequencies import *
from radiograph.system import *
from radiograph.simulation import allocate_freqs
from data_generation import read_data

class TestFrequency(unittest.TestCase):
    def test_create_frequency_no_user(self):
        sim = Simulation(5)
        freq = RadioFrequency(sim, 1, 107.9)
        self.assertEqual(freq.frequency, 107.9)
        self.assertEqual(freq.assigned_to, [])
        self.assertEqual(freq.is_active, False)

    def test_create_frequency_user(self):
        sim = Simulation(5)
        cog = CognitiveUser(sim, 3, 4)
        freq = RadioFrequency(sim, 1, 107.9, cog)
        self.assertEqual(freq.frequency, 107.9)
        self.assertEqual(freq.assigned_to, [cog])
        self.assertEqual(freq.is_active, False)

class TestSpectrum(unittest.TestCase):
    def test_create_spectrum(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        freq2 = RadioFrequency(sim, 2, 103.5)
        freq3 = RadioFrequency(sim, 3, 99.9)
        spectrum = RadioFrequencySpectrum(sim, freq1, freq2, freq3)

        self.assertEqual(spectrum.get_frequency(1), freq1)
        self.assertEqual(spectrum.get_frequency(2), freq2)
        self.assertEqual(spectrum.get_frequency(3), freq3)
        self.assertEqual(spectrum.get_frequency(4), None)

class TestCognitiveUser(unittest.TestCase):
    def test_create_cognitive(self):
        sim = Simulation(5)
        cog = CognitiveUser(sim, 3, 4)
        self.assertEqual(cog.position, (3, 4))
        self.assertEqual(cog.is_broadcasting, False)

        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.active_frequency, None)

    def test_assign_frequency(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        cog = CognitiveUser(sim, 3, 4)
        cog.set_frequency(freq1)
        self.assertEqual(freq1.assigned_to, [cog])
        self.assertEqual(cog.active_frequency, freq1)
        self.assertEqual(cog.isActive, True)

    def test_broadcast(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        cog = CognitiveUser(sim, 3, 4)

        with self.assertRaises(Exception):
            cog.begin_broadcasting()
        self.assertEqual(cog.is_broadcasting, False)
        
        cog.set_frequency(freq1)
        self.assertEqual(cog.is_broadcasting, False)
        cog.begin_broadcasting()
        self.assertEqual(cog.is_broadcasting, True)
        self.assertEqual(cog.active_frequency.is_active, True)
        cog.stop_broadcasting()
        self.assertEqual(cog.is_broadcasting, False)
        self.assertEqual(cog.active_frequency.is_active, False)

    def test_invalid_pos(self):
        sim = Simulation(5)
        with self.assertRaises(Exception):
            cog = CognitiveUser(sim, -3, -4)

class TestAuthorizedUser(unittest.TestCase):
    def test_create_auth(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        self.assertEqual(auth.position, (3, 4))
        self.assertEqual(auth.is_broadcasting, False)

        self.assertEqual(auth.has_rented_frequency, None)
        self.assertEqual(auth.assigned_frequency, freq1)

    def test_broadcast(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)

        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, True)
        self.assertEqual(auth.assigned_frequency.is_active, True)

        auth.stop_broadcasting()
        self.assertEqual(auth.is_broadcasting, False)
        self.assertEqual(auth.assigned_frequency.is_active, False)

    def test_invalid_pos(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        with self.assertRaises(Exception):
            auth = AuthorizedUser(sim, -3, -4, freq1)

    def test_rent_freq(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        cog = CognitiveUser(sim, 3, 5)

        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.active_frequency, None)
        self.assertEqual(auth.has_rented_frequency, None)

        auth.grant_frequency(freq1, cog)
        self.assertEqual(cog.isActive, True)
        self.assertEqual(cog.active_frequency, freq1)
        self.assertEqual(auth.has_rented_frequency, cog)

        auth.revoke_frequency(cog)
        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.active_frequency, None)
        self.assertEqual(auth.has_rented_frequency, None)

    def test_cant_rent_while_using(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        cog = CognitiveUser(sim, 3, 5)

        auth.begin_broadcasting()

        with self.assertRaises(Exception):
            auth.grant_frequency(freq1, cog)
        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.active_frequency, None)
        self.assertEqual(auth.has_rented_frequency, None)

    def test_broadcast_with_rented(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        cog = CognitiveUser(sim, 3, 5)

        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, True)
        self.assertEqual(auth.assigned_frequency.is_active, True)
        auth.stop_broadcasting()

        auth.grant_frequency(freq1, cog)

        # Take back so we can broadcast
        print(auth)
        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, True)
        self.assertEqual(auth.assigned_frequency.is_active, True)
        auth.stop_broadcasting()

        auth.grant_frequency(freq1, cog)

        # We can't take it back because cog is broadcasting
        cog.begin_broadcasting()
        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, False)
        self.assertEqual(cog.is_broadcasting, True)
        self.assertEqual(auth.assigned_frequency.is_active, True)

class TestVisualization(unittest.TestCase):
    def test_standard(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        freq2 = RadioFrequency(sim, 2, 103.5)
        freq3 = RadioFrequency(sim, 3, 99.9)
        spectrum = RadioFrequencySpectrum(sim, freq1, freq2, freq3)
        cog = CognitiveUser(sim, 3, 4)
        other_cog = CognitiveUser(sim, 5, 12)
        auth = AuthorizedUser(sim, 2, 2, freq3)
        auth.grant_frequency(freq3, cog)
        cog.begin_broadcasting()

        display_sim_state(spectrum, [auth], [cog, other_cog], sim)

    def test_coords(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        spectrum = RadioFrequencySpectrum(sim, freq1)

        u00 = CognitiveUser(sim, 0, 0)

        # diagonal group
        # u11 = CognitiveUser(sim, 1, 1)
        # u22 = CognitiveUser(sim, 2, 2)
        # u33 = CognitiveUser(sim, 3, 3)
        # u44 = CognitiveUser(sim, 4, 4)

        # x = 0 group
        u01 = CognitiveUser(sim, 0, 1)
        u02 = CognitiveUser(sim, 0, 2)
        u03 = CognitiveUser(sim, 0, 3)
        u04 = CognitiveUser(sim, 0, 4)

        # y = 0 group
        u10 = CognitiveUser(sim, 1, 0)
        u20 = CognitiveUser(sim, 2, 0)
        u30 = CognitiveUser(sim, 3, 0)
        u40 = CognitiveUser(sim, 4, 0)

        display_sim_state(spectrum, [], [u00,
            # u11, u22, u33, u44, 
            u01, u02, u03, u04, 
            u10, u20, u30, u40
            ], sim)

    def test_range(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        spectrum = RadioFrequencySpectrum(sim, freq1)

        u00 = CognitiveUser(sim, 0, 0)

        display_sim_state(spectrum, [], [u00], sim)
    
class TestDataRead(unittest.TestCase):
    def test_small_data(self):
        sim = Simulation(5)
        data = read_data.get_small_dataset(sim)

class TestMisc(unittest.TestCase):
    def test_users_on_same_freq(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        cog1 = CognitiveUser(sim, 0, 0)
        cog1.set_frequency(freq1)

        self.assertIn(cog1, freq1.assigned_to)
        self.assertEqual(cog1.active_frequency, freq1)
        self.assertEqual(cog1.isActive, True)

        cog2 = CognitiveUser(sim, 0, 2 + sim.get_transmit_distance())
        cog2.set_frequency(freq1)
        self.assertEqual(cog2.active_frequency, freq1)
        self.assertEqual(cog2.isActive, True)
        self.assertIn(cog2, freq1.assigned_to)
    
    def test_users_too_close_on_same_freq(self):
        sim = Simulation(5)
        freq1 = RadioFrequency(sim, 1, 107.9)
        cog1 = CognitiveUser(sim, 0, 0)
        cog1.set_frequency(freq1)

        self.assertIn(cog1, freq1.assigned_to)
        self.assertEqual(cog1.active_frequency, freq1)
        self.assertEqual(cog1.isActive, True)

        cog2 = CognitiveUser(sim, 0, 1)
        cog2.set_frequency(freq1)
        self.assertNotIn(cog2, freq1.assigned_to)
        self.assertEqual(cog2.active_frequency, None)
        self.assertEqual(cog2.isActive, False)

    def test_users_wont_have_same_id(self):
        sim = Simulation(5)
        u1 = CognitiveUser(sim, 3, 8)
        u2 = CognitiveUser(sim, 3, 4)
        self.assertNotEqual(u1.id, u2.id)

    def test_users_cant_be_in_same_pos(self):
        sim = Simulation(5)
        u1 = CognitiveUser(sim, 3, 4)
        with self.assertRaises(Exception):
            u2 = CognitiveUser(sim, 3, 4)

class TestFrequencyAllocation(unittest.TestCase):
    def test_cogs_want_broadcast_happy(self):
        sim = Simulation(5)
        freq0 = RadioFrequency(sim, 0, 100.0)
        freq1 = RadioFrequency(sim, 1, 101.1)
        freq2 = RadioFrequency(sim, 2, 102.2)
        spectrum = RadioFrequencySpectrum(sim, freq0, freq1, freq2)
        auth0 = AuthorizedUser(sim, 2, 2, freq0, False)
        auth1 = AuthorizedUser(sim, 3, 3, freq1, False)
        auth2 = AuthorizedUser(sim, 5, 2, freq2, False)
        auths = [auth0, auth1, auth2]
        cog0 = CognitiveUser(sim, 3, 4, True)
        cog1 = CognitiveUser(sim, 2, 5, True)
        cog2 = CognitiveUser(sim, 4, 9, True)
        cog4 = CognitiveUser(sim, 9, 2, True)
        cogs = [cog0, cog1, cog2, cog4]

        allocate_freqs(spectrum, auths, cogs, sim, False)

        for cog in cogs:
            self.assertEqual(cog.is_broadcasting, True) 
    
    def test_cogs_and_auths_want_broadcast_happy(self):
        sim = Simulation(5)
        freq0 = RadioFrequency(sim, 0, 100.0)
        freq1 = RadioFrequency(sim, 1, 101.1)
        freq2 = RadioFrequency(sim, 2, 102.2)
        spectrum = RadioFrequencySpectrum(sim, freq0, freq1, freq2)
        auth0 = AuthorizedUser(sim, 2, 2, freq0, False)
        auth1 = AuthorizedUser(sim, 3, 3, freq1, True)
        auth2 = AuthorizedUser(sim, 5, 2, freq2, False)
        auths = [auth0, auth1, auth2]
        cog0 = CognitiveUser(sim, 3, 4, True)
        cog1 = CognitiveUser(sim, 2, 5, True)
        cog2 = CognitiveUser(sim, 4, 9, True)
        cog4 = CognitiveUser(sim, 9, 2, True)
        cogs = [cog0, cog1, cog2, cog4]

        allocate_freqs(spectrum, auths, cogs, sim, False)

        for cog in cogs:
            self.assertEqual(cog.is_broadcasting, True) 
        self.assertEqual(auth1.is_broadcasting, True)     
        
    def test_cogs_want_broadcast_sad(self):
        sim = Simulation(5)
        freq0 = RadioFrequency(sim, 0, 100.0)
        freq1 = RadioFrequency(sim, 1, 101.1)
        freq2 = RadioFrequency(sim, 2, 102.2)
        spectrum = RadioFrequencySpectrum(sim, freq0, freq1, freq2)
        auth0 = AuthorizedUser(sim, 2, 2, freq0, False)
        auths = [auth0]
        cog0 = CognitiveUser(sim, 3, 4, True)
        cog1 = CognitiveUser(sim, 2, 5, True)
        cog2 = CognitiveUser(sim, 4, 9, True)
        cog4 = CognitiveUser(sim, 9, 2, True)
        cogs = [cog0, cog1, cog2, cog4]

        allocate_freqs(spectrum, auths, cogs, sim, False)

        self.assertEqual(cog0.is_broadcasting, True)  
        self.assertEqual(cog1.is_broadcasting, False)
        self.assertEqual(cog2.is_broadcasting, True)
        self.assertEqual(cog4.is_broadcasting, True)
    
    def test_cogs_and_auths_want_broadcast_sad(self):
        sim = Simulation(5)
        freq0 = RadioFrequency(sim, 0, 100.0)
        freq1 = RadioFrequency(sim, 1, 101.1)
        freq2 = RadioFrequency(sim, 2, 102.2)
        spectrum = RadioFrequencySpectrum(sim, freq0, freq1, freq2)
        auth0 = AuthorizedUser(sim, 2, 2, freq0, False)
        auth1 = AuthorizedUser(sim, 3, 3, freq1, True)
        auths = [auth0, auth1]
        cog0 = CognitiveUser(sim, 3, 4, True)
        cog1 = CognitiveUser(sim, 2, 5, True)
        cog2 = CognitiveUser(sim, 4, 9, True)
        cog4 = CognitiveUser(sim, 9, 2, True)
        cogs = [cog0, cog1, cog2, cog4]

        allocate_freqs(spectrum, auths, cogs, sim, False)

        self.assertEqual(cog0.is_broadcasting, True)  
        self.assertEqual(cog1.is_broadcasting, False)
        self.assertEqual(cog2.is_broadcasting, True)
        self.assertEqual(cog4.is_broadcasting, True)

if __name__ == '__main__':
    unittest.main()
