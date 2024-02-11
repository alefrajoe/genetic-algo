from .chromosome import Chromosome
import numpy as np
from typing import List
from loguru import logger

class Population:

    def __init__(self, genes : int = 3, n_population : int = 1000):

        # Initialize parameters
        self.genes = genes

        # Initialize a whole population of random genes
        self.population = [Chromosome(genes=genes) for _ in range(n_population)]

    def sort(self, reverse : bool = False) -> List[Chromosome]:

        # Sort the population
        return sorted(self.population, key=lambda x : x.fitness(), reverse=reverse)

    def select(self, top_k : int = 100) -> List[Chromosome]:

        # Return the top_k chromosomes after sorting
        return self.sort()[:top_k]

    def mix_two_chromosomes(self, chromosome1 : Chromosome, chromosome2 : Chromosome) -> Chromosome:

        # Create an array of true/false
        return Chromosome(seed=np.where(np.random.rand(self.genes) >= 0.5, chromosome1.val, chromosome2.val))
    
    def mate(self, parents : List[Chromosome], n_offsprings : int = 300) -> List[Chromosome]:

        # Return the mixing of the two elements
        return [self.mix_two_chromosomes(*np.random.choice(parents, 2, replace=True)) for _ in range(n_offsprings)]
    
    def mutation(self, parents : List[Chromosome], n_mutations : int, max_mutation : float = 0.0005) -> List[Chromosome]:

        # Randomly pick n_mutations chromosomes to be mutated
        mutations = np.random.choice(parents, n_mutations, replace=True).tolist()

        # Randomly mutate each element
        return [Chromosome(seed=(chr.val + 2.0 * max_mutation * np.random.rand(self.genes) - max_mutation)) for chr in mutations]
    
    def run_generation(self, n_selection : int = 100, n_offsprings : int = 300, n_mutations : int = 600):

        # Select top k
        generation = self.select(top_k=n_selection)

        # Mate best chromosomes to create n_offsprings
        generation.extend(self.mate(generation, n_offsprings=n_offsprings))

        # Mutate chromosomes
        generation.extend(self.mutation(generation, n_mutations=n_mutations))

        # Return the new generation
        return generation

    def run_simulation(self, n_generations : int = 1000):

        # Loop over the generations
        for gen in range(n_generations):

            # Run simulation
            self.population = self.run_generation(n_selection=100, n_offsprings=300, n_mutations=600)

            # Select the best fitness
            top_fitness = self.sort()[0].fitness()

            # Print the results
            logger.info(f"Generation {gen}: top_fitness {round(top_fitness, 8)}")
