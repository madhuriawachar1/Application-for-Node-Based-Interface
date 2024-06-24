from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Data models for nodes and edges
class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, str]

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    
    
# Endpoint to parse the pipeline data
@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    nodes = pipeline.nodes
    edges = pipeline.edges

    num_nodes = len(nodes)
    num_edges = len(edges)


    # Build the graph representation
    graph = {node.id: [] for node in nodes}
    for edge in edges:
        graph[edge.source].append(edge.target)
        
    # Function to check if the graph is a Directed Acyclic Graph (DAG)
    def is_dag(graph):
        visited = set()
        rec_stack = set()

        def dfs(node):
            if node in rec_stack:
                return False
            if node in visited:
                return True

            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            rec_stack.remove(node)
            return True

        for node in graph:
            if not dfs(node):
                return False
        return True

    is_dag_result = is_dag(graph)

    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag_result}
