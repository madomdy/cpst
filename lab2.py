# https://en.wikipedia.org/wiki/Capacitated_minimum_spanning_tree

import re

BIG = 1000000000

def get_new_pair(graph, not_viewed, root, capacity_load, capacity):
    global_from = -1
    global_to = -1
    max_tradeoff = 0
    for v in not_viewed:
        v_closest_dest = BIG
        v_closest_ind = -1
        for neigh in range(len(graph[v])):
            # if v == 5 and neigh in (6, 7):
            #     import pdb; pdb.set_trace()
            if graph[v][neigh] == -1 or neigh == root:
                continue
            # if neigh == 7:
            #     import pdb; pdb.set_trace()
            if graph[v][neigh] <= v_closest_dest:
                if capacity_load[v] + capacity_load[neigh] <= capacity:
                    v_closest_dest = graph[v][neigh]
                    v_closest_ind = neigh
        if v_closest_ind != -1:
            cur_tradeoff = graph[v][root] - graph[v][v_closest_ind]
            if cur_tradeoff > max_tradeoff:
                global_from = v
                global_to = v_closest_ind
                max_tradeoff = cur_tradeoff
    return global_from, global_to, max_tradeoff

def get_cmst(graph, root, capacities, capacity):
    tree = set((root, i) for i in range(len(graph)) if i != root)
    not_viewed = set(i for i in range(len(graph)))
    cost = sum(graph[t[0]][t[1]] for t in tree)
    capacity_load = capacities[:]
    capacity -= capacity_load[root]
    for i in range(100):
        v_from, v_to, tradeoff = get_new_pair(graph, not_viewed, 
                        root, capacity_load, capacity)
        if -1 in (v_from, v_to):
            break
        not_viewed.remove(v_from)
        capacity_load[v_to] += capacity_load[v_from]
        graph[v_from][v_to] = -1
        graph[v_to][v_from] = -1
        tree.remove((root, v_from))
        tree.add((v_from, v_to))
        cost -= tradeoff
    return tree, cost

def read_data(path):
    with open(path) as inp:
        s = inp.readline()
        s = re.findall("[V,E,R,C]{1}:[\d]+", s)
        d = dict((x[0], int(x[2:])) for x in s)
        count_V = d['V']
        count_E = d['E']
        root = d['R']
        capacity = d['C']
        capacities = [(int(x)) for x in inp.readline().split()]
        graph = [[-1 for _ in range(count_V)] for _ in range(count_V)]
        for row in inp:
            l, r, weight = (int(x) for x in row.split())
            graph[l][r] = weight
            graph[r][l] = weight
        return graph, root, capacities, capacity

if __name__ == "__main__":
    path = "input.txt"
    graph, root, capacities, capacity = read_data(path)
    tree, cost = get_cmst(graph, root, capacities, capacity)
    print(tree, cost)