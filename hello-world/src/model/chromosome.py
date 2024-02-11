import numpy as np
from typing import List, Optional

class Chromosome:

    def __init__(self, genes : int = 3, max : float = 100, seed : Optional[np.array] = None):

        # Store initial values into the object
        self.genes = genes
        self.max = max

        # Define values of the chromosomes
        # Use seed if available
        if isinstance(seed, np.ndarray):
            self.val = seed
        else:
            self.val = 2.0 * self.max * np.random.rand(self.genes) - self.max

    def fitness(self):

        return np.abs(3.0 * self.val[0]**2 + 5.2 * self.val[1]**5 - 13.0 * self.val[2]**3 - 14)