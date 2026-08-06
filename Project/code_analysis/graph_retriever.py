from .repository_graph import REPOSITORY_GRAPH
class GRAPH_RETRIEVER:
    """
    Traverses and queries the Repository Graph.
    """
    def __init__(self, 
                 repository_graph,
                 repository_indices):
        
        self.graph = repository_graph
        self.repository_indices = repository_indices
    
    def resolve_node(self, document:dict):
        
        metadata = document.get("metadata",{})
        file_name = metadata.get("file_name")
        
        if not file_name:
            return None
        node_id = f"file:{file_name}"
        return self.find_node(node_id)
        
    def find_node(self, node_id):
        
        return self.graph.nodes.get(node_id)
        
    def get_children(self, node_id):
        """
        Return all child nodes connected to outgoing edges
        """
        
        children = []
        for edge in self.graph.edges:
            
            if edge["source"] == node_id:
                child = self.find_node(edge["target"])
                if child:
                    children.append(child)
        return children
        
    def get_parent(self, node_id):
        """
        Return the immediate parent node.
        """
        
        for edge in self.graph.edges:
            if edge["target"] == node_id:
                return self.find_node(edge["source"])
            
        return None
    def get_neighbors(self, node_id):
        """
        Return every directly connected node.
        """
        
        neighbors = []
        
        parent = self.get_parent(node_id)
        if parent:
            neighbors.append(parent)
        
        neighbors.extend(
            self.get_children(node_id)
        )
        
        return neighbors
    
    def expand_context(self, node):
        """
            Expand a graph node into repository context.

            Args:
                node (dict): Graph node

            Returns:
                dict | None
        """

        if node is None:
            return None
        
        repository_context = None
                
        if node["type"] == "file":
            graph_context = self.repository_indices.get(
                node["name"]
            )
            parent = self.get_parent(node_id=node["id"])
            children = self.get_children(node_id=node["id"])
            neighbors = self.get_neighbors(node_id=node["id"])
            
            return {
                "graph_context":graph_context,
                "parent":parent,
                "children":children,
                "neighbors":neighbors
            }
        
    def enrich_document(self, doc:dict):
        """
        This Because Retriever.py does'nt know how graph_retriever.py
        """
        
        node = self.resolve_node(doc)
        
        if node is None:
            return doc
        
        repository_context = self.expand_context(node)
        doc["graph_node"] = node
        doc["graph_context"] = repository_context
        
        return doc
