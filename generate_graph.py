from langgraph_workflow.graph import builder

graph = builder.compile()

mermaid = graph.get_graph().draw_mermaid()

with open("workflow_graph.md", "w", encoding="utf-8") as f:
    f.write(mermaid)

print("workflow_graph.md created successfully.")