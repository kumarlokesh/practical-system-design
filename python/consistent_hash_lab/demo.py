"""
CLI demo for consistent hash ring.

Provides command-line interface for adding/removing nodes, distributing keys, 
and showing key-to-node mappings.
"""
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from collections import Counter
import random
import string

try:
    from .node import Node
    from .ring import ConsistentHashRing
except ImportError:
    from node import Node
    from ring import ConsistentHashRing

app = typer.Typer(help="Consistent Hash Lab - Interactive demonstration of consistent hashing")
console = Console()


def generate_test_keys(count: int, prefix: str = "key") -> List[str]:
    """Generate test keys for demonstration."""
    if count <= 1000:
        # For smaller counts, use simple numbered keys
        return [f"{prefix}_{i:04d}" for i in range(count)]
    else:
        # For larger counts, use random strings for better distribution
        keys = []
        for i in range(count):
            if i % 100 == 0:  # Mix of patterns and random
                keys.append(f"{prefix}_{i:06d}")
            else:
                random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                keys.append(f"{prefix}_{random_suffix}")
        return keys


@app.command()
def demo(
    nodes: int = typer.Option(4, "--nodes", "-n", help="Number of nodes to create"),
    keys: int = typer.Option(10000, "--keys", "-k", help="Number of keys to distribute"),
    hash_func: str = typer.Option("sha256", "--hash", help="Hash function (sha256, fnv1a)"),
    virtual_nodes: int = typer.Option(1, "--virtual-nodes", "-v", help="Number of virtual nodes per physical node"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode for adding/removing nodes"),
    show_distribution: bool = typer.Option(True, "--show-dist", help="Show key distribution table"),
    show_ring: bool = typer.Option(False, "--show-ring", help="Show ring state"),
):
    """
    Run a demonstration of consistent hashing.
    
    Creates nodes, distributes keys, and shows the mapping results.
    Optionally allows interactive manipulation of nodes.
    """
    console.print(Panel.fit(
        "[bold blue]🧩 Consistent Hash Lab Demo[/bold blue]\n"
        f"Nodes: {nodes} | Keys: {keys} | Hash: {hash_func} | Virtual nodes: {virtual_nodes}",
        title="Configuration"
    ))
    
    # Create the hash ring
    ring = ConsistentHashRing(hash_function=hash_func)
    
    # Add initial nodes
    console.print("\n[bold green]Creating nodes...[/bold green]")
    for i in range(nodes):
        node = Node(f"node-{i:02d}", replicas=virtual_nodes)
        ring.add_node(node)
        console.print(f"  ✓ Added {node}")
    
    # Generate test keys
    console.print(f"\n[bold green]Generating {keys:,} test keys...[/bold green]")
    test_keys = generate_test_keys(keys)
    
    # Show initial distribution
    distribution = ring.get_key_distribution(test_keys)
    show_key_distribution(distribution, "Initial Distribution")
    
    if show_ring:
        show_ring_state(ring)
    
    if interactive:
        interactive_mode(ring, test_keys)


def show_key_distribution(distribution: dict, title: str = "Key Distribution"):
    """Display key distribution across nodes in a formatted table."""
    table = Table(title=title, show_header=True)
    table.add_column("Node ID", style="cyan", width=15)
    table.add_column("Keys", justify="right", style="green")
    table.add_column("Percentage", justify="right", style="yellow")
    table.add_column("Load Bar", width=20)
    
    total_keys = sum(len(keys) for keys in distribution.values())
    
    if total_keys == 0:
        console.print("[red]No keys distributed[/red]")
        return
    
    # Sort nodes by key count for better visualization
    sorted_nodes = sorted(distribution.items(), key=lambda x: len(x[1]), reverse=True)
    
    for node_id, keys in sorted_nodes:
        key_count = len(keys)
        percentage = (key_count / total_keys) * 100
        
        # Create a simple bar chart
        bar_length = int((key_count / max(len(v) for v in distribution.values())) * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        table.add_row(
            node_id,
            f"{key_count:,}",
            f"{percentage:.2f}%",
            f"[bright_blue]{bar}[/bright_blue]"
        )
    
    console.print(table)
    
    # Show balance statistics
    key_counts = [len(keys) for keys in distribution.values()]
    avg_keys = sum(key_counts) / len(key_counts) if key_counts else 0
    min_keys = min(key_counts) if key_counts else 0
    max_keys = max(key_counts) if key_counts else 0
    
    console.print(f"\n[bold]Balance Statistics:[/bold]")
    console.print(f"  Average: {avg_keys:.1f} keys per node")
    console.print(f"  Range: {min_keys:,} - {max_keys:,} keys")
    console.print(f"  Balance ratio: {(max_keys / avg_keys):.2f}x" if avg_keys > 0 else "N/A")


def show_ring_state(ring: ConsistentHashRing):
    """Display the current state of the hash ring."""
    ring_state = ring.get_ring_state()
    
    console.print(f"\n[bold cyan]Hash Ring State[/bold cyan] ({len(ring_state)} positions)")
    
    table = Table(show_header=True, max_width=80)
    table.add_column("Position", justify="right", style="dim")
    table.add_column("Hash Value", style="cyan")
    table.add_column("Node", style="green")
    
    for i, (hash_val, node_id) in enumerate(ring_state[:20]):  # Show first 20 positions
        # Display hash in a more readable format
        hash_display = f"{hash_val:016x}"[-16:]  # Last 16 hex digits
        table.add_row(str(i + 1), hash_display, node_id)
    
    if len(ring_state) > 20:
        table.add_row("...", "...", "...")
    
    console.print(table)


def interactive_mode(ring: ConsistentHashRing, test_keys: List[str]):
    """Interactive mode for manipulating the hash ring."""
    console.print("\n[bold cyan]🎮 Interactive Mode[/bold cyan]")
    console.print("Commands: [bold]add <node_id>[/bold], [bold]remove <node_id>[/bold], [bold]status[/bold], [bold]quit[/bold]")
    
    original_distribution = ring.get_key_distribution(test_keys)
    
    while True:
        command = typer.prompt("\n> ").strip().lower()
        
        if command == "quit" or command == "q":
            break
        elif command == "status" or command == "s":
            current_distribution = ring.get_key_distribution(test_keys)
            show_key_distribution(current_distribution, "Current Distribution")
            
            # Show movement statistics
            moved_keys = ring.get_moved_keys(original_distribution, current_distribution)
            movement_percentage = (len(moved_keys) / len(test_keys)) * 100
            console.print(f"\n[bold yellow]Movement:[/bold yellow] {len(moved_keys):,} keys moved ({movement_percentage:.2f}%)")
            
        elif command.startswith("add "):
            parts = command.split()
            if len(parts) != 2:
                console.print("[red]Usage: add <node_id>[/red]")
                continue
            
            node_id = parts[1]
            if node_id in ring.nodes:
                console.print(f"[red]Node {node_id} already exists[/red]")
                continue
            
            # Get current distribution before adding
            before_distribution = ring.get_key_distribution(test_keys)
            
            # Add the node
            node = Node(node_id, replicas=1)  # Default 1 replica for interactive
            ring.add_node(node)
            console.print(f"[green]✓ Added node {node_id}[/green]")
            
            # Show impact
            after_distribution = ring.get_key_distribution(test_keys)
            moved_keys = ring.get_moved_keys(before_distribution, after_distribution)
            movement_percentage = (len(moved_keys) / len(test_keys)) * 100
            console.print(f"[yellow]Impact: {len(moved_keys):,} keys moved ({movement_percentage:.2f}%)[/yellow]")
            
        elif command.startswith("remove "):
            parts = command.split()
            if len(parts) != 2:
                console.print("[red]Usage: remove <node_id>[/red]")
                continue
            
            node_id = parts[1]
            if node_id not in ring.nodes:
                console.print(f"[red]Node {node_id} not found[/red]")
                continue
            
            # Get current distribution before removing
            before_distribution = ring.get_key_distribution(test_keys)
            
            # Remove the node
            removed_node = ring.remove_node(node_id)
            if removed_node:
                console.print(f"[green]✓ Removed node {node_id}[/green]")
                
                # Show impact
                after_distribution = ring.get_key_distribution(test_keys)
                moved_keys = ring.get_moved_keys(before_distribution, after_distribution)
                movement_percentage = (len(moved_keys) / len(test_keys)) * 100
                console.print(f"[yellow]Impact: {len(moved_keys):,} keys moved ({movement_percentage:.2f}%)[/yellow]")
            else:
                console.print(f"[red]Failed to remove node {node_id}[/red]")
        
        else:
            console.print("[yellow]Unknown command. Use: add <node_id>, remove <node_id>, status, quit[/yellow]")


@app.command()
def benchmark(
    min_nodes: int = typer.Option(2, help="Minimum number of nodes"),
    max_nodes: int = typer.Option(10, help="Maximum number of nodes"),
    keys: int = typer.Option(10000, help="Number of keys to test with"),
    virtual_nodes: int = typer.Option(3, help="Virtual nodes per physical node"),
):
    """
    Benchmark consistent hashing with different node counts.
    """
    console.print(Panel.fit(
        "[bold blue]🏁 Consistent Hash Benchmark[/bold blue]\n"
        f"Testing {min_nodes}-{max_nodes} nodes with {keys:,} keys",
        title="Benchmark Configuration"
    ))
    
    test_keys = generate_test_keys(keys)
    
    table = Table(title="Benchmark Results")
    table.add_column("Nodes", justify="right")
    table.add_column("Min Keys", justify="right")
    table.add_column("Max Keys", justify="right") 
    table.add_column("Avg Keys", justify="right")
    table.add_column("Balance Ratio", justify="right")
    table.add_column("Movement %", justify="right")
    
    prev_distribution = None
    
    for num_nodes in track(range(min_nodes, max_nodes + 1), description="Testing..."):
        ring = ConsistentHashRing()
        
        # Add nodes
        for i in range(num_nodes):
            node = Node(f"node-{i:02d}", replicas=virtual_nodes)
            ring.add_node(node)
        
        # Distribute keys
        distribution = ring.get_key_distribution(test_keys)
        key_counts = [len(keys) for keys in distribution.values()]
        
        avg_keys = sum(key_counts) / len(key_counts)
        min_keys = min(key_counts)
        max_keys = max(key_counts)
        balance_ratio = max_keys / avg_keys if avg_keys > 0 else 0
        
        # Calculate movement from previous configuration
        movement_pct = 0
        if prev_distribution:
            moved_keys = ring.get_moved_keys(prev_distribution, distribution)
            movement_pct = (len(moved_keys) / len(test_keys)) * 100
        
        table.add_row(
            str(num_nodes),
            str(min_keys),
            str(max_keys),
            f"{avg_keys:.1f}",
            f"{balance_ratio:.2f}x",
            f"{movement_pct:.1f}%" if movement_pct > 0 else "N/A"
        )
        
        prev_distribution = distribution
    
    console.print(table)


if __name__ == "__main__":
    app()
