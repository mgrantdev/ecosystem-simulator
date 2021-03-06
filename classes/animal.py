# import modules
import math
import random


class Animal:
    # animal entity

    def __init__(self, block_index, args):
        # static (user-defined) properties
        self.location = block_index
        self.species = args["species"]
        self.parent_species = args["parent"]
        self.max_size = args["max_size"] # x% of 100, with size of 100 representing one block
        self.min_food = args["min_food"] + (args["max_size"]/50) # minimum food required per turn
        self.movement = args["movement"]
        self.food_type = args["food_type"]
        # static calculated properties
        self.growth_rate = (self.max_size/self.min_food)
        self.sex = random.choice(['male','female'])
        self.lifespan = (self.max_size/self.growth_rate) * 2 # double the time it takes to reach full size
        self.lifespan = random.randint(math.floor(self.lifespan * .9), math.ceil(self.lifespan * 1.1)) # add variability
        if(self.lifespan == 0):
            # ensure lifespan is at least 1
            self.lifespan = 1
        self.maturity_age = math.ceil(self.lifespan * .7)
        self.offspring_max = math.ceil(self.lifespan/4)
        self.min_water = math.ceil(self.min_food/3)
        # dynamic properties
        # utility variables
        self.animal_saved = True
        # general organism variables
        self.subspecies = 0
        if "subspecies" in args:
            # override default sub species var if passed as parameter
            self.subspecies = args["subspecies"]    
        self.animal_generation = 1
        if "generation" in args:
            # override default generation var if passed as parameter
            self.animal_generation = args["generation"]
        # health/age variables
        self.animal_age = 0
        self.animal_size = 1.0
        self.animal_health_max = 100
        self.animal_health = self.animal_health_max
        self.animal_consumable_meat = self.animal_size
        self.animal_decay_index = 0
        self.animal_decay_time = 1 # calculated property
        # offspring/breeding variables
        self.animal_offspring = 0
        self.animal_is_fertile = False
        # food/water variables
        self.animal_water = 0
        self.animal_thirst = 0
        self.animal_food = 0
        self.animal_decay_tolerance = 5
        self.animal_stomach = []
        self.animal_acquired_taste = None
        # adaptationary variables
        self.preferred_terrain = "dirt"
        if "preferred_terrain" in args:
            # override default wing size var if passed as parameter
            self.preferred_terrain = args["preferred_terrain"]
        self.animal_can_fly = False
        self.animal_wing_size = 1
        if "wing_size" in args:
            # override default wing size var if passed as parameter
            self.animal_wing_size = args["wing_size"]
            if(self.animal_wing_size >= 5):
                self.movement *= 1.2
            if(self.animal_wing_size >= 25):
                self.movement *= 1.8
                self.animal_can_fly = True
        self.water_movement = 1
        if "water_movement" in args:
            # override default water movement var if passed as parameter
            self.water_movement = args["water_movement"]
        self.animal_fin_development = 1
        if "fin_development" in args:
            # override default fin development var if passed as parameter
            self.animal_fin_development = args["fin_development"]
            if(self.animal_fin_development >= 20):
                self.water_movement *= 1.8
        # species variation baseline -> if new organism, sets "baseline" for species to test for subspecies
        self.variation = self.animal_fin_development + self.min_food + self.max_size + self.water_movement + self.animal_fin_development
        self.variation_baseline =  self.animal_wing_size + self.min_food + self.max_size + self.water_movement + self.animal_fin_development
        if "variation_baseline" in args:
            # override default variation var if passed as parameter
            self.variation_baseline = args["variation_baseline"]
        self.classify_organism()

    # handle growth of the animal
    def check_growth(self):
        self.animal_age += 1 # age the animal
        self.analyze_stomach() # analyze stomach contents
        if(self.animal_food >= self.min_food and self.animal_thirst <= 0):
            # grow animal if sufficient food and water detected
            self.animal_thirst = 0 
            self.grow()
        elif(self.animal_thirst > 0):
            # otherwise, if insufficent water detected, subtract health
            self.animal_health -= 20
        if(self.animal_health > 0):
            if(self.animal_age >= self.lifespan):
                # if animal has reached the end of its lifespan, set health to zero
                self.animal_health = 0
            elif(self.animal_food < self.min_food):
                # if animal doesn't have enough food, subtract health points
                self.animal_health -= 10
                if(self.animal_food < 0):
                    # if animal has negative food, set food to zero
                    self.animal_food = 0
            elif(self.animal_size == self.max_size and self.animal_health == self.animal_health_max and self.animal_age >= self.maturity_age):
                # if animal is at maximum health and size, has reached maturity, and has not reached max offspring, mark animal as fertile
                if(self.animal_offspring < self.offspring_max):
                    # only mark animal as fertile if max offspring isn't reached
                    self.animal_is_fertile = True
                else:
                    self.animal_is_fertile = False

    # classify organism
    def classify_organism(self):
        # detect preferred terrain
        if(self.water_movement > 10):
            self.preferred_terrain = "water"
        else:
            self.preferred_terrain = "land"
        # detect species/subspecies
        if(abs(self.variation - self.variation_baseline) > (10 * self.max_size/15)):
            self.parent_species = self.species
            if("-" in self.parent_species):
                self.parent_species = self.parent_species.split("-")[0]
            self.subspecies += 1
            self.species = self.parent_species + "-variant" + str(self.subspecies)
            self.animal_saved = False

    # grow organism
    def grow(self):
        # automatically grow and heal animal
        self.animal_size += self.growth_rate
        self.animal_size = round(self.animal_size, 2) # round animal size
        self.animal_health += 10
        if(self.animal_size > self.max_size):
            # ensure size doesn't exceed maximum
            self.animal_size = self.max_size
        if(self.animal_health > self.animal_health_max):
            # ensure animal health doesn't exceed maximum
            self.animal_health = self.animal_health_max
        # update decay time and consumable meat
        self.animal_decay_time = math.ceil(self.animal_size/10)
        self.animal_consumable_meat = self.animal_size

    # analyze stomach for acquired taste
    def analyze_stomach(self):
        counter = 0
        num = None
        list = self.animal_stomach
        if(len(self.animal_stomach) > 5):
            # if stomach has sufficient content, find most frequent item
            for i in list:
                frequency = list.count(i)
                if(frequency > counter):
                    counter = frequency
                    num = i
            self.animal_acquired_taste = num
