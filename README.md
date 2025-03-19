+------+-----+

|   N |   b |          bsq |

+======+=====+

|   10 |   0 | 1.76898     |

+------+-----+

|   40 |   0 | 0.278999    |

+------+-----+

| 4000 |   0 | 0.000440895 |

+------+-----+

Results of simulateAndRecovery.py


[In the assignment description it was mentioned that ideally the average value for bias should converge to 0 and that squared error should decrease as the number of trials increased. An explanation for the same is given below]

As seen above, the average values for bias (b_avg) converge to 0. I opted to round the values obtained to the nearest whole number for convenience and to allow for quick comparisons. If the average value obtained for bias (b_avg) converges to zero it means that on average, the estimated parameter values align with the ‘true’ original assumed values for the parameters of boundary separation, drift rate, and non-decision time. Given that the value converges to zero, the EZ Diffusion model so implemented is unbiased, and therefore, ‘good.’ 

A decreasing trend of squared error values as the number of trials increases implies that the model is displaying precision (estimated values are closer to actual/true values). As seen in the attached image, the values for squared error decrease, and the number of trials (N) increases from 10 to 40 to 4000. This trend is evidence that with larger sample sizes, the model becomes more precise, and aligns with the expected trend of a ‘good’ implementation of the EZ Diffusion model.

To further explain the code and its functions:

With regards to the code contained in simulateAndRecovery.py, the following functions:
get_model_parameters(): Generates random values for the parameters of boundary separation, drift rate, and non-decision time as required, and stores them in a dictionary.
predicted_ parameters(): Predict values for R^pred, M^pred, and V^pred in accordance with the formulae provided in the slides, and stored in the dictionary.
- obs_parameters(): Calculates R^obs, M^obs, and V^obs in accordance with the instructions in the slides
- inverse_eq(): Provided estimates for the values of boundary separation, drift rate, and non-decision time in accordance with the formulae in the slides, and stored in a global dictionary.
To correct for the highly unlikely situations where R^obs could be 0, I added the value of Epsilon (1e-8). The extremely small value of the same allows the model to proceed with the required mathematical calculations without compromising much on its validity and/or accuracy.
- n_simulations(): The functions listed above are iterated 1000 times (as required), and the values for the averages of bias and squared error are calculated. These values are stored in an array.
Finally, the values of average bias and squared error are displayed in tabular form for ease of comparison.

For the code contained in the TestSimulateAndRecovery.py file, I have included tests that aim to verify whether or not the code in simulateAndRecovery.py executes its functions correctly. 
- test_get_model_parameters(): Check if the required parameters required to understand an EZ Diffusion model, namely boundary separation (alpha), drift rate (v), and non-decision time (T) are within the recommended bounds. 
- test_predicted_parameters(): Confirm that the values obtained for R^pred, M^pred, and V^pred are in accordance with the equations used and are mathematically sound. 
- test_inverse_eq(): Ensures that the estimated values so calculated are within reasonable error from the original parameters obtained from the data, i.e., the estimated value of boundary separation (alpha) should be within a minor error range from the originally assumed boundary separation value, and so on for the other parameters. 
- test_b_avg_zero(): Verify that the average bias value converges to zero as is to be expected in the EZ Diffusion model results. 
- test_sq_error_decreasing(): Confirm that the average values of the squared error decrease as the number of trials (N) increases. 
