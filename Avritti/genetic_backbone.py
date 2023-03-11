import random as rd


class Genome:

    def __init__(self, length: int, mutation_probability=0.1, list_genome=None):
        '''
        Creates a list of 1's and 0's of the specified length
        '''
        self.length = length
        self.genome = rd.choices([0, 1], k=self.length)
        self.mutation_probability = mutation_probability
        if list_genome is not None:
            self.genome = list_genome

    def __str__(self):
        return "".join(map(str, self.genome))

    def mutation(self):
        '''
        Modify the genome
        '''
        index = rd.randrange(self.length)
        self.genome[index] = abs(self.genome[index] - 1) if rd.random() < self.mutation_probability else self.genome[index]

    def __add__(self, genome):
        '''
        Implemetation of crossover function
        '''
        position = rd.randint(1, self.length-1)
        return (Genome(self.length, list_genome=self.genome[0:position] + genome.genome[position:]),
                Genome(self.length, list_genome=genome.genome[0:position] + self.genome[position:]))


class Population:

    def __init__(self, population_size, genome_size, fitness_function):
        self.population_size = population_size
        self.genome_size = genome_size
        self.population = [Genome(length=genome_size)
                           for i in range(population_size)]
        self.fitness_values = [0 for i in range(population_size)]
        self.parents = [None, None]
        self.fitness_function = fitness_function

    def __str__(self):
        return ", ".join(map(str, self.population))

    def fitness(self):
        '''
        Takes a fitness function and calculates the fitness value 
        for the genomes according to the fitness function
        '''
        for i, genome in enumerate(self.population):
            genome_fitness = self.fitness_function(genome)
            self.fitness_values[i] = genome_fitness

    def parent_selection(self):
        '''
        Choose parents from the population
        based on the fitness functoin
        '''
        self.parents = rd.choices(
            population=self.population,
            weights=self.fitness_values,
            k=2
        )

    def sort_population(self):
        '''
        Sort population based on fitness value
        '''
        self.population.sort(key=self.fitness_function, reverse=True)
        self.fitness_values.sort(reverse=True)

    def move_generation(self, debug=True):
        self.fitness()
        self.sort_population()
        if self.fitness_values[0] == self.genome_size:
            return True
        if debug:
            for p in self.population:
                print(p, end=" ")
            print(f"\nFitness Values: {self.fitness_values}")
        next_generation = self.population[:2]

        
        for i in range(self.population_size // 2 - 1):
            self.parent_selection()
            if debug:
                print(self.parents[0], self.parents[1])
            offsprings = self.parents[0] + self.parents[1]
            offsprings[1].mutation(), offsprings[0].mutation()
            next_generation += [offsprings[0], offsprings[1]]

        self.population = next_generation
        return False


def fit(genome: Genome):
    # count1 = 0
    # for i in range(genome.length):
    #     if genome.genome[i] == 1:
    #         count1 += 1
    return rd.randint(0,6)


# popn = Population(10, 16, fit)
# for i in range(1000):
#     if popn.move_generation(debug=False):
#         print(i, popn.population[0])
#         break

