# -*- coding: utf-8 -*-

from pygraphviz import *

def get_color(num_color):
    if num_color == 1:
        return "#3498db"
    if num_color == 2:
        return "#f1c40f"
    if num_color == 3:
        return "#c0392b"
    if num_color == 4:
        return "#27ae60"

    return "#ffffff"

def draw_graph(state_manager, filename):
    graph = AGraph()
    graph.node_attr['style']='filled'
    graph.node_attr['shape']='circle'
    graph.node_attr['fixedsize']='true'
    graph.node_attr['width']='0.5'
    graph.node_attr['height']='0.5'

    # we add all nodes (keys = ID)
    graph.add_nodes_from(state_manager.vars.keys())
    for n in state_manager.vars:
        # and for each of these nodes, we change color
        node = graph.get_node(n)
        node.attr['fillcolor'] = get_color(state_manager.vars[n])

    # finally, we add edges
    for e in state_manager.constraints:
        graph.add_edge(e[0], e[1])

    graph.write("data/%s" % filename)
