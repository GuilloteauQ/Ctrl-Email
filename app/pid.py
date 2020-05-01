
class PID:
    def __init__(self, variable = 0, kp = 0, ki = 0, kd = 0, delta_t = 1, max_value=3000, min_value = 0):
        self.variable = variable
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.cumulated_error = 0
        self.previous_error = 0
        self.delta_t = delta_t
        self.max_value = max_value
        self.min_value = min_value

    def update(self, error):
        self.cumulated_error += error
        proportional_term = self.kp * error
        integral_term = self.ki * self.cumulated_error * self.delta_t
        derivative_term = self.kd * (error - self.previous_error) / self.delta_t

        u = self. variable + proportional_term + integral_term + derivative_term

        if u < self.min_value:
            u = self.min_value
        if u > self.max_value:
            u = self.max_value

        self.previous_error = error
        self.variable = u

    def get(self):
        return self.variable
