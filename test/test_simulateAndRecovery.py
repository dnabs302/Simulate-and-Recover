import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src.simulateAndRecovery import SimulateAndRecovery

class TestSimulateAndRecovery(unittest.TestCase):
    sar = SimulateAndRecovery()

    def test_get_model_parameters(self):
        boundary_sep, drift_rt, nondec = self.sar.get_model_parameters()
        self.assertTrue(0.5 <= boundary_sep <= 2)
        self.assertTrue(0.5 <= drift_rt <= 2)
        self.assertTrue(0.1 <= nondec <= 0.5)

    def test_predicted_parameters(self):
        boundary_sep, drift_rt, nondec = 1.6, 1.1, 0.2
        R_pred, M_pred, V_pred = self.sar.predicted_parameters(boundary_sep, drift_rt, nondec)
        self.assertTrue(0 <= R_pred <= 1)
        self.assertTrue(M_pred > nondec)
        self.assertTrue(V_pred > 0)

    def test_inverse_equations(self):
        boundary_sep, drift_rt, nondec = 1.6, 1.1, 0.2
        r_pred, m_pred, v_pred = self.sar.predicted_parameters(boundary_sep, drift_rt, nondec)
        t_obs, r_obs, v_obs, m_obs = self.sar.obs_parameters(1000, r_pred, m_pred, v_pred)
        v_est, a_est, t_est = self.sar.inverse_eq(r_obs, v_obs, m_obs)
        self.assertAlmostEqual(boundary_sep, a_est, delta=0.2)
        self.assertAlmostEqual(drift_rt, v_est, delta=0.2)
        self.assertAlmostEqual(nondec, t_est, delta=0.1)

    def test_b_avg_zero(self):
        for N in [10, 40, 4000]:
            b_avg, sq_error_avg = self.sar.n_simulations(N)
            self.assertAlmostEqual(b_avg, 0, places=0)
    
    def test_sq_error_decreasing(self):
        obj = SimulateAndRecovery()

        prev_sq_error_avg = None
        for N in [10, 40, 4000]:
            _, sq_error_avg = obj.n_simulations(N)
            if prev_sq_error_avg is not None:
                self.assertGreaterEqual(prev_sq_error_avg, sq_error_avg)
            prev_sq_error_avg = sq_error_avg

if __name__ == "__main__":
    unittest.main()