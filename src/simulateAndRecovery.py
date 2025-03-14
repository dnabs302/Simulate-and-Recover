import numpy as np
import random
import math

class SimulateAndRecovery:
    def get_model_parameters(self):
        boundary_sep = random.uniform(0.5,2)
        drift_rt = random.uniform(0.5,2)
        nondec = random.uniform(0.1,0.5)
        return boundary_sep, drift_rt, nondec

    def predicted_parameters(self, boundary_sep, drift_rt, nondec):
        y = math.exp(-(boundary_sep*drift_rt))
        r_pred = 1/(y+1)
        m_pred = nondec + ((boundary_sep/(2*drift_rt))*((1-y)/(1+y)))
        v_pred = (boundary_sep/(2*(math.pow(drift_rt,3))))*((1-(2*boundary_sep*drift_rt*y)-(math.pow(y,2)))/math.pow((y+1),2))
        return r_pred, m_pred, v_pred

    def obs_parameters(self, N, r_pred, m_pred, v_pred):
        t_obs = np.random.binomial(N, r_pred)
        r_obs = t_obs/N
        #m_obs = np.random.normal(m_pred, v_pred/N)
        v_obs = np.random.gamma(shape = (N-1)/2, scale = (2*v_pred)/(N-1)) #formula partly from numpy.org, partly from slides
        std_dev = np.sqrt(v_pred / N)
        m_obs = np.random.normal(loc=m_pred,scale=std_dev) #formula from numpy.org
        return t_obs, r_obs, v_obs, m_obs

    def inverse_eq(self, r_obs, v_obs, m_obs):
        epsilon = 1e-8 

        L = math.log(r_obs / (1 - r_obs)) if r_obs != 1 else 1  #ask prof if its okay to assume 1
        L_sq_robs = L*math.pow(r_obs, 2)
        L_robs = r_obs*L
        v_est = np.sign(r_obs - 0.5)*(math.pow(L * (L_sq_robs - L_robs + r_obs - 0.5) / (v_obs),1/4))

        a_est = L/v_est

        term1 = a_est/(2*v_est)
        term2 = -(v_est)*(a_est)
        t_est = m_obs - ((term1)*((1-math.exp(term2))/(1+math.exp(term2))))

        return v_est, a_est, t_est

    def n_simulations(self, N):
        bias = []
        sq_error = []

        for i in range(1000):
            boundary_sep, drift_rt, nondec = self.get_model_parameters()
            r_pred, m_pred, v_pred = self.predicted_parameters(boundary_sep, drift_rt, nondec)
            t_obs, r_obs, v_obs, m_obs = self.obs_parameters(N, r_pred, m_pred, v_pred)
            v_est, a_est, t_est = self.inverse_eq(r_obs, v_obs, m_obs)

            bias.append(np.array([drift_rt-v_est, boundary_sep-a_est, nondec-t_est]))
            sq_error.append(np.square(bias[-1]))

        b_avg = np.nanmean(bias)
        sq_error_avg = np.nanmean(sq_error) #nanmean suggested by ChatGpt

        return b_avg, sq_error_avg

def main():
    obj = SimulateAndRecovery()

    print("N   b   bsq")
    for N in [10, 40, 4000]:
        b_avg, sq_error_avg = obj.n_simulations(N)
        print(N, " ", round(b_avg ,1), " ", sq_error_avg)    #verify look of output
            
if __name__ == "__main__":
    main()


    


   
  