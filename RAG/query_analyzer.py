import re
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import get_logger

logger = get_logger(__name__)

class QUERY_ANALYZER:
    """
    Analyzes the query and list them into a filter metadata
    """
    
    def __init__(self):
        logger.info("Query Analyzer Initialized")
        self.language_map = {
                            "python": "py",
                            "jyputer": "pynb",  
                            "java": "java",
                            "javascript": "js",
                            "typescript": "ts",
                            "c": "c",
                            "cpp": "cpp",
                            "c++": "cpp",
                            "csharp": "cs",
                            "c#": "cs",
                            "go": "go",
                            "golang": "go",
                            "rust": "rs",
                            "ruby": "rb",
                            "php": "php",
                            "swift": "swift",
                            "kotlin": "kt",
                            "scala": "scala",
                            }
        self.intent = {
            "explain": ["explain", "describe", "how"],
            "find": ["find", "search", "locate"],
            "summarize": ["summarize", "summary"],
            "compare": ["compare", "difference", "vs"]
        }
    
    def analyzer(self, query:str) -> Dict[str, Any]:
        """
        Analyzing function

        Args:
            query (str): user provided query

        Returns:
            Dict[str, Any]: dict of results
        """
        
        analysis = {
            "semantic_query":query,
            "filters":{}
        }
        filename_pattern = r"\b[\w\-]+\.[A-Za-z0-9]+\b"
        match = re.search(filename_pattern, query)
        
        if match:
            file_name = match.group()
            analysis["filters"]["file_name"] = file_name
            analysis["semantic_query"] = query
        lower_query = analysis["semantic_query"].lower()

        for language, extension in self.language_map.items():
            if re.search(rf"\b{re.escape(language)}\b", lower_query):

                analysis["filters"]["language"] = extension

                analysis["semantic_query"] = re.sub(
                                                    rf"\b{re.escape(language)}\b",
                                                        "",
                                                        analysis["semantic_query"],
                                                        flags=re.IGNORECASE
                                                    ).strip()
                break
        analysis["intent"] = "general"
        lower_query = analysis["semantic_query"].lower()
        for intent, keywords in self.intent.items():
            if any(keyword in lower_query for keyword in keywords):
                analysis["intent"] = intent
                break
        logger.info(f"Query Analyzed: {analysis}")
        return analysis
    
''' Flow of the Analyzer
User Query
     │
     ▼
Create analysis dictionary
     │
     ▼
File Name Detection
     │
     ▼
Language Detection
     │
     ▼
(Next: Directory Detection)
     │
     ▼
Return analysis
'''
