class edge_node:
    def __init__(self,
                 i_vex,
                 j_vex,
                 i_link=None,
                 j_link=None,
                 info=None):
        self.i_vex = i_vex
        self.j_vex = j_vex
        self.i_link = i_link
        self.j_link = j_link
        self.info = info


class vertex_node:
    def __init__(self, data, first_edge):
        self.data = data
        self.first_edge = first_edge
        self.mark = False


class AML_graph:
    def __init__(self, adjmul_list, vex_num: int, edge_num: int):
        self.adjmul_list = adjmul_list
        self.vex_num = vex_num
        self.edge_num = edge_num


def locate_node(graph, node) -> int:
    for i in range(graph.vex_num):
        if node.data == graph.adjmul_list[i].data:
            return i
    return -1


def insert_edge_action(graph, index1: int, index2: int, info):
    edge = edge_node(index1, index2, info=info)

    p = graph.adjmul_list[index1].first_edge
    if not p:
        graph.adjmul_list[index1].first_edge = edge
        edge.i_link = None
    else:
        graph.adjmul_list[index1].first_edge = edge
        edge.i_link = p

    q = graph.adjmul_list[index2].first_edge
    if not q:
        graph.adjmul_list[index2].first_edge = edge
        edge.j_link = None
    else:
        graph.adjmul_list[index2].first_edge = edge
        edge.j_link = q


def insert_edge(graph, node1, node2, info):
    index1 = locate_node(graph, node1)
    index2 = locate_node(graph, node2)
    if index1 < 0 or index2 < 0:
        raise("index error")

    insert_edge_action(graph, index1, index2, info)


def create_aml_graph(vex_num) -> AML_graph:
    adjmul_list = list()
    graph = AML_graph(adjmul_list, vex_num, 0)
    for i in range(vex_num):

        graph.adjmul_list.append(vertex_node(
            input("Input {:d}-th node: ".format(i)), None))

    print("Input edge info:")
    while True:
        print("Are you going to add a edge into AMLGraph?")
        status = input("Please enter y/n: ")
        if status == "y":
            print("Please input two nodes of {:d}-th edge:"
                  .format(graph.edge_num+1))

            data1 = input("First node: ")
            data2 = input("Second node: ")
            node1 = vertex_node(data1, None)
            node2 = vertex_node(data2, None)
            info = int(input("Info: "))
            insert_edge(graph, node1, node2, info)
            graph.edge_num += 1
        else:
            break

    return graph


def print_AML_graph(graph):
    for i in range(graph.vex_num):
        print("{:d} {:s}".format(i, graph.adjmul_list[i].data), end="")
        edge = graph.adjmul_list[i].first_edge

        while edge:
            print("-->|{:d} {:s}|info: {:d}|{:d} {:s}|".format(edge.i_vex,
                                                               graph.adjmul_list[edge.i_vex].data,
                                                               edge.info,
                                                               edge.j_vex,
                                                               graph.adjmul_list[edge.j_vex].data
                                                               ),
                  end="")
            if edge.i_vex == i:
                edge = edge.i_link
            else:
                edge = edge.j_link
        print("-->NULL")
    print()


def first_adj_vex(graph, v: int) -> int:
    if graph.adjmul_list[v].first_edge:
        w = graph.adjmul_list[v].first_edge.j_vex
        if w == v:
            return -1
        return w
    return -1


def next_adj_vex(graph, v: int, w: int):
    p = graph.adjmul_list[v].first_edge
    while p.j_vex != w:
        p = p.i_link
    if p.i_link:
        t = p.i_link.j_vex
        if t == v:
            return -1
        return t
    else:
        return -1


def DFS(graph, v, all_list, level):
    if len(all_list) == level:
        all_list.append(list())
    graph.adjmul_list[v].mark = True
    print(" ->", graph.adjmul_list[v].data)
    all_list[level].append(graph.adjmul_list[v].data)

    w = first_adj_vex(graph, v)
    while True:
        if w < 0:
            break
        w = next_adj_vex(graph, v, w)
        if not graph.adjmul_list[w].mark:
            DFS(graph, w, all_list, level+1)


def DFS_traverse(graph):
    all_list = list()
    sp_data = int(input("Choose start point: "))
    start_index = locate_node(graph, graph.adjmul_list[sp_data])
    print("DFS result:")
    for i in range(graph.vex_num):
        ii = (i + start_index) % graph.vex_num
        graph.adjmul_list[ii].mark = False
    for i in range(graph.vex_num):
        ii = (i + start_index) % graph.vex_num
        if not graph.adjmul_list[ii].mark:
            DFS(graph, ii, all_list, 0)
    print()

    print("Show search tree:")
    print("-> {:s}".format(all_list[0][0]))
    for i in range(len(all_list)):
        if i == 0:
            for j in range(1, len(all_list[i])):
                print("-> {:s} ".format(all_list[i][j]), end="")
        else:
            for j in range(len(all_list[i])):
                print("-> {:s} ".format(all_list[i][j]), end="")
        print()
    print()


def BFS_traverse(graph):
    sp_data = int(input("Choose start point: "))
    start_index = locate_node(graph, graph.adjmul_list[sp_data])

    first = 0
    end = 0
    queue = list()

    for v in range(graph.vex_num):
        i = (v + start_index) % graph.vex_num
        graph.adjmul_list[i].mark = False
    print("BFS result:")
    for v in range(graph.vex_num):
        i = (v + start_index) % graph.vex_num
        if not graph.adjmul_list[i].mark:
            graph.adjmul_list[i].mark = True
            print(" ->", graph.adjmul_list[i].data)
            queue.append(i)
            end += 1
            while end - first != 0:
                u = queue[first]
                first += 1
                w = first_adj_vex(graph, u)
                while True:
                    if w < 0:
                        break
                    w = next_adj_vex(graph, u, w)
                    if not graph.adjmul_list[w].mark:
                        graph.adjmul_list[w].mark = True
                        print(" ->", graph.adjmul_list[w].data)
                        queue.append(w)
                        end += 1


def DFS_non_recursive(graph):
    stack = list()

    sp_data = int(input("Choose start point: "))
    start_index = locate_node(graph, graph.adjmul_list[sp_data])

    for v in range(graph.vex_num):
        i = (v + start_index) % graph.vex_num
        graph.adjmul_list[i].mark = False

    print("DFS non recursive results:")
    for v in range(graph.vex_num):
        i = (v + start_index) % graph.vex_num
        stack.append(i)
        while len(stack) != 0:
            u = stack.pop()
            if not graph.adjmul_list[u].mark:
                print(" ->", graph.adjmul_list[u].data)
                graph.adjmul_list[u].mark = True
            edge = graph.adjmul_list[u].first_edge
            while edge:
                if edge.i_vex == u:
                    if not graph.adjmul_list[edge.j_vex].mark:
                        stack.append(edge.j_vex)
                        edge = edge.i_link
                    else:
                        break
                else:
                    if not graph.adjmul_list[edge.i_vex].mark:
                        stack.append(edge.i_vex)
                        edge = edge.j_link
                    else:
                        break


if __name__ == "__main__":
    vex_num = int(input("Please input node num: "))
    graph = create_aml_graph(vex_num)
    print_AML_graph(graph)

    DFS_traverse(graph)

    BFS_traverse(graph)
    print()

    DFS_non_recursive(graph)
    print()
