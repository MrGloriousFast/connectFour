import random

from ai.bot_base import BotBase
import numpy as np

'''
The NEAT brain class.
This is the only class we will have to deal with from the outside
'''


class NEATBrain(BotBase):
    def __init__(self, in_dimension, out_dimension, genome=None):
        super().__init__()
        self.name = 'NEAT Brain'

        self.noise = 0.0
        self.inverted_team_color = False

        if genome is None:
            self.genome = Genome(in_dimension, out_dimension)
        else:
            self.genome = genome

        self.pheno = Pheno(self.genome)

    def choose_action(self, field, action_list, player_color):

        #gamefield is 2d array and we have to make it into a list
        in_list = []

        # invert player colors
        # so the bot doesnt optimize to play only one color
        #for the bot it looks like he always plays in his own team
        invert = False
        if player_color == 1:
            invert = True

        for ii in np.nditer(field):
            if ii == -1:
                in_list.append(0.1)
            if invert:
                if ii == 1:
                    in_list.append(0.5)
                if ii == 0:
                    in_list.append(0.9)
            else:
                if ii == 0:
                    in_list.append(0.5)
                if ii == 1:
                    in_list.append(0.9)
        if invert:
            if player_color == 0:
                player_color == 1
            else:
                player_color == 0
        in_list.append(player_color)

        #give him a warning that there is one illegal move possible
        if len(action_list) < 7:
            in_list.append(1.0)
        else:
            in_list.append(0.0)

        # apply noise
        if self.noise != 0.0:
            for i in in_list:
                i += random.uniform(-self.noise, self.noise)

        self.apply_input(in_list)

        # more than once so the network can grow deeper
        self.propagate()
        self.propagate()
        self.propagate()

        '''
        output = self.get_output()[0]
        output *= 7.0

        decision = 0
        if output < 1.0:
            decision = 0
        elif output < 2.0:
            decision = 1
        elif output < 3.0:
            decision = 2
        elif output < 4.0:
            decision = 3
        elif output < 5.0:
            decision = 4
        elif output < 6.0:
            decision = 5
        else:
            decision = 6

        return decision
        '''
        return self.get_output(max_pool=True)

    def apply_input(self, in_array):
        self.pheno.apply_input(in_array)

    def get_output(self, max_pool=False):
        return self.pheno.get_output(max_pool)

    def propagate(self):
        # everyone neuron is updated once
        # unpredictable order
        self.pheno.propagate()

    def mutate(self):
        self.genome.mutate()
        self.pheno = Pheno(self.genome)

    def to_string(self):
        g_string = ''
        for g in self.genome.gen_dict:
            n = self.genome.gen_dict[g]
            g_string += n.type + ' id ' + str(g)+'\n'
            g_string += '\tinnovation ' + str(n.innovation) + '\n'
            if n.type == 'connection':
                g_string += '\tenabled ' + str(n.enabled) + '\n'
                g_string += '\tfrom ' + str(n.in_neuron) + '\n'
                g_string += '\tto ' + str(n.out_neuron) + '\n'
                g_string += '\tweight ' + str(n.weight) + '\n'

        p_string = ''
        p_string += 'Neurons ' + str(len(self.pheno.neuron_list)) + '\n'
        p_string += 'Connections ' + str(self.pheno.connection_counter) + '\n'

        '''
        for ii in self.pheno.neuron_list:
            n = self.pheno.neuron_list[ii]
            p_string += str(n) + '\n'
            p_string += '\tid ' + str(ii) + '\n'
            p_string += '\tlast output' + str(n.last_output) + '\n'

            if isinstance(n, Neuron):
                for c in n.connections:

                    p_string += '\t\tto ' + str(c.in_neuron) + ' weight ' + str(c.weight) + '\n'
        '''
        result = ''
        result += 'Genome' + '\n' + g_string + '\n'
        result += 'Phenom' + '\n' + p_string + '\n'

        return result

    def get_clone(self):
        clone = NEATBrain(self.genome.in_dimension, self.genome.out_dimension, self.genome)
        return clone


'''
A genome is a collection of genes.
Its the coded representation of the NEAT brain
'''


class Genome:
    def __init__(self, in_dimension, out_dimension):
        self.gen_dict = {}
        self.in_dimension = in_dimension
        self.out_dimension = out_dimension
        self.innovation_counter = 0

        self.node_counter = 0

        # create nodes that have to be present regardless of evolution
        self.create_input()
        self.create_output()
        self.create_bias()

    # create all genes which define input neurons
    def create_input(self):
        for _ in range(self.in_dimension):

            inn = GenIn(self.innovation_counter)
            self.gen_dict[str(self.innovation_counter).zfill(5)] = inn
            self.innovation_counter += 1
            self.node_counter += 1

    # create all genes which define output neurons
    def create_output(self):
        for _ in range(self.out_dimension):

            o = GenOut(self.innovation_counter)
            self.gen_dict[str(self.innovation_counter).zfill(5)] = o
            self.innovation_counter += 1
            self.node_counter += 1

    # create a gene which defines a bias neuron
    def create_bias(self):
        b = GenBias(self.innovation_counter)
        self.gen_dict[str(self.innovation_counter).zfill(5)] = b
        self.innovation_counter += 1
        self.node_counter += 1

    # create a gene which defines a bias neuron
    def create_random_node(self):
        r = GenRand(self.innovation_counter)
        self.gen_dict[str(self.innovation_counter).zfill(5)] = r
        self.innovation_counter += 1
        self.node_counter += 1

    # either create a new connection or change the weight
    def create_connection(self, node0, node1, weight):
        if str(node0+node1) not in self.gen_dict:

            g = GenNeuron(self.innovation_counter, node0, node1, weight)
            self.gen_dict[str(node0+node1)] = g
            self.innovation_counter += 1


    def change_connection_weight(self, node0, node1, weight):
        if str(node0 + node1) in self.gen_dict:
            self.gen_dict[str(node0 + node1)].weight += weight

    def enable_flip(self, gen):
        if gen in self.gen_dict:
            if self.gen_dict[gen].type == 'connection':
                self.gen_dict[gen].enabled = not self.gen_dict[gen].enabled

    def create_node_from_connection(self, node0, node1, weight):
        if str(node0 + node1) not in self.gen_dict:
            return
        else:

            '''
            from this:
            old_g = (node0,     weight,     new_node )
            
            to this:
            old_g = (node0,     weight,     new_node )
            new_g = (new_node , new_weight, node1)
            '''

            #get the old connection
            old_g = self.gen_dict[node0+node1]

            #make a new new Node
            new_node = str(self.node_counter).zfill(5)
            self.node_counter += 1

            #connect the old one correctly now
            old_g.out_neuron = new_node

            #make a new Gen
            new_g = GenNeuron(self.innovation_counter, self.node_counter, node1, weight)

            self.gen_dict[str(self.innovation_counter).zfill(5)] = new_g
            self.innovation_counter += 1

    # create a new connection between two random picked nodes (or change the weight if a connection already exists)
    def mutate(self):
        # probabilities for mutations
        prob_enable = 10
        prop_new_node = 1
        prop_new_connection = 25
        prop_weight_change = 70

        # values we have to pick anyway regardless of which mutation we choose
        node0 = random.randint(0, self.node_counter)
        node0 = str(node0).zfill(5)

        node1 = random.randint(0, self.node_counter)
        node1 = str(node1).zfill(5)
        r = 1.0
        weight = random.uniform(-r, r)

        # random choosing a mutation
        # if no connection is already between both nodes we will only be able to connect them
        random_number = random.randint(0, prop_new_node + prop_new_connection + prop_weight_change + prob_enable)
        if random_number < prop_new_node and str(node0+node1) in self.gen_dict:
            # make a new node
            self.create_node_from_connection(node0, node1, weight)
        elif random_number < prop_weight_change + prop_new_node and str(node0+node1) in self.gen_dict:
            # change the connection
            self.change_connection_weight(node0, node1, weight)
        elif random_number < prop_weight_change + prop_new_node + prop_new_connection:
            # make a new connection between those two nodes
            self.create_connection(node0, node1, weight)
        else:
            gen = random.choice(list(self.gen_dict.keys()))
            self.enable_flip(gen)

        # hard limit for connections/nodes
        max_genes = 100000
        if len(self.gen_dict.keys()) > max_genes:
            #print(' genome is too big! reached ' + str(len(self.gen_dict.keys())))
            #print('removing random genes !')
            while len(self.gen_dict.keys()) > max_genes:
                random_gene = random.choice(list(self.gen_dict.keys()))
                if self.gen_dict[random_gene].type == 'connection':
                    self.gen_dict.pop(random_gene)
            #print( 'mutant has ' + str(len(self.gen_dict.keys())) + ' genes')


"""
One gene.
It hold information of who is connected with whom and how strongly
Inspiration from: https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume21/stanley04a-html/node3.html
"""


class GenBase:
    def __init__(self, innovation):
        self.innovation = innovation
        self.type = 'base'


class GenBias(GenBase):
    def __init__(self, innovation):
        super().__init__(innovation)
        self.type = 'bias'

class GenRand(GenBase):
    def __init__(self, innovation):
        super().__init__(innovation)
        self.type = 'rand'


class GenIn(GenBase):
    def __init__(self, innovation):
        super().__init__(innovation)
        self.type = 'in'


class GenOut(GenBase):
    def __init__(self, innovation):
        super().__init__(innovation)
        self.type = 'out'


class GenNeuron(GenBase):
    def __init__(self, innovation, id_neuron0, id_neuron1, weight):
        super().__init__(innovation)
        self.type = 'connection'
        self.enabled = True
        self.in_neuron = id_neuron0 # string eg: 0001
        self.out_neuron = id_neuron1 # string
        self.weight = weight


'''
Phenotype representation of one Genome
Made out of neurons
'''


class Pheno():
    def __init__(self, genome = None):
        self.neuron_list = {}
        self.input_list = []
        self.output_list = []
        self.connection_counter = 0

        # create nodes that are defined by the genome
        if genome is not None:
            self.create_from_genome(genome)

    def create_from_genome(self, genome):
        # create all necessary neurons
        for g in genome.gen_dict.values():
            if g.type == 'in':
                s = Sensor()
                id = self.get_id()
                self.neuron_list[id] = s
                self.input_list.append(s)

            if g.type == 'out':
                n = Neuron()
                id = self.get_id()
                self.neuron_list[id] = n
                self.output_list.append(n)

            if g.type == 'bias':
                b = Bias()
                id = self.get_id()
                self.neuron_list[id] = b

            if g.type == 'bias':
                r = Rand()
                id = self.get_id()
                self.neuron_list[id] = r


            if g.type == 'connection':
                i = str(g.in_neuron).zfill(5)
                o = str(g.out_neuron).zfill(5)
                if i not in self.neuron_list:
                    self.neuron_list[i] = Neuron()
                if o not in self.neuron_list:
                    self.neuron_list[o] = Neuron()

        # now we can create all necessary connections
        # create all connections/weights
        for g in genome.gen_dict.values():
            if g.type == 'connection' and g.enabled:
                i = str(g.in_neuron).zfill(5)
                o = str(g.out_neuron).zfill(5)
                c = Connection(g.weight, self.neuron_list[i])
                self.neuron_list[o].connections.append(c)
                self.connection_counter += 1

    def get_id(self):
        return str(len(self.neuron_list)).zfill(5)

    def apply_input(self, in_array):
        if len(in_array) != len(self.input_list):
            print('wrong input dimension. We have ', len(self.input_list), ' you want ', len(in_array))

        for i in range(0, len(in_array)):
            self.input_list[i].set_value(in_array[i])

    # every neuron works once
    def propagate(self):
        for n in self.neuron_list.values():
            n.propagate()

    def get_output(self, max_pool=False):
        out_list = []
        for o in self.output_list:
            out_list.append(o.get_output())

        if max_pool:
            return out_list.index(max(out_list))
        else:
            return out_list


'''
one neuron made out of activation function and input connections
'''


class Neuron:
    def __init__(self):
        self.activation_function = 1
        self.last_output = 0.0
        self.connections = []

    def propagate(self):
        # add up all inputs
        sum = 0.0
        for c in self.connections:
            sum += c.get_value()

        # use the proper activation function
        if self.activation_function == 0:
            self.last_output = self.sigmoid(sum)
        elif self.activation_function == 1:
            self.last_output = self.linear(sum)

    def get_output(self):
        return self.last_output

    def sigmoid(self, x, derivative=False):
        if derivative:
            return x * (1.0 - x)
        return 1.0 / (1.0 + np.exp(-x))

    def linear(self, x):
        # return x
        if x < 0:
            return x*0.05
        else:
            return x


# input Node
class Sensor(Neuron):
    def __init__(self):
        super().__init__()

    def set_value(self, value):
        self.last_output = value

    def propagate(self):
        return


# bias, constant output of 1.0
class Bias(Neuron):
    def __init__(self):
        super().__init__()

    def get_output(self):
        return 1.0

    def propagate(self):
        return

# bias, constant output of 1.0
class Rand(Neuron):
    def __init__(self):
        super().__init__()

    def get_output(self):
        return random.uniform(0.0, 1.0)

    def propagate(self):
        return


'''
One connection between two neurons.
directed and weighted
'''


class Connection():
    def __init__(self, weight, neuron):
        self.weight = weight
        self.in_neuron = neuron

    def get_value(self):
        return self.weight*self.in_neuron.get_output()


'''
# test
net = NEATBrain(10, 7)
for _ in range(0):
    net.mutate()
#print(net.to_string())

random_input = []
for i in range(0, 10):
    random_input.append(random.uniform(-1.0, 1.0))

for _ in range (10):
    net.apply_input(random_input)
    net.propagate()
    print('output ', net.get_output(True), net.get_output())
'''