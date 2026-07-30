from pathlib import Path
import sys 
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

class REPOSITORY_GRAPH:
    def __init__(self):
        self.edges = [] # Relationship Data
        self.nodes = {} # id -> node metadata
    
    def add_node(self, node:dict):
        
        node_id = node["id"]
        
        if node_id not in self.nodes:
            self.nodes[node_id] = node
    
    def build_nodes(self, repository_index:dict):
        
        file_name = repository_index["file_name"]

        # ------------------------
        # File Node
        # ------------------------
        self.add_node(
            {
                "id": f"file:{file_name}",
                "type": "file",
                "name": file_name,
            }
        )
        
        for cls in repository_index["classes"]:
            self.add_node(
                {
                "id":f"class:{cls['name']}",
                "type":"class",
                "name":cls["name"]
                }
            )
        
        for func in repository_index["functions"]:
            self.add_node(
                {
                "id":f"function:{func['name']}",
                "type":"function",
                "name":func["name"]
                }
            )
        
        for method in repository_index["methods"]:
            self.add_node(
                {
                "id": f"method:{method['class']}.{method['name']}",
                "type":"method",
                "name":method["name"]
                }
            )

        for module in repository_index["imports"]:
            self.add_node(
                {
            "id":f"module:{module}",
            "type":"module",
            "name":module
                }
            )
            
    def add_edge(self,
                  source:str,
                  target:str,
                  relation:str):
    
        if source not in self.nodes:
            logger.error(f"{source} does not exist")
            raise ValueError(f"{source} does not exist")

        if target not in self.nodes:
            logger.error(f"{target} does not exist")
            raise ValueError(f"{target} does not exist")

        self.edges.append(
            {
                "source":source,
                "target":target,
                "relation":relation
            }
        )
    
    def build_edges(
        self,
        repository_index:dict
    ):
        self._build_contains_edges(repository_index)
        self._build_owns_edges(repository_index)
        self._build_imports_edges(repository_index)
    
    def _build_contains_edges(self, repository_index:dict):
        file_name = repository_index["file_name"]
        for cls in repository_index["classes"]:
            self.add_edge(
                    source=f"file:{file_name}",
                    target=f"class:{cls['name']}",
                    relation="contains"
                    )
        for func in repository_index["functions"]:
            self.add_edge(
                    source=f"file:{file_name}",
                    target=f"function:{func['name']}",
                    relation="contains"
                    )
    
    def _build_owns_edges(self, repository_index:dict):
        for method in repository_index["methods"]:
            self.add_edge(
                source=f"class:{method['class']}",
                target=f"method:{method['class']}.{method['name']}",
                relation="owns"
            )
    
    def _build_imports_edges(self, repository_index:dict):
        file_name = repository_index["file_name"]
        for module in repository_index["imports"]:
            self.add_edge(
                source=f"file:{file_name}",
                target=f"module:{module}",
                relation="imports"
            )
    def build(self, repository_index):
        self.build_nodes(repository_index)
        self.build_edges(repository_index)
        