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
WEBWEB_CONFIG_PATH = DATA_PATH.joinpath("webweb-config.yaml")


def load_yaml(path):
    """Load YAML data from a file"""
    return yaml.load(path.read_text(), Loader=yaml.FullLoader)


def load_config():
    """Load all configuration from config file"""
    config = load_yaml(WEBWEB_CONFIG_PATH)
    
    colors = config.get("colors", {})
    sizes = config.get("sizes", {})
    display = config.get("display", {})
    scales = config.get("scales", {})
    labels = config.get("labels", {})
    
    return {
        "colors": {
            "lab member": colors.get("lab_member", "#E01E7B"),
            "alumni": colors.get("alumni", "#9d1557"),
            "paper": colors.get("paper", "#1C7BE0"),
            "collaborator": colors.get("collaborator", "#999999"),
        },
        "sizes": {
            "lab member": sizes.get("lab_member", 2.0),
            "alumni": sizes.get("alumni", 1.8),
            "paper": sizes.get("paper", 0.7),
            "collaborator": {
                "one_paper": sizes.get("collaborator", {}).get("one_paper", 0.3),
                "few_papers": sizes.get("collaborator", {}).get("few_papers", 0.5),
                "many_papers": sizes.get("collaborator", {}).get("many_papers", 0.9),
            }
        },
        "display": {
            "gravity": display.get("gravity", 0.7),
            "width": display.get("width", 600),
            "height": display.get("height", 600),
            "scaleLinkOpacity": display.get("scaleLinkOpacity", True),
            "scaleLinkWidth": display.get("scaleLinkWidth", True),
            "hideMenu": display.get("hideMenu", True),
            "showLegend": display.get("showLegend", False),
        },
        "scales": {
            "nodeSize": {
                "min": scales.get("nodeSize", {}).get("min", 0.3),
                "max": scales.get("nodeSize", {}).get("max", 2.0),
            }
        },
        "labels": {
            "fontSize": labels.get("fontSize", 14),
            "fontColor": labels.get("fontColor", "#333333"),
            "fontOutline": labels.get("fontOutline", True),
            "fontOutlineColor": labels.get("fontOutlineColor", "#FFFFFF"),
            "fontOutlineWidth": labels.get("fontOutlineWidth", 3),
        }
    }


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
    
    # Load config
    config = load_config()
    colors = config["colors"]
    sizes = config["sizes"]
    display_config = config["display"]
    scales_config = config["scales"]
    labels_config = config["labels"]
    
    # Create name mapping for quick lookup
    name_map = create_name_to_member_map(members)
    
    # FIRST: Set up lab member and alumni nodes so they exist before processing papers
    for member in members:
        name = member["name"]
        group = member["group"]
        
        # Add all lab members/alumni
        if group == "alum":
            nodes[name]["kind"] = "alumni"
        else:
            nodes[name]["kind"] = "lab member"
        
        nodes[name]["name"] = name
    
    # THEN: Process each paper from citations
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
                # Use the canonical name - this ensures aliases map to the same node
                canonical_name = name_map[cleaned_author]["canonical_name"]
                collaborator_connections[canonical_name].add(title)
                edges.append([title, canonical_name])
            else:
                # External collaborator - use the name as it appears
                collaborator_connections[cleaned_author].add(title)
                edges.append([title, cleaned_author])
    
    # Set up collaborator nodes (external people only)
    for name in collaborator_connections:
        # Only add if not already a lab member/alumni
        if name not in nodes:
            nodes[name]["name"] = name
            nodes[name]["kind"] = "collaborator"
    
    # Set size and color based on node kind and connection count
    for node in nodes:
        kind = nodes[node]["kind"]
        
        # Set color
        nodes[node]["color"] = colors[kind]
        
        # Set size
        if kind == "paper":
            size = sizes["paper"]
        elif kind == "lab member":
            size = sizes["lab member"]
        elif kind == "alumni":
            size = sizes["alumni"]
        elif kind == "collaborator":
            connection_count = len(collaborator_connections.get(node, set()))
            
            if connection_count < 2:
                size = sizes["collaborator"]["one_paper"]
            elif connection_count < 5:
                size = sizes["collaborator"]["few_papers"]
            else:
                size = sizes["collaborator"]["many_papers"]

        nodes[node]["size"] = size
    
    # Create and configure the web using config values
    web = Web(adjacency=edges, nodes=dict(nodes))
    web.display.sizeBy = "size"
    web.display.colorBy = "color"
    web.display.hideMenu = display_config["hideMenu"]
    web.display.showLegend = display_config["showLegend"]
    web.display.gravity = display_config["gravity"]
    web.display.width = display_config["width"]
    web.display.height = display_config["height"]
    web.display.scaleLinkOpacity = display_config["scaleLinkOpacity"]
    web.display.scaleLinkWidth = display_config["scaleLinkWidth"]
    web.display.scales = scales_config
    
    # Add label styling
    web.display.nameFontSize = labels_config["fontSize"]
    web.display.nameFontColor = labels_config["fontColor"]
    
    # Save
    WEBWEB_JSON_PATH.write_text(web.json)

    return web


def main():
    """Main function to generate the network"""
    members = load_members()
    citations = load_yaml(CITATIONS_PATH)
    make_network(members, citations)


if __name__ == "__main__":
    main()