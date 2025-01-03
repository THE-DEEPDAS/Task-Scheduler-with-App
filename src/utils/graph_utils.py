import networkx as nx
import matplotlib.pyplot as plt

def create_dependency_graph(tasks_df):
    graph = nx.DiGraph()
    for _, row in tasks_df.iterrows():
        if row['dependencies'] != 'None':
            dependencies = [dep.strip() for dep in row['dependencies'].split(',')]
            for dep in dependencies:
                graph.add_edge(dep, row['task_name'])
    return graph

def visualize_graph(graph):
    if not graph.nodes():
        print("No dependencies to visualize.")
        return
        
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, 
            node_color='lightblue', 
            node_size=3000, 
            font_size=10, 
            font_weight='bold', 
            arrows=True)
    plt.title("Task Dependencies")
    plt.show()
