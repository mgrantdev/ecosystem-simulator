# import modules
import math
import random
from classes.block import *

class Environment:

    boundary_check_indexes = []

    # initialize environment
    def __init__(self, size, water_percentage, water_distribution, rainfall_frequency):

        # create gameboard array
        self.env_tiles = [None] * (size * size)
        tile_index = 0
        for x in self.env_tiles:
            self.env_tiles[tile_index] = Block()
            tile_index += 1
        # reassign variables
        self.env_size = size * size
        self.env_water_percentage = water_percentage
        self.env_water_distribution = water_distribution
        self.env_rainfall_frequency = rainfall_frequency
        # generation variables
        self.env_water_clusters = 0
        # run generator method
        self.generate()
        self.debug()

    # generate environment
    def generate(self, reset = False):
        # if reset parameter detected, reset gameboard array
        if(reset):
            tile_index = 0
            for x in self.env_tiles:
                self.env_tiles[tile_index].reset_terrain()
                tile_index += 1
        # calculate ideal number of clusters given user parameters
        water_clusters_max = math.ceil((self.env_size/30) * (self.env_water_distribution/100))
        water_blocks_max = math.ceil((self.env_water_percentage/100) * self.env_size)
        # if water percentage is greater than zero, ensure there's at least one cluster
        if(self.env_water_percentage > 0 and water_clusters_max == 0):
            water_clusters_max = 1
        print("maximum clusters allowed->{}".format(water_clusters_max)) # debug
        while(len(self.get_water_blocks()) < water_blocks_max):
            # select random tile as starting point for new cluster
            rand_index = random.randint(0, len(self.env_tiles)-1)
            current_tile = self.env_tiles[rand_index]
            cursor = rand_index # cursor to guide expansion of cluster
            print("start->{}".format(rand_index)) # debug
            if(current_tile.terrain_generated == False):
                # create starting point for cluster
                current_tile.set_terrain("water", random.randint(3, 5))
                cluster_created = False
                # expand cluster
                while(cluster_created == False):
                    cluster_expansion_chance = random.randint(0, 100)
                    boundary_indexes = [cursor+1, cursor-1, int(cursor+math.sqrt(self.env_size)), int(cursor-math.sqrt(self.env_size))]
                    random.shuffle(boundary_indexes)
                    cluster_size = math.floor(random.randint(math.ceil(self.env_size * 0.25), math.ceil(self.env_size * 0.75)) * (5/self.env_water_distribution))
                    if(cluster_size > self.env_size):
                        # ensure cluster is not larger than its environment
                        cluster_size = math.floor(random.randint(math.ceil(self.env_size * 0.25), math.ceil(self.env_size * 0.75)) * (1/self.env_water_distribution))
                    # chance of expansion is dependent on user parameter "env_water_percentage"; 100% water translates to 100% chance of cluster expanding
                    if(cluster_expansion_chance <= self.env_water_percentage):
                        for x in boundary_indexes:
                            if(self.check_tile_boundary(x)):
                                if(self.env_tiles[x].terrain_generated == False):
                                    if(len(self.get_water_blocks()) < water_blocks_max):
                                        # print("cluster_max->{}, current water cluster size->{}, total water clusters->{}".format(local_max, len(water_cluster), self.env_water_clusters)) # debug
                                        layer_height = random.randint(3, 5)
                                        self.expand_water_cluster(x, layer_height, water_blocks_max) # loop until cluster is created
                                        # print("index->{}".format(x)) # debug
                                        self.env_tiles[x].set_terrain("water", layer_height)
                        # if no expansion possible, break loop
                        # print("endpoint->root method, no expansion possible (exhausted all boundaries)") # debug
                        cluster_created = True
                    else:
                        # if no expansion possible, break loop
                        # print("endpoint->root method, no expansion possible (low chance of expansion due to water percentage in environment)") # debug
                        cluster_created = True
        # if insufficient water tiles created, recall generator
        if(len(self.get_water_blocks()) != water_blocks_max):
          self.generate(True)

    def expand_water_cluster(self, index, height, global_max):
        cluster_expansion_chance = random.randint(0, 100)
        boundary_indexes = [index+1, index-1, int(index+math.sqrt(self.env_size)), int(index-math.sqrt(self.env_size))]
        random.shuffle(boundary_indexes)
         # chance of expansion is dependent on user parameter "env_water_percentage"; 100% water translates to 100% chance of cluster expanding
        if(cluster_expansion_chance <= self.env_water_percentage):
            for x in boundary_indexes:
                if(self.check_tile_boundary(x)):
                    if(self.env_tiles[x].terrain_generated == False):
                        if(len(self.get_water_blocks()) < global_max):
                            # print("cluster_max->{}, current water cluster size->{}, total water clusters->{}".format(local_max, len(water_cluster), self.env_water_clusters)) # debug
                            # print("sub-index->{}".format(x)) # debug
                            new_height = height - 1
                            if(new_height < 1):
                                new_height = 1
                            self.expand_water_cluster(x, new_height, global_max)
                            self.env_tiles[x].set_terrain("water", random.randint(3, 5))
                            # print("current blocks:{}, max:{}".format(len(self.get_water_blocks()), max)) # debug
                        else:
                            break
            # if no expansion possible, break loop
            # print("endpoint->root method, no expansion possible (exhausted all boundaries)") # debug
            cluster_created = True
        else:
            # print("endpoint->recursive method, no expansion possible (low chance of expansion due to water percentage in environment)") # debug
            cluster_created = True

    # generate water clusters
    def generate_water_clusters(self, water_clusters_max):
        water_clusters_created = 0

    # check if tile exists
    def check_tile_boundary(self, index):
        if(index > self.env_size-1 or index < 0):
            return False
        else:
            return True

    def get_water_blocks(self):
        blocks = []
        for x in self.env_tiles:
            if(x.terrain_type == "water"):
                blocks.append(x)
        return blocks


    # debug function
    def debug(self):
        # show block data
        coordinate = 0
        terrain_types = {"dirt":0, "water":0}
        for x in self.env_tiles:
            print("({}) terrain_type->{}, terrain_depth->{}, cluster->{}".format(coordinate, x.terrain_type, x.terrain_depth, x.terrain_group))
            # tally block terrain types
            if(x.terrain_type == "water"):
                terrain_types["water"] += 1
            elif(x.terrain_type == "dirt"):
                terrain_types["dirt"] += 1
            coordinate += 1
        print(terrain_types)
        






