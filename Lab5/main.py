"""
Main script to generate visualizations and performance comparisons
for MST algorithms with enhanced aesthetics
"""

import os
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import PillowWriter
import networkx as nx
import numpy as np

# Import algorithms from impl.py
from impl import kruskal_mst, prim_mst, generate_random_graph

# Set up beautiful plotting style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'kruskal': '#FF6B6B',
    'prim': '#4ECDC4',
    'mst_edge': '#FF6B6B',
    'frontier': '#FFA07A',
    'node': '#87CEEB',
    'node_in_tree': '#90EE90',
    'background': '#F8F9FA'
}


def visualize_algorithm_steps_enhanced(G, pos, steps, algorithm_name, output_path):
    """
    Create an enhanced step-by-step animation of algorithm execution
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle(f'{algorithm_name} Algorithm - Execution Sequence', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Select 4 key steps for display
    step_indices = [
        0, 
        len(steps) // 3, 
        2 * len(steps) // 3, 
        len(steps) - 1
    ]
    
    edge_labels = {(u, v): f"{G[u][v]['weight']:.1f}" 
                   for u, v in G.edges()}
    
    for idx, step_idx in enumerate(step_indices):
        ax = axes[idx // 2, idx % 2]
        ax.set_title(f'Step {step_idx + 1}/{len(steps)}', 
                    fontweight='bold', fontsize=11)
        
        # Draw all edges of the original graph (faded)
        nx.draw_networkx_edges(G, pos, alpha=0.15, ax=ax, width=0.5, 
                              edge_color='gray')
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=300, 
                              node_color=colors['node'], ax=ax, 
                              edgecolors='navy', linewidths=1.5)
        
        # Draw node labels
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=9, 
                               font_color='black', ax=ax, font_weight='bold')
        
        # Draw MST edges built so far
        mst_edges_so_far = [(u, v) for u, v, _ in steps[step_idx][0]]
        if mst_edges_so_far:
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges_so_far, 
                                  width=2.5, edge_color=colors['mst_edge'], 
                                  ax=ax, alpha=0.8)
        
        # Highlight the edge just added in this step (if not the first step)
        if step_idx > 0:
            latest_edge = steps[step_idx][1]
            if latest_edge:
                nx.draw_networkx_edges(G, pos, edgelist=[latest_edge], 
                                     width=3.5, edge_color='#FF0000', ax=ax, 
                                     style='dashed', alpha=0.9)
        
        # Add edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                    font_size=7, ax=ax)
        
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    print(f"✓ Saved {algorithm_name} snapshot to {output_path}")
    plt.close()


def create_animated_visualization(G, pos, steps, algorithm_name, output_path):
    """
    Create an animated visualization showing the full algorithm progression
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(colors['background'])
    
    edge_labels = {(u, v): f"{G[u][v]['weight']:.1f}" for u, v in G.edges()}
    
    def update(frame_idx):
        ax.clear()
        ax.set_title(f'{algorithm_name} - Step {frame_idx + 1}/{len(steps)}',
                    fontsize=14, fontweight='bold', pad=10)
        
        # Draw all edges of the original graph (faded)
        nx.draw_networkx_edges(G, pos, alpha=0.12, ax=ax, width=0.8,
                              edge_color='gray')
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=400, 
                              node_color=colors['node'], ax=ax,
                              edgecolors='navy', linewidths=2)
        
        # Draw node labels
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=10,
                               font_color='black', ax=ax, font_weight='bold')
        
        # Draw MST edges built so far
        mst_edges_so_far = [(u, v) for u, v, _ in steps[frame_idx][0]]
        if mst_edges_so_far:
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges_so_far,
                                  width=2.5, edge_color=colors['mst_edge'],
                                  ax=ax, alpha=0.85)
        
        # Highlight the edge just added in this step
        latest_edge = steps[frame_idx][1]
        if latest_edge:
            nx.draw_networkx_edges(G, pos, edgelist=[latest_edge],
                                  width=3.5, edge_color='#FF0000', ax=ax,
                                  style='dashed', alpha=0.95)
        
        # Add edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                    font_size=8, ax=ax)
        
        ax.axis('off')
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=len(steps), interval=800, 
                        repeat=True, repeat_delay=1000)
    
    # Save as GIF
    writer = PillowWriter(fps=1.25)
    anim.save(output_path, writer=writer)
    print(f"✓ Saved {algorithm_name} animation to {output_path}")
    plt.close()


def plot_performance_comparison(node_sizes, kruskal_times, prim_times, 
                               density_name, output_path):
    """
    Create enhanced performance comparison plots with better visibility
    """
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor('white')
    
    # Convert to milliseconds
    kruskal_ms = np.array(kruskal_times) * 1000
    prim_ms = np.array(prim_times) * 1000
    
    line_width = 3
    marker_size = 10
    
    ax.plot(node_sizes, kruskal_ms, 'o-', 
           label="Kruskal's Algorithm", color=colors['kruskal'], 
           linewidth=line_width, markersize=marker_size, markeredgewidth=2,
           markeredgecolor='darkred', markerfacecolor=colors['kruskal'], alpha=0.85)
    
    ax.plot(node_sizes, prim_ms, 's-', 
           label="Prim's Algorithm", color=colors['prim'], 
           linewidth=line_width, markersize=marker_size, markeredgewidth=2,
           markeredgecolor='darkblue', markerfacecolor=colors['prim'], alpha=0.85)
    
    # Add value labels on points
    for i, size in enumerate(node_sizes):
        ax.text(size, kruskal_ms[i], f'{kruskal_ms[i]:.1f}', 
               ha='center', va='bottom', fontsize=9, fontweight='bold', color=colors['kruskal'])
        ax.text(size, prim_ms[i], f'{prim_ms[i]:.1f}', 
               ha='center', va='top', fontsize=9, fontweight='bold', color=colors['prim'])
    
    ax.set_xlabel('Number of Nodes', fontsize=13, fontweight='bold')
    ax.set_ylabel('Execution Time (milliseconds)', fontsize=13, fontweight='bold')
    ax.set_title(f'MST Algorithm Performance Comparison - {density_name} Graphs',
                fontsize=15, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.7, color='gray')
    ax.set_axisbelow(True)
    ax.legend(fontsize=12, loc='upper left', framealpha=0.98, title='Algorithm', title_fontsize=12)
    
    # Use linear scale for better visibility
    ax.set_xscale('linear')
    ax.set_yscale('linear')
    
    # Improve tick labels
    ax.tick_params(axis='both', labelsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    print(f"✓ Saved performance comparison to {output_path}")
    plt.close()


def plot_algorithm_comparison(node_sizes, algorithm_times, algorithm_name, 
                             output_path):
    """
    Plot performance of a single algorithm across densities with better visibility
    """
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor('white')
    
    line_width = 3
    marker_size = 10
    
    sparse_ms = np.array(algorithm_times['sparse']) * 1000
    dense_ms = np.array(algorithm_times['dense']) * 1000
    
    color = colors['kruskal'] if 'kruskal' in algorithm_name.lower() else colors['prim']
    
    ax.plot(node_sizes, sparse_ms, 'o-',
           label="Sparse Graph (p=0.3)", color=color,
           linewidth=line_width, markersize=marker_size, markeredgewidth=2,
           markeredgecolor='darkred' if 'kruskal' in algorithm_name.lower() else 'darkblue',
           alpha=0.85)
    
    ax.plot(node_sizes, dense_ms, 's-',
           label="Dense Graph (p=0.7)", color='#FF8C00',
           linewidth=line_width, markersize=marker_size, markeredgewidth=2,
           markeredgecolor='#B85C00', alpha=0.85)
    
    # Add value labels on points
    for i, size in enumerate(node_sizes):
        ax.text(size, sparse_ms[i], f'{sparse_ms[i]:.1f}', 
               ha='center', va='bottom', fontsize=9, fontweight='bold', color=color)
        ax.text(size, dense_ms[i], f'{dense_ms[i]:.1f}', 
               ha='center', va='top', fontsize=9, fontweight='bold', color='#FF8C00')
    
    ax.set_xlabel('Number of Nodes', fontsize=13, fontweight='bold')
    ax.set_ylabel('Execution Time (milliseconds)', fontsize=13, fontweight='bold')
    ax.set_title(f"{algorithm_name} - Performance on Different Graph Densities",
                fontsize=15, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.7, color='gray')
    ax.set_axisbelow(True)
    ax.legend(fontsize=12, loc='upper left', framealpha=0.98, title='Graph Type', title_fontsize=12)
    
    ax.set_xscale('linear')
    ax.set_yscale('linear')
    
    ax.tick_params(axis='both', labelsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    print(f"✓ Saved {algorithm_name} performance to {output_path}")
    plt.close()


def plot_overall_comparison(node_sizes, results, output_path):
    """
    Create comprehensive overall performance comparison with better visibility
    """
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor('white')
    
    line_width = 3
    marker_size = 10
    
    # Convert to milliseconds
    kruskal_sparse_ms = np.array(results['kruskal_sparse']) * 1000
    kruskal_dense_ms = np.array(results['kruskal_dense']) * 1000
    prim_sparse_ms = np.array(results['prim_sparse']) * 1000
    prim_dense_ms = np.array(results['prim_dense']) * 1000
    
    # Plot all four combinations with distinct visibility
    ax.plot(node_sizes, kruskal_sparse_ms, 'o-',
           label="Kruskal (Sparse p=0.3)", color=colors['kruskal'],
           linewidth=line_width, markersize=marker_size, markeredgewidth=2.5,
           markeredgecolor='darkred', alpha=0.9)
    
    ax.plot(node_sizes, kruskal_dense_ms, 'o--',
           label="Kruskal (Dense p=0.7)", color=colors['kruskal'],
           linewidth=line_width, markersize=marker_size, markeredgewidth=2.5,
           markeredgecolor='darkred', alpha=0.55, linestyle='--')
    
    ax.plot(node_sizes, prim_sparse_ms, 's-',
           label="Prim (Sparse p=0.3)", color=colors['prim'],
           linewidth=line_width, markersize=marker_size, markeredgewidth=2.5,
           markeredgecolor='darkblue', alpha=0.9)
    
    ax.plot(node_sizes, prim_dense_ms, 's--',
           label="Prim (Dense p=0.7)", color=colors['prim'],
           linewidth=line_width, markersize=marker_size, markeredgewidth=2.5,
           markeredgecolor='darkblue', alpha=0.55, linestyle='--')
    
    ax.set_xlabel('Number of Nodes', fontsize=13, fontweight='bold')
    ax.set_ylabel('Execution Time (milliseconds)', fontsize=13, fontweight='bold')
    ax.set_title('Comprehensive MST Algorithm Performance Comparison',
                fontsize=15, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.7, color='gray')
    ax.set_axisbelow(True)
    ax.legend(fontsize=11, loc='upper left', framealpha=0.98, title='Algorithm & Density', 
             title_fontsize=12, ncol=1)
    
    ax.set_xscale('linear')
    ax.set_yscale('linear')
    
    ax.tick_params(axis='both', labelsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    print(f"✓ Saved overall performance comparison to {output_path}")
    plt.close()


# Import FuncAnimation for animations
from matplotlib.animation import FuncAnimation


def run_benchmarks():
    """
    Run comprehensive benchmarks and generate all visualizations
    """
    output_dir = 'graph_visualizations'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("MST ALGORITHM VISUALIZATION AND BENCHMARKING")
    print("="*60 + "\n")
    
    # Generate a sample graph for visualization
    print("→ Generating sample graph for visualization (22 nodes)...")
    n_sample = 22
    G_sample, pos_sample = generate_random_graph(n_sample, density=0.3)
    
    print(f"  Generated graph with {G_sample.number_of_nodes()} nodes and "
          f"{G_sample.number_of_edges()} edges\n")
    
    # Run algorithms on sample graph
    print("→ Running Kruskal's algorithm on sample graph...")
    kruskal_result, kruskal_weight, kruskal_steps = kruskal_mst(G_sample)
    print(f"  MST weight: {kruskal_weight:.2f}")
    
    print("→ Running Prim's algorithm on sample graph...")
    prim_result, prim_weight, prim_steps = prim_mst(G_sample)
    print(f"  MST weight: {prim_weight:.2f}\n")
    
    # Generate visualizations for sample graph
    print("→ Generating visualizations for sample graph...")
    visualize_algorithm_steps_enhanced(G_sample, pos_sample, kruskal_steps,
                                       "Kruskal's", 
                                       f'{output_dir}/kruskal_snapshot.png')
    
    visualize_algorithm_steps_enhanced(G_sample, pos_sample, prim_steps,
                                       "Prim's",
                                       f'{output_dir}/prim_snapshot.png')
    
    print("→ Generating animated visualizations...")
    create_animated_visualization(G_sample, pos_sample, kruskal_steps,
                                 "Kruskal's",
                                 f'{output_dir}/kruskal_animation.gif')
    
    create_animated_visualization(G_sample, pos_sample, prim_steps,
                                 "Prim's",
                                 f'{output_dir}/prim_animation.gif')
    
    # Performance benchmarking
    print("\n→ Running performance benchmarks...\n")
    
    node_sizes = [10, 20, 50, 100, 200, 500, 700, 1000]
    results = {
        'kruskal_sparse': [],
        'kruskal_dense': [],
        'prim_sparse': [],
        'prim_dense': []
    }
    
    for n in node_sizes:
        print(f"  Testing with {n} nodes...")
        
        # Test sparse graphs
        k_time_sparse = 0
        p_time_sparse = 0
        for _ in range(3):
            G_sparse, _ = generate_random_graph(n, density=0.3)
            
            start = time.time()
            kruskal_mst(G_sparse)
            k_time_sparse += time.time() - start
            
            start = time.time()
            prim_mst(G_sparse)
            p_time_sparse += time.time() - start
        
        # Test dense graphs
        k_time_dense = 0
        p_time_dense = 0
        for _ in range(3):
            G_dense, _ = generate_random_graph(n, density=0.7)
            
            start = time.time()
            kruskal_mst(G_dense)
            k_time_dense += time.time() - start
            
            start = time.time()
            prim_mst(G_dense)
            p_time_dense += time.time() - start
        
        results['kruskal_sparse'].append(k_time_sparse / 3)
        results['kruskal_dense'].append(k_time_dense / 3)
        results['prim_sparse'].append(p_time_sparse / 3)
        results['prim_dense'].append(p_time_dense / 3)
        
        print(f"    Kruskal: {results['kruskal_sparse'][-1]*1000:.3f}ms (sparse), "
              f"{results['kruskal_dense'][-1]*1000:.3f}ms (dense)")
        print(f"    Prim:    {results['prim_sparse'][-1]*1000:.3f}ms (sparse), "
              f"{results['prim_dense'][-1]*1000:.3f}ms (dense)\n")
    
    # Generate performance plots
    print("→ Generating performance comparison plots...\n")
    
    plot_performance_comparison(node_sizes, results['kruskal_sparse'],
                               results['kruskal_dense'], "Sparse (p=0.3)",
                               f'{output_dir}/kruskal_performance.png')
    
    plot_performance_comparison(node_sizes, results['prim_sparse'],
                               results['prim_dense'], "Dense (p=0.7)",
                               f'{output_dir}/prim_performance.png')
    
    plot_algorithm_comparison(node_sizes,
                             {'sparse': results['kruskal_sparse'],
                              'dense': results['kruskal_dense']},
                             "Kruskal's Algorithm",
                             f'{output_dir}/kruskal_sparse_dense.png')
    
    plot_algorithm_comparison(node_sizes,
                             {'sparse': results['prim_sparse'],
                              'dense': results['prim_dense']},
                             "Prim's Algorithm",
                             f'{output_dir}/prim_sparse_dense.png')
    
    plot_performance_comparison(node_sizes, results['kruskal_sparse'],
                               results['prim_sparse'], "Sparse (p=0.3)",
                               f'{output_dir}/comparison_sparse.png')
    
    plot_performance_comparison(node_sizes, results['kruskal_dense'],
                               results['prim_dense'], "Dense (p=0.7)",
                               f'{output_dir}/comparison_dense.png')
    
    plot_overall_comparison(node_sizes, results,
                           f'{output_dir}/overall_comparison.png')
    
    print("="*60)
    print("✓ All visualizations and benchmarks completed successfully!")
    print(f"✓ Output saved to: {os.path.abspath(output_dir)}")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_benchmarks()
