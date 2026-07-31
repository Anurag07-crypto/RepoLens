import ast
from pathlib import Path
import sys 
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from logger import get_logger

logger = get_logger(__name__)

class AST_PARSER:
    """
    Parses Python source files into an Abstract Syntax Tree (AST).
    """
    def parse_file(self, file_path:str)->ast.AST:
        """
        Parse the python source file into ast

        Args:
            file_path (str): file_path of python file

        Returns:
            ast.AST: Root node of the parsed AST
        """
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            logger.info("Sourced code parsed")
            return tree
        
        except SyntaxError as e:
            logger.error(f"Getting a Syntax Error in {file_path} : e")
            raise SystemError(f"Getting Syntax Error in {file_path}") from e

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            raise
    
    def print_ast(self, tree:ast.AST):
        "Prints the AST structure"
        print(ast.dump(tree, indent=4))
        
    def extract_imports(self, tree:ast.AST)->list[str]:
        "Extract all imported Modules from AST"
        
        imports = set()
        for node in ast.walk(tree):
            
            if isinstance(node, ast.Import):
                
                for alias in node.names:
                    imports.add(alias.name)
                    
            elif isinstance(node, ast.ImportFrom):
                
                if node.module:
                    imports.add(node.module)
        return sorted(imports)
    
    def extract_classes(self, tree:ast.AST)->list[dict]:
        "Extract all classes definitions from AST"
        
        classes = []
        
        for node in ast.walk(tree):
            
            if isinstance(node, ast.ClassDef):
                classes.append(
                    {
                        "name": node.name,
                        "line": node.lineno,
                        "doc_string":ast.get_docstring(node)
                    }
                )
        return sorted(classes, key=lambda cls: cls["line"])

    def extract_functions(
        self,
        tree:ast.Module,
        file_path:str,
    )->list[dict]:
        
        "Extract Standalone (Module level) functions"
        
        functions = []
        
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(
                    {
                        "name":node.name,
                        "file":Path(file_path).name,
                        "line":node.lineno,
                        "args":[
                            arg.arg 
                            for arg in node.args.args
                        ],
                        "doc_string":ast.get_docstring(node)
                    }
                )
        return functions
    
    def extract_methods(
        self,
        tree:ast.Module,
        file_path:str
    )->list[dict]:
        
        "Extract Methods from Class"
        
        methods = []
        
        for node in tree.body:
            
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(
                            {
                                "class":class_name,
                                "name":item.name,
                                "file":Path(file_path).name,
                                "line":item.lineno,
                                "args":[
                                    arg.arg
                                    for arg in item.args.args
                                ],
                                "doc_string":ast.get_docstring(item)
                            }
                        )
        return methods
    
    def build_repository_index(
        self,
        file_path:str
    )->dict:
        
        " Parse a Python file and build a structured repository index."
        
        tree = self.parse_file(file_path)
        
        return {
            "file_name":Path(file_path).name,
            "imports":self.extract_imports(tree),
            "classes":self.extract_classes(tree),
            "functions":self.extract_functions(tree, file_path),
            "methods":self.extract_methods(tree, file_path)
        }
        
