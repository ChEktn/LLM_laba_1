import asyncio
from models import *
from graph import build_graph


async def demo():
    user_input = LiteratureRequest(
        topic="Large Language Models in Natural Language Processing",
        year_from=2017,
        year_to=2024
    )

    initial_state = GraphState(user_request=user_input)
    app = build_graph()
    result = await app.ainvoke(initial_state)

    review = result["reviewed_answer"]

    print("\n=== FINAL LITERATURE REVIEW ===\n")

    print("Key papers:")
    for paper in review.key_papers:
        print(f"- {paper}")

    print("\nMain trends:")
    for trend in review.main_trends:
        print(f"- {trend}")

    print("\nTop authors:")
    for author in review.top_authors:
        print(f"- {author}")

    print("\nOpen research questions:")
    for q in review.open_questions:
        print(f"- {q}")


if __name__ == "__main__":
    asyncio.run(demo())
