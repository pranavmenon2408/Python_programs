class Graph:
    def __init__(self):
        self.graph_dict = {}
        self.heuristic = {}
    def add_edge(self,source,dest,weight):
        if source not in self.graph_dict:
            self.graph_dict[source] = {}
        self.graph_dict[source][dest] = weight
        if dest not in self.graph_dict:
            self.graph_dict[dest] = {}
        self.graph_dict[dest][source] = weight
    def add_heuristic(self,source,heuristic):
        self.heuristic[source] = heuristic
    def a_star(self,start,goal):
        open_list = [(0,[start])]
        visited = [start]
        while open_list:
            open_list.sort()
            path = open_list.pop(0)
            current = path[1][-1]
            print(open_list)
            if current in goal:
                return path
            for neighbor in self.graph_dict[current]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    new_path = list(path[1])
                    new_path.append(neighbor)
                    g = path[0] + self.graph_dict[current][neighbor]
                    h = self.heuristic[neighbor]
                    f = g + h
                    open_list.append((f,new_path))
if __name__=="__main__":
    graph = Graph()
    choice=1
    while choice:
        source = input("Enter source: ")
        dest = input("Enter destination: ")
        weight = int(input("Enter weight: "))
        graph.add_edge(source,dest,weight)
        choice = int(input("Do you want to add more edges? (0/1): "))
    for i in graph.graph_dict:
        heuristic = int(input(f"Enter heuristic for {i}: "))
        graph.add_heuristic(i,heuristic)

    start = input("Enter start node: ")
    goal = input("Enter goal nodes: ").split()
    for i in goal:
        graph.add_heuristic(i,0)
    path=graph.a_star(start,goal)
    print(f"Possible path: {path[1]} with cost {path[0]}")
