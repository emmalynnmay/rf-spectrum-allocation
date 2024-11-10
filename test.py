import unittest
from radiograph.agents.coguser import *
from radiograph.agents.frequencies import *
from radiograph.system import *

class TestFrequency(unittest.TestCase):
    def test_create_frequency_no_user(self):
        sim = Simulation()
        freq = RadioFrequency(sim, 1, 107.9)
        self.assertEqual(freq.frequency, 107.9)
        self.assertEqual(freq.assignedTo, None)
        self.assertEqual(freq.is_active, False)

    def test_create_frequency_user(self):
        sim = Simulation()
        cog = CognitiveUser(sim, 3, 4)
        freq = RadioFrequency(sim, 1, 107.9, cog)
        self.assertEqual(freq.frequency, 107.9)
        self.assertEqual(freq.assignedTo, cog)
        self.assertEqual(freq.is_active, False)

class TestSpectrum(unittest.TestCase):
    def test_create_spectrum(self):
        sim = Simulation()
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
        sim = Simulation()
        cog = CognitiveUser(sim, 3, 4)
        self.assertEqual(cog.position, (3, 4))
        self.assertEqual(cog.is_broadcasting, False)

        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.activeFrequency, None)

    def test_assign_frequency(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        cog = CognitiveUser(sim, 3, 4)
        cog.set_frequency(freq1)
        self.assertEqual(freq1.assignedTo, cog)
        self.assertEqual(cog.activeFrequency, freq1)
        self.assertEqual(cog.isActive, True)

    def test_drop_frequency(self):
        self.assertFalse(True)

    def test_broadcast(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        cog = CognitiveUser(sim, 3, 4)

        with self.assertRaises(Exception):
            cog.begin_broadcasting()
        self.assertEqual(cog.is_broadcasting, False)
        
        cog.set_frequency(freq1)
        self.assertEqual(cog.is_broadcasting, False)
        cog.begin_broadcasting()
        self.assertEqual(cog.is_broadcasting, True)
        self.assertEqual(cog.activeFrequency.is_active, True)
        cog.stop_broadcasting()
        self.assertEqual(cog.is_broadcasting, False)
        self.assertEqual(cog.activeFrequency.is_active, False)

    def test_invalid_pos(self):
        sim = Simulation()
        with self.assertRaises(Exception):
            cog = CognitiveUser(sim, -3, -4)

class TestAuthorizedUser(unittest.TestCase):
    def test_create_auth(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        self.assertEqual(auth.position, (3, 4))
        self.assertEqual(auth.is_broadcasting, False)

        self.assertEqual(auth.has_rented_frequency, False)
        self.assertEqual(auth.assignedFrequency, freq1)

    def test_broadcast(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)

        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, True)
        self.assertEqual(auth.assignedFrequency.is_active, True)

        auth.stop_broadcasting()
        self.assertEqual(auth.is_broadcasting, False)
        self.assertEqual(auth.assignedFrequency.is_active, False)

    def test_invalid_pos(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        with self.assertRaises(Exception):
            auth = AuthorizedUser(sim, -3, -4, freq1)

    def test_rent_freq(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        cog = CognitiveUser(sim, 3, 4)

        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.activeFrequency, None)
        self.assertEqual(auth.has_rented_frequency, False)

        auth.grant_frequency(freq1, cog)
        self.assertEqual(cog.isActive, True)
        self.assertEqual(cog.activeFrequency, freq1)
        self.assertEqual(auth.has_rented_frequency, True)

        auth.revoke_frequency(cog)
        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.activeFrequency, None)
        self.assertEqual(auth.has_rented_frequency, False)

    def test_cant_rent_while_using(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        cog = CognitiveUser(sim, 3, 4)

        auth.begin_broadcasting()

        with self.assertRaises(Exception):
            auth.grant_frequency(freq1, cog)
        self.assertEqual(cog.isActive, False)
        self.assertEqual(cog.activeFrequency, None)
        self.assertEqual(auth.has_rented_frequency, False)

    def test_broadcast_with_rented(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        auth = AuthorizedUser(sim, 3, 4, freq1)
        cog = CognitiveUser(sim, 3, 4)

        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, True)
        self.assertEqual(auth.assignedFrequency.is_active, True)
        auth.stop_broadcasting()

        auth.grant_frequency(freq1, cog)

        # Take back so we can broadcast
        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, True)
        self.assertEqual(auth.assignedFrequency.is_active, True)
        auth.stop_broadcasting()

        auth.grant_frequency(freq1, cog)

        # We can't take it back because cog is broadcasting
        cog.begin_broadcasting()
        auth.begin_broadcasting()
        self.assertEqual(auth.is_broadcasting, False)
        self.assertEqual(cog.is_broadcasting, True)
        self.assertEqual(auth.assignedFrequency.is_active, True)

class TestVisualization(unittest.TestCase):
    def test_standard(self):
        sim = Simulation()
        freq1 = RadioFrequency(sim, 1, 107.9)
        freq2 = RadioFrequency(sim, 2, 103.5)
        freq3 = RadioFrequency(sim, 3, 99.9)
        spectrum = RadioFrequencySpectrum(sim, freq1, freq2, freq3)
        cog = CognitiveUser(sim, 3, 4)
        other_cog = CognitiveUser(sim, 5, 12)
        auth = AuthorizedUser(sim, 2, 2, freq3)
        auth.grant_frequency(freq3, cog)
        cog.begin_broadcasting()

        display_sim_state(spectrum, [auth], [cog, other_cog])
        self.assertTrue(False) #FIXME: make sure this works

class TestMisc(unittest.TestCase):
    def test_users_on_same_freq(self):
        self.assertTrue(False)
    
    def test_users_too_close_on_same_freq(self):
        self.assertTrue(False)

    def users_wont_have_same_id(self):
        sim = Simulation()
        u1 = CognitiveUser(sim, 3, 8)
        u2 = CognitiveUser(sim, 3, 4)
        self.assertNotEqual(u1.id, u2.id)

    def users_cant_be_in_same_pos(self):
        sim = Simulation()
        u1 = CognitiveUser(sim, 3, 4)
        with self.assertRaises(Exception):
            u2 = CognitiveUser(sim, 3, 4)
    

if __name__ == '__main__':
    unittest.main()
