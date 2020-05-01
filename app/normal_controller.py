import scipy.stats

class NormalController:
    def __init__(self, variable = 0, mean = 0, sd = 1, min_value = 5 * 60, max_value = 3600):
        self.variable = variable
        self.mean = mean
        self.sd = sd
        self.pdf = lambda x: scipy.stats.norm(self.mean, self.sd).pdf(x)
        self.g = lambda x: max_value - (max_value - min_value) * self.pdf(x) / self.pdf(mean)

    def update(self, current_time):
        self.variable = int(self.g(current_time))

    def get(self):
        return self.variable
