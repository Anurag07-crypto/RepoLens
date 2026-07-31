from langchain_core.documents import Document
from typing import List
import sys
from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
sys.path.insert(0 ,str(Path(__file__).parent.parent))
from logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
logger = get_logger(__name__)

class SEMANTIC_CHUNKER:
    def __init__(self):
        self.parser = Parser()
        self.parser.language = Language(tspython.language())
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n\n","\n\n","\n",""],
            chunk_size=2000,
            chunk_overlap = 200
        )
        
    def chunk_documents(self, docs:List[Document])-> List[Document]:
        
        semantic_chunks = []
        
        for doc in docs:
            language = self._detect_language(doc)
            
            if language == "py":
                chunks = self._chunk_python(doc)
            else:
                chunks = self._chunk_texts(doc)
            semantic_chunks.extend(chunks)
        logger.info("Semantic_chunks_loaded")
        return semantic_chunks

    def _detect_language(self, doc):
        file_path = doc.metadata.get("source", "")
        language = Path(file_path).suffix.replace(".", "")
        return language
    
    def _chunk_python(self, doc:List[Document])-> List[Document]:
        """
            Python Semantic chunking
        Args:
            doc (List[Document]): List of documents

        Returns:
            List[Document]: doc
        """
        source_code = doc.page_content
        tree = self.parser.parse(
            bytes(source_code,"utf-8")
        )
        root = tree.root_node
        return self._create_chunk(doc, source_code, root)

    def _create_chunk(self, doc, source_code, root):
        semantic_nodes = self._collect_nodes(root)
        if not semantic_nodes:
            return self._chunk_texts(doc)
        chunks = []
        
        for node in semantic_nodes:
            logger.info(
        f"{node.type} | {node.start_point} -> {node.end_point}"
    )
            start_byte = node.start_byte
            end_byte = node.end_byte
            
            chunk_text = source_code[start_byte:end_byte]
            
            metadata = doc.metadata.copy()
            metadata["chunk_type"] = node.type
            metadata["symbol"] = self._get_symbol_name(node)
            metadata["start_line"] = node.start_point[0] + 1
            metadata["end_line"] = node.end_point[0] + 1
            
            chunk = Document(
                page_content=chunk_text,
                metadata=metadata
            )
            
            chunks.append(chunk)
                    
        logger.info("RootNode Created")
        return chunks
    
    def _chunk_texts(self, doc:List[Document])-> List[Document]:
        """
        Fallback of Unsupported languages
        """
        return self.text_splitter.split_documents([doc])
    
    def _collect_nodes(self, root_node):
        
        semantic_nodes = []
        for child in root_node.children:
            if child.type in (
                "function_definition",
                "class_definition"
            ):
                semantic_nodes.append(child)
        for child in root_node.children:
            semantic_nodes.extend(self._collect_nodes(child))
            
        return semantic_nodes
    
    def _get_symbol_name(self, node):
        
        for child in node.children:
            if child.type == "identifier":
                return child.text.decode("utf-8")
        return None
    