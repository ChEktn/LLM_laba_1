from models import GraphState
from langgraph.graph import StateGraph, END
from nodes import planner_node, writer_node, reviewer_node
from tools import paper_search_node, trend_analysis_node, author_analysis_node 

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("planner", planner_node)

    graph.add_node("paper_search", paper_search_node)

    graph.add_node("trend_analysis", trend_analysis_node)

    graph.add_node("author_analysis", author_analysis_node)

    graph.add_node("writer", writer_node)

    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "paper_search")

    graph.add_edge("paper_search", "trend_analysis")

    graph.add_edge("paper_search", "author_analysis")

    graph.add_edge("trend_analysis", "writer")

    graph.add_edge("author_analysis", "writer")

    graph.add_edge("writer", "reviewer")

    graph.add_edge("reviewer", END)

    app = graph.compile()

    return app
