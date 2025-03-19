import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src.simulateAndRecovery import SimulateAndRecovery

class TestSimulateAndRecovery(unittest.TestCase):
    sar = SimulateAndRecovery()

    def test_get_model_parameters(self):
        self.sar.get_model_parameters()
        self.assertTrue(0.5 <= self.sar.params['boundary_s'] <= 2)
        self.assertTrue(0.5 <= self.sar.params['drift'] <= 2)
        self.assertTrue(0.1 <= self.sar.params['nond'] <= 0.5)

    def test_predicted_parameters(self):
        self.sar.params['boundary_s'], self.sar.params['drift'], self.sar.params['nond'] = 1.6, 1.1, 0.2
        self.sar.predicted_parameters()
        self.assertTrue(0 <= self.sar.params['r_pred'] <= 1)
        self.assertTrue(self.sar.params['m_pred'] > self.sar.params['nond']) #to ensure values are mathematically reasonable
        self.assertTrue(0 < self.sar.params['v_pred']) #to ensure the correct decisions are being made

    def test_inverse_equations(self):
        self.sar.params['boundary_s'], self.sar.params['drift'], self.sar.params['nond'] = 1.6, 1.1, 0.2
        self.sar.predicted_parameters()
        self.sar.obs_parameters(1000)
        self.sar.inverse_eq()
        self.assertAlmostEqual(self.sar.params['boundary_s'], self.sar.params['a_est'], delta=0.2)
        self.assertAlmostEqual(self.sar.params['drift'], self.sar.params['v_est'], delta=0.2)
        self.assertAlmostEqual(self.sar.params['nond'], self.sar.params['t_est'], delta=0.1)

    def test_b_avg_zero(self):
        for N in [10, 40, 4000]:
            self.sar.n_simulations(N)
            self.assertAlmostEqual(self.sar.params['b_avg'], 0, places=0)
    
    def test_sq_error_decreasing(self):
        obj = SimulateAndRecovery()

        prev_sq_error_avg = None
        for N in [10, 40, 4000]:
            obj.n_simulations(N)
            if prev_sq_error_avg is not None:
                self.assertGreaterEqual(prev_sq_error_avg, self.sar.params['sq_error_avg'])
            prev_sq_error_avg = self.sar.params['sq_error_avg']

if __name__ == "__main__":
    unittest.main()