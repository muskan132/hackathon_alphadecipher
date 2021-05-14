from collections import defaultdict

class Graph():

    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight




class eval:
    def __init__(self):
        self.location_dict = {"Khardung La": ["A", (0, 10)], "Lachulang La":["B", (10, 20)], "Sasser Pass":["C", (10, 10)],
                        "Gyong La":["D", (10, 0)], "Sia La":["E", (20, 20)], "Zoji La":["F", (20, 10)],
                        "Indira Col":["G", (20, 0)], "Rezang La":["H", (30, 10)], "Tanglang La":["I", (40, 20)],
                        "Pensi La":["J", (40, 0)], "Marsimik La":["K", (50, 10)]
                        }
    def arrange(self, k):
        b = ""
        for i in sorted(k):
            b += i
        k, b = b, k
        d = {}
        for i in range(len(k)):
            if k[i] not in d.keys():
                d[k[i]] = [i]
            else:
                d[k[i]].append(i)
        ret = []
        for i in b:
            ret.append(d[i][0])
            d[i].pop(0)
        return ret

    def decode_message(self, x, key):
        ret = ""
        ctr = 0
        step = len(x) // len(key)
        ind = self.arrange(key)
        for i in range(step):
            temp = ""
            for j in range(ctr, (len(key) * step) , step):
                # print(x[j], end="")
                temp = temp + x[j]
            for k in range(len(key)):
                ret = ret + temp[ind[k]]
                # print(temp[ind[k]], end="")

            ctr += 1
        return ret

    def extract_location(self,msg):
        master = list(self.location_dict.keys())
        ret = []
        for i in master:
            if i in msg:
                ret.append(i)
        return ret

    def search(self, loc_list):
        graph = Graph()

        edges = [
        ('A', 'B', 1.14),
        ('A', 'C', 1),
        ('A', 'D', 1.14),
        ('B', 'E', 1),
        ('C', 'E', 1.14),
        ('C', 'F', 1),
        ('D', 'F', 1.14),
        ('D', 'G', 1),
        ('E', 'H', 1.14),
        ('G', 'H', 1.14),
        ('H', 'I', 1.14),
        ('H', 'J', 1.14),
        ('I', 'K', 1.14),
        ('J', 'K', 1.14)
        ]

        for edge in edges:
            graph.add_edge(*edge)

        min, ret = None, None
        total_cost_dict = {}
        for camp in self.location_dict.keys():
            camp_code = self.location_dict[camp][0]
            total_cost = 0
            print("hi", loc_list)
            if camp not in loc_list:
                print(camp)
                for enemy in loc_list:
                    enemy_code = self.location_dict[enemy][0]
                    path, cost = self.dijsktra(graph, camp_code, enemy_code)
                    total_cost += cost

                total_cost_dict[camp] = round(total_cost, 2)


                if min == None or total_cost < min:
                    min = total_cost
                    ret = camp

        return ret, total_cost_dict

    def dijsktra(self, graph, initial, end):
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()

        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]

                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}

            if not next_destinations:
                return "Route not possible."

            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        path = []
        cost = 0

        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path = path[::-1]

        for i in range(len(path)):
            try:
                cost += graph.weights[(path[i], path[i+1])]
            except:
                break

        return path, cost

    def run(self, x, key):
        # x = "Cnwvtus KuaiTaa rlodeeurethn  an Ia_mrhs baer oag ndC_a aeoat dLj lLdio_me  p  hagZLngan _"
        # key = "DELHI"
        ret = []

        #ret.append("encrypted message is:")
        #ret.append(x)
        #ret.append("key:" + " " + key)

        decoded = self.decode_message(x, key).replace("_", "")

        loc_list = self.extract_location(decoded)
        if loc_list == []:
            ret.append("NOT APPLICABLE")
            return None, None, None

        else:
            ret.append("Decoded message: " + decoded)
            print("run", loc_list)
            our_camp, total_cost_dict = self.search(loc_list)
            ret.append("Our base should be at:" + " " + our_camp)

            from grid import generate
            india = [self.location_dict[x][0] for x in [our_camp]]
            print(india)
            china = [self.location_dict[x][0] for x in loc_list]
            gen = generate(india, china)
            gen.generate_image()

            return ret, total_cost_dict, loc_list
