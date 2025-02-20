import random
from alive_progress import alive_bar
import matplotlib.pyplot as plt

def createRabbit():
    return {
        'size': random.uniform(1, 10),
        'speed': random.uniform(1, 10),
        'camouflage': random.uniform(0, 1),
        'reproductiveRate': random.uniform(1, 5),
    }

def createPopulation(size):
    return [createRabbit() for _ in range(size)]

def fitness(rabbit, environment):
    predationRisk = (1 - rabbit['camouflage']) * (1 / rabbit['speed'])
    foodRequirement = rabbit['size'] * 0.5
    survivalChance = (environment['foodAvailability'] / foodRequirement) - predationRisk
    return max(0, survivalChance) * rabbit['reproductiveRate']

def select(population, environment):
    fitnessScores = [fitness(rabbit, environment) for rabbit in population]
    totalFitness = sum(fitnessScores)
    selectionProbs = [score / totalFitness for score in fitnessScores]
    selected = random.choices(population, weights=selectionProbs, k=len(population))
    return selected

def crossover(parent1, parent2, traits):
    child = {}
    for trait in traits:
        child[trait] = random.choice([parent1[trait], parent2[trait]])
    return child

def mutate(rabbit, mutationRate, traits):
    for trait in traits:
        if random.random() < mutationRate:
            if trait == 'camouflage':
                rabbit[trait] = max(0, min(1, rabbit[trait] + random.uniform(-0.1, 0.1)))
            else:
                rabbit[trait] = max(1, rabbit[trait] + random.uniform(-1, 1))
    return rabbit

def evolve(population, environment, mutationRate, traits):
    selected = select(population, environment)
    nextGeneration = []
    for i in range(0, len(selected), 2):
        if i + 1 < len(selected):
            parent1, parent2 = selected[i], selected[i + 1]
            child1 = crossover(parent1, parent2, traits)
            child2 = crossover(parent1, parent2, traits)
            nextGeneration.extend([mutate(child1, mutationRate, traits), mutate(child2, mutationRate, traits)])
    return nextGeneration

def main():
    print('/SIMULATING THE EVOLUTION OF RABBITS/')

    loop = True
    while loop:
        print()

        valid = False
        while not valid:
            try:
                populationSize = int(input('Enter a population size (e.g. 20): '))
                generations = int(input('Enter a number of generations (e.g. 50): '))
                mutationRate = float(input('Enter the chance of a mutation occurring (e.g. 0.1): '))
                valid = True
            except:
                print('Invalid input!\n')

        traits = ['size', 'speed', 'camouflage', 'reproductiveRate']
        environment = {'predators': 5, 'foodAvailability': 0.5}

        population = createPopulation(populationSize)

        avgSize = []
        avgSpeed = []
        avgCamouflage = []
        avgReproductiveRate = []

        with alive_bar(generations) as bar:
            for generation in range(1, generations + 1):

                population = evolve(population, environment, mutationRate, traits)
        
                avgTraits = {trait: 0 for trait in traits}
                for rabbit in population:
                    for trait in traits:
                        avgTraits[trait] += rabbit[trait]
                for trait in traits:
                    avgTraits[trait] /= len(population)

                avgSize.append(avgTraits['size'])
                avgSpeed.append(avgTraits['speed'])
                avgCamouflage.append(avgTraits['camouflage'])
                avgReproductiveRate.append(avgTraits['reproductiveRate'])

                bar()

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, generations + 1), avgSize, label='Average Size')
        plt.plot(range(1, generations + 1), avgSpeed, label='Average Speed')
        plt.plot(range(1, generations + 1), avgCamouflage, label='Average Camouflage')
        plt.plot(range(1, generations + 1), avgReproductiveRate, label='Average Reproductive Rate')

        plt.title('Changes in Rabbit Population Traits Over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Trait Value')
        plt.legend()
        plt.grid(True)
        plt.show()

        again = input('Simulate another (y/n)? ')
        if again.lower() != 'y':
            loop = False

if __name__ == '__main__':
    main()