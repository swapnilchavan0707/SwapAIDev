import networkx as nx
import matplotlib.pyplot as plt


def build_link_graph(email_data):
    """Creates a directed graph from Sender -> Email -> Final Links."""
    G = nx.DiGraph()

    sender = email_data['sender']
    email_node = "Phishing Email"

    G.add_node(sender, type='sender')
    G.add_node(email_node, type='email')
    G.add_edge(sender, email_node)

    # Add link nodes
    for link in email_data['links']:
        dest_node = link['domain']
        G.add_node(dest_node, type='malicious' if 'xyz' in dest_node else 'unknown')
        G.add_edge(email_node, dest_node)

    return G


def plot_link_map(G):
    """Plots the NetworkX graph with Times New Roman labels."""
    plt.style.use('dark_background')
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]

    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color coding
    colors = []
    for node, data in G.nodes(data=True):
        if data.get('type') == 'sender':
            colors.append('#ff4b4b')  # Red
        elif data.get('type') == 'email':
            colors.append('#f0f2f6')  # Gray
        else:
            colors.append('#ffbd45')  # Yellow/Orange

    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=2000, font_size=10, font_family="Times New Roman",
            edge_color='gray', arrows=True, ax=ax)

    plt.title("Malicious Link Path Analysis", fontsize=15)
    return fig
