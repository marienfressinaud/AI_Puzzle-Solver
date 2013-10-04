# -*- coding: utf-8 -*-

from pygraphviz import AGraph


def get_color(num_color):
    colors = ["#3498db", "#f1c40f", "#c0392b", "#27ae60"]

    if 0 < num_color <= len(colors):
        return colors[num_color - 1]
    else:
        return "#ffffff"


def draw_graph(state_manager, filename):
    graph = AGraph()
    graph.node_attr["style"] = "filled"
    graph.node_attr["shape"] = "circle"
    graph.node_attr["fixedsize"] = "true"
    graph.node_attr["width"] = 0.5
    graph.node_attr["height"] = 0.5

    # we add all nodes (keys = ID)
    graph.add_nodes_from(state_manager.state.keys())
    for var_id in state_manager.state:
        # and for each of these nodes, we change color
        node = graph.get_node(var_id)
        node.attr["fillcolor"] = get_color(state_manager.state[var_id])

    # finally, we add edges
    for c in state_manager.constraints:
        e = c.list_vars
        graph.add_edge(e[0], e[1])

    graph.write(filename)
