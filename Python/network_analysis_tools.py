import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class KeyConnectorAnalyzer:
    """
    A class to identify and analyze key connectors in a network
    """
    
    def __init__(self, graph=None):
        """
        Initialize with an optional graph
        
        Parameters:
        -----------
        graph : networkx.Graph, optional
            An existing NetworkX graph
        """
        self.graph = graph if graph else nx.Graph()
        self.centrality_scores = {}
    
    def create_sample_network(self, n_nodes=30, edge_prob=0.15):
        """
        Create a sample random network for demonstration
        
        Parameters:
        -----------
        n_nodes : int
            Number of nodes in the network
        edge_prob : float
            Probability of edge creation between nodes
        """
        self.graph = nx.erdos_renyi_graph(n_nodes, edge_prob)
        print(f"Created network with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
    
    def load_from_edgelist(self, edges):
        """
        Load network from edge list
        
        Parameters:
        -----------
        edges : list of tuples
            List of (source, target) or (source, target, weight) tuples
        """
        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)
    
    def calculate_all_centralities(self):
        """
        Calculate multiple centrality measures for all nodes
        
        Returns:
        --------
        pd.DataFrame : DataFrame with all centrality scores
        """
        print("Calculating centrality measures...")
        
        # Degree Centrality
        self.centrality_scores['degree'] = nx.degree_centrality(self.graph)
        
        # Betweenness Centrality
        self.centrality_scores['betweenness'] = nx.betweenness_centrality(self.graph)
        
        # Closeness Centrality
        self.centrality_scores['closeness'] = nx.closeness_centrality(self.graph)
        
        # Eigenvector Centrality
        try:
            self.centrality_scores['eigenvector'] = nx.eigenvector_centrality(self.graph, max_iter=1000)
        except:
            print("Warning: Eigenvector centrality calculation failed")
            self.centrality_scores['eigenvector'] = {node: 0 for node in self.graph.nodes()}
        
        # PageRank
        self.centrality_scores['pagerank'] = nx.pagerank(self.graph)
        
        # Create DataFrame
        df = pd.DataFrame(self.centrality_scores)
        df['node'] = df.index
        df = df[['node'] + [col for col in df.columns if col != 'node']]
        
        return df
    
    def get_top_connectors(self, n=10, method='betweenness'):
        """
        Get top N key connectors based on specified centrality measure
        
        Parameters:
        -----------
        n : int
            Number of top connectors to return
        method : str
            Centrality measure to use ('degree', 'betweenness', 'closeness', 
            'eigenvector', 'pagerank')
        
        Returns:
        --------
        list : List of (node, score) tuples
        """
        if method not in self.centrality_scores:
            raise ValueError(f"Method {method} not calculated. Run calculate_all_centralities() first.")
        
        sorted_nodes = sorted(self.centrality_scores[method].items(), 
                            key=lambda x: x[1], reverse=True)
        return sorted_nodes[:n]
    
    def identify_bridges(self):
        """
        Identify bridge edges (edges whose removal disconnects the graph)
        
        Returns:
        --------
        list : List of bridge edges
        """
        bridges = list(nx.bridges(self.graph))
        print(f"Found {len(bridges)} bridge edges")
        return bridges
    
    def find_communities(self):
        """
        Detect communities in the network using Louvain method
        
        Returns:
        --------
        dict : Dictionary mapping nodes to community IDs
        """
        communities = nx.community.louvain_communities(self.graph)
        node_to_community = {}
        for idx, community in enumerate(communities):
            for node in community:
                node_to_community[node] = idx
        
        print(f"Found {len(communities)} communities")
        return node_to_community
    
    def visualize_network(self, highlight_top_n=5, method='betweenness', 
                         figsize=(12, 8), save_path=None):
        """
        Visualize the network with key connectors highlighted
        
        Parameters:
        -----------
        highlight_top_n : int
            Number of top connectors to highlight
        method : str
            Centrality measure for highlighting
        figsize : tuple
            Figure size
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=figsize)
        
        # Get layout
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
        
        # Get top connectors
        top_connectors = self.get_top_connectors(highlight_top_n, method)
        top_nodes = [node for node, score in top_connectors]
        
        # Node colors
        node_colors = ['red' if node in top_nodes else 'lightblue' 
                      for node in self.graph.nodes()]
        
        # Node sizes based on centrality
        if method in self.centrality_scores:
            node_sizes = [3000 * self.centrality_scores[method].get(node, 0) + 100 
                         for node in self.graph.nodes()]
        else:
            node_sizes = [300 for _ in self.graph.nodes()]
        
        # Draw network
        nx.draw_networkx_edges(self.graph, pos, alpha=0.2, width=1)
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8)
        nx.draw_networkx_labels(self.graph, pos, 
                               labels={n: n for n in top_nodes},
                               font_size=10, font_weight='bold')
        
        plt.title(f'Network with Top {highlight_top_n} Key Connectors ({method.capitalize()} Centrality)', 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def get_network_stats(self):
        """
        Get basic network statistics
        
        Returns:
        --------
        dict : Dictionary of network statistics
        """
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'avg_clustering': nx.average_clustering(self.graph),
            'is_connected': nx.is_connected(self.graph),
        }
        
        if nx.is_connected(self.graph):
            stats['diameter'] = nx.diameter(self.graph)
            stats['avg_shortest_path'] = nx.average_shortest_path_length(self.graph)
        else:
            stats['num_components'] = nx.number_connected_components(self.graph)
        
        return stats


# Example usage with detailed output
if __name__ == "__main__":
    print("="*60)
    print("KEY CONNECTORS NETWORK ANALYSIS")
    print("="*60)
    
    # Create analyzer
    analyzer = KeyConnectorAnalyzer()
    
    # Option 1: Create sample network
    print("\n[1] Creating Sample Network...")
    analyzer.create_sample_network(n_nodes=30, edge_prob=0.15)
    
    # Option 2: Load from edge list (uncomment to use)
    # edges = [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    # analyzer.load_from_edgelist(edges)
    
    # Get network statistics
    print("\n[2] Network Statistics:")
    print("-"*60)
    stats = analyzer.get_network_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    # Calculate all centrality measures
    print("\n[3] Calculating Centrality Measures...")
    print("-"*60)
    centrality_df = analyzer.calculate_all_centralities()
    print("\nTop 10 Nodes - All Centrality Scores:")
    print(centrality_df.sort_values('betweenness', ascending=False).head(10).to_string(index=False))
    
    # Get top connectors by different methods
    print("\n[4] Top 5 Key Connectors by Different Metrics:")
    print("-"*60)
    
    print("\n  📊 BETWEENNESS CENTRALITY (Information Flow Control)")
    top_betweenness = analyzer.get_top_connectors(5, 'betweenness')
    for i, (node, score) in enumerate(top_betweenness, 1):
        print(f"    {i}. Node {node}: {score:.4f}")
    
    print("\n  📊 DEGREE CENTRALITY (Most Connected)")
    top_degree = analyzer.get_top_connectors(5, 'degree')
    for i, (node, score) in enumerate(top_degree, 1):
        print(f"    {i}. Node {node}: {score:.4f}")
    
    print("\n  📊 PAGERANK (Influence Score)")
    top_pagerank = analyzer.get_top_connectors(5, 'pagerank')
    for i, (node, score) in enumerate(top_pagerank, 1):
        print(f"    {i}. Node {node}: {score:.4f}")
    
    print("\n  📊 CLOSENESS CENTRALITY (Quick Access)")
    top_closeness = analyzer.get_top_connectors(5, 'closeness')
    for i, (node, score) in enumerate(top_closeness, 1):
        print(f"    {i}. Node {node}: {score:.4f}")
    
    # Identify bridges
    print("\n[5] Bridge Analysis (Critical Connections):")
    print("-"*60)
    bridges = analyzer.identify_bridges()
    if bridges:
        print(f"  Found {len(bridges)} bridge edges")
        print(f"  Sample bridges: {bridges[:5]}")
    else:
        print("  No bridge edges found (robust network)")
    
    # Find communities
    print("\n[6] Community Detection:")
    print("-"*60)
    communities = analyzer.find_communities()
    community_sizes = {}
    for node, comm in communities.items():
        community_sizes[comm] = community_sizes.get(comm, 0) + 1
    
    print(f"  Total communities: {len(community_sizes)}")
    for comm_id, size in sorted(community_sizes.items()):
        print(f"    Community {comm_id}: {size} nodes")
    
    # Summary insights
    print("\n[7] Key Insights:")
    print("-"*60)
    top_connector = top_betweenness[0]
    print(f"  🔑 Primary Key Connector: Node {top_connector[0]}")
    print(f"     Controls {top_connector[1]:.2%} of shortest paths")
    print(f"\n  🌐 Network Structure: ", end="")
    if stats['is_connected']:
        print("Fully connected")
    else:
        print(f"{stats.get('num_components', 'Multiple')} separate components")
    print(f"  📈 Network Density: {stats['density']:.2%}")
    print(f"  🔗 Clustering Coefficient: {stats['avg_clustering']:.4f}")
    
    print("\n" + "="*60)
    print("Analysis Complete! Generating visualization...")
    print("="*60 + "\n")
    
    # Visualize
    analyzer.visualize_network(highlight_top_n=5, method='betweenness')
