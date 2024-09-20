from random import triangular, random, choice, uniform
from rats import Rat
from time import time


GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def calculate_weight(sex, mother, father):
  
  
  
  # Use the triangular function from the random library to skew the 
  #baby's weight based on its sex
  

  if sex == "M":
    wt = int(triangular(mother.weight, father.weight, father.weight))
  else:
    wt = int(triangular(mother.weight, father.weight, mother.weight))

  return wt

def initial_population():
  '''Create the initial set of rats based on constants'''
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)
  
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1
  
    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)
  
  return rats

def select(rats, real_largest):
  '''Choose the largest viable rats for the next round of breeding'''
  canbreed = [[], []]
  largest = real_largest
  Mnum = 0
  gen_large = max(rats[0], key=lambda x:x.weight)
  gen_large2 = max(rats[1], key=lambda x:x.weight)
  if gen_large.weight < gen_large2.weight:
    gen_large = gen_large2

  gen_small = max(rats[0], key=lambda x:x.weight)
  gen_small2 = max(rats[1], key=lambda x:x.weight)
  if gen_small > gen_small2:
    gen_small = gen_small2

  while Mnum <10:
      rat = max(rats[0], key=lambda x:x.weight)
      if rat.litters < 5:
        canbreed[0].append(rat)
        Mnum +=1
      if rat.weight > largest.weight:
        largest = rat
      rats[0].remove(rat)

  Fnum = 0        
  while Fnum <10:
      rat = max(rats[1], key=lambda x:x.weight)
      if rat.litters < 5:
        canbreed[1].append(rat)
        Fnum +=1
      if rat.weight > largest.weight:
        largest = rat
      rats[1].remove(rat)

  rats = canbreed

  return rats, largest, gen_large, gen_small

def calculate_mean(rats):
  sumWt = 0
  numRats = len(rats[0]) + len(rats[1])
  for i in rats[0]:
    sumWt += i.weight
  for i in rats[1]:
    sumWt += i.weight


  return sumWt // numRats

def fitness(rats):
  """Determine if the target average matches the current population's average"""
  mean = calculate_mean(rats)
  return mean >= GOAL, mean

def mutate(pups):
  """Check for mutability, modify weight of affected pups"""
  for i in pups:
    odds = random()
    if odds <= MUTATE_ODDS:
      i.weight *= uniform(MUTATE_MIN, MUTATE_MAX)
  return pups

def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""
  pups = []
  pairs = [[], [], [], [], [], [], [], [], [], []]
  for i in pairs:
    pairs[pairs.index(i)].append(rats[0][pairs.index(i)])
    pairs[pairs.index(i)].append(rats[1][pairs.index(i)])

  sexlist = ["M", "F"]
  for h in pairs:
    
    parent1 = h[0]
    parent2 = h[1]
    for i in range(0, LITTER_SIZE):
      sex = choice(sexlist)
      wt = calculate_weight(sex, parent2, parent1)
      pup = Rat(sex, wt)
      pups.append(pup)
    parent1.litters += 1
    parent2.litters += 1


  return pups  

def main():
  time1 = time()
  gen_amm = 1
  years = 0
  rats = initial_population()
  average_weights = []
  largest = Rat("M", 0)
  fullmean = 0
  gen_largests = []
  gen_smallests = []
  while years < 50:
    
    mean = calculate_mean(rats)
    average_weights.append(f"{int(mean)}")
    rats, largest, gen_large, gen_small = select(rats, largest)
    gen_largests.append(str(gen_large.weight))
    gen_smallests.append(str(gen_small.weight))
    pups = breed(rats)
    pups = mutate(pups)
    for i in pups:
      if i.sex == "M":
        rats[0].append(i)
      else:
        rats[1].append(i)
        pups.remove(i)
    
    if mean >= GOAL:
      break
    gen_amm += 1
    if gen_amm % 10 == 0:
      years +=1
  
  printavgwt = ', '.join(average_weights)
  file = "gen_large.txt"
  f = open(file, 'w')
  f.write(", ".join(gen_largests))
  f.close()

  file = "gen_small.txt"
  f = open(file, 'w')
  f.write(", ".join(gen_smallests))
  f.close()

  file = "gen_avg.txt"
  f = open(file, 'w')
  f.write(", ".join(average_weights))
  f.close()

  print(f"\nTotal generations: {gen_amm}")
  print(f"Total years: {years}")
  print(f"Time ran: {time() - time1}")
  print(f"\nAverage weight for each generation: \n{printavgwt}")
  print(f"\nLargest Rat: {largest.sex} {int(largest.weight)}")

  



