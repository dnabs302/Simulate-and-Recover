import numpy as np
import random
import math
from tabulate import tabulate #from ChatGpt

class SimulateAndRecovery:
    params = {}
    def get_model_parameters(self):
        self.params['boundary_s'] = random.uniform(0.5,2)
        self.params['drift'] = random.uniform(0.5,2)
        self.params['nond'] = random.uniform(0.1,0.5)

    def predicted_parameters(self):
        y = math.exp(-(self.params['boundary_s']*self.params['drift']))
        self.params['r_pred'] = 1/(y+1)
        self.params['m_pred'] = self.params['nond'] + ((self.params['boundary_s']/(2*self.params['drift']))*((1-y)/(1+y)))
        self.params['v_pred'] = (self.params['boundary_s']/(2*(math.pow(self.params['drift'],3))))*((1-(2*self.params['boundary_s']*self.params['drift']*y)-(math.pow(y,2)))/math.pow((y+1),2))

    def obs_parameters(self, N):
        t_obs = np.random.binomial(N, self.params['r_pred'])
        self.params['r_obs'] = t_obs/N
        self.params['v_obs'] = np.random.gamma(shape = (N-1)/2, scale = (2*self.params['v_pred'])/(N-1)) #formula partly from numpy.org, partly from slides
        std_dev = np.sqrt(self.params['v_pred'] / N)
        self.params['m_obs'] = np.random.normal(loc=self.params['m_pred'],scale=std_dev) #formula from numpy.org

    def inverse_eq(self):
        epsilon = 1e-8 
        L = math.log(self.params['r_obs'] / (1 - self.params['r_obs'] + epsilon))

        L_sq_robs = L*math.pow(self.params['r_obs'], 2)
        L_robs = self.params['r_obs']*L

        if self.params['v_obs'] == 0 or np.isnan(self.params['v_obs']):
            self.params['v_est'] = np.nan
        else:
            self.params['v_est'] = np.sign(self.params['r_obs'] - 0.5) * (math.pow(max((L * (L_sq_robs - L_robs + self.params['r_obs'] - 0.5) / (self.params['v_obs']+epsilon)),0), 1 / 4))

        self.params['a_est'] = L/(self.params['v_est'] + epsilon)
        term1 = self.params['a_est']/(2*(self.params['v_est'] + epsilon))
        term2 = -(self.params['v_est'])*(self.params['a_est'])
        self.params['t_est'] = self.params['m_obs'] - ((term1)*((1-math.exp(term2))/(1+math.exp(term2))))


    def n_simulations(self, N):
        bias = []
        sq_error = []

        for i in range(1000):
            self.get_model_parameters()
            self.predicted_parameters()
            self.obs_parameters(N)
            self.inverse_eq()

            bias.append(np.array([self.params['drift']-self.params['v_est'], self.params['boundary_s']-self.params['a_est'], self.params['nond']-self.params['t_est']]))
            sq_error.append(np.square(bias[-1]))

        self.params['b_avg'] = np.nanmean(np.array(bias))
        self.params['sq_error_avg'] = np.nanmean(np.array(sq_error)) #nanmean suggested by ChatGpt


def main():
    obj = SimulateAndRecovery()

    data = []
    for N in [10, 40, 4000]:
        obj.n_simulations(N)
        data.append([N, round(obj.params['b_avg']), obj.params['sq_error_avg']])

    print(tabulate(data, headers=["N", "b", "bsq"], tablefmt="grid"))     
if __name__ == "__main__":
    main()