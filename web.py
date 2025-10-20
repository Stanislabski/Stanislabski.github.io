from collections import defaultdict
from webweb import Web
from pathlib import Path
import yaml
import frontmatter

# Define constants for paths
DATA_PATH = Path(__file__).parent.joinpath("_data")
MEMBERS_PATH = Path(__file__).parent.joinpath("_members")
CITATIONS_PATH = DATA_PATH.joinpath("citations.yaml")
WEBWEB_JSON_PATH = DATA_PATH.joinpath("webweb.json")

# Map groups to colors
KIND_TO_COLOR_MAP = {
    "collaborator": "#999999",      # Gray for collaborators
    "lab member": "#E01E7B",        # Pink for current lab members
    "alumni": "#9d1557",            # Dark pink for alumni
    "paper": "#1C7BE0",             # Blue for papers
}


def load_yaml(path):
    """Load YAML data from a file"""
    return yaml.load(path.read_text(), Loader=yaml.FullLoader)


def clean_name(name):
    """Clean author names by removing trailing punctuation"""
    return name.rstrip("*.")


def load_members():
    """Load all members from the _members directory"""
    members = []
    
    for md_file in MEMBERS_PATH.glob("*.md"):
        # Parse the markdown file with frontmatter
        post = frontmatter.load(md_file)
        
        # Extract relevant information
        name = post.get("name")
        aliases = post.get("aliases", [])
        group = post.get("group", "active")  # Default to active if not specified
        
        if name:
            members.append({
                "name": clean_name(name),
                "aliases": [clean_name(alias) for alias in aliases],
                "group": group
            })
    
    return members


def create_name_to_member_map(members):
    """Create a mapping from all possible names/aliases to the canonical member name"""
    name_map = {}
    
    for member in members:
        canonical_name = member["name"]
        
        # Map the main name to itself
        name_map[canonical_name] = {
            "canonical_name": canonical_name,
            "group": member["group"]
        }
        
        # Map all aliases to the canonical name
        for alias in member["aliases"]:
            name_map[alias] = {
                "canonical_name": canonical_name,
                "group": member["group"]
            }
    
    return name_map


def make_network(members, citations):
    """Create the network from members and citations"""
    nodes = defaultdict(dict)
    edges = []
    collaborator_connections = defaultdict(set)  # Track unique connections per collaborator
    
    # Create name mapping for quick lookup
    name_map = create_name_to_member_map(members)
    
    print(f"Found {len(name_map)} unique names/aliases mapping to {len(members)} members")
    
    # Process each paper from citations
    for paper in citations:
        title = paper.get("title", "")
        authors = paper.get("authors", [])
        
        if not title or not authors:
            continue
        
        # Add paper as a node
        nodes[title] = {
            "name": title,
            "kind": "paper"
        }
        
        # Add link if available
        if paper.get("link"):
            nodes[title]["url"] = paper["link"]
        
        # Connect paper to ALL authors
        for author in authors:
            cleaned_author = clean_name(author)
            
            # Check if this author is a lab member (or alias of one)
            if cleaned_author in name_map:
                # Use the canonical name
                canonical_name = name_map[cleaned_author]["canonical_name"]
                collaborator_connections[canonical_name].add(title)
                edges.append([title, canonical_name])
            else:
                # External collaborator
                collaborator_connections[cleaned_author].add(title)
                edges.append([title, cleaned_author])
    
    # Set up lab member and alumni nodes
    for member in members:
        name = member["name"]
        group = member["group"]
        
        # Add all lab members/alumni (even if no papers yet)
        if group == "alum":
            nodes[name]["kind"] = "alumni"
        else:
            nodes[name]["kind"] = "lab member"
        
        nodes[name]["name"] = name
    
    # Set up collaborator nodes (external people only)
    for name in collaborator_connections:
        # Only add if not already a lab member/alumni
        if name not in nodes:
            nodes[name]["name"] = name
            nodes[name]["kind"] = "collaborator"
    
    # Print connection counts for debugging
    print("\nTop 20 collaborators by paper count:")
    for name, connections in sorted(collaborator_connections.items(), 
                                   key=lambda x: len(x[1]), reverse=True)[:20]:
        kind = nodes[name].get("kind", "unknown")
        print(f"{name} ({kind}): {len(connections)}")
    
    # Set size based on node kind and connection count
    for node in nodes:
        kind = nodes[node]["kind"]
        
        if kind == "paper":
            size = 0.7  # Papers are small
        elif kind == "lab member":
            size = 2.0  # Lab members are large
        elif kind == "alumni":
            size = 1.8  # Alumni are medium-small
        elif kind == "collaborator":
            connection_count = len(collaborator_connections.get(node, set()))
            
            if connection_count < 2:  # One-off collaborators
                size = 0.3
            elif connection_count < 5:  # 2-4 papers
                size = 0.5
            else:  # 5+ papers
                size = 0.8

        nodes[node]["size"] = size
        nodes[node]["color"] = KIND_TO_COLOR_MAP[kind]
    
    # Create and configure the web
    web = Web(adjacency=edges, nodes=dict(nodes))
    web.display.sizeBy = "size"
    web.display.colorBy = "color"
    web.display.hideMenu = True
    web.display.showLegend = False
    web.display.gravity = 0.7
    web.display.width = 600
    web.display.height = 600
    web.display.scaleLinkOpacity = True
    web.display.scaleLinkWidth = True
    web.display.scales = {
        "nodeSize": {
            "min": 0.7,
            "max": 2,
        }
    }
    
    # Save and display
    print(f"\nWriting network data to {WEBWEB_JSON_PATH}")
    WEBWEB_JSON_PATH.write_text(web.json)
    print("File written successfully!")
    
    web.show()

    return web


def main():
    """Main function to generate the network"""
    print("Loading lab members from _members directory...")
    members = load_members()
    print(f"Found {len(members)} members")
    
    print("\nLoading citations from citations.yaml...")
    citations = load_yaml(CITATIONS_PATH)
    print(f"Found {len(citations)} publications")
    
    print("\nBuilding network...")
    make_network(members, citations)
    
    print("\nNetwork built and saved successfully!")


if __name__ == "__main__":
    main()