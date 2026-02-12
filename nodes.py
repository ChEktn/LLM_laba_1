from typing import Dict, Any
from models import GraphState, PlannerOutput, LiteratureReview, ReviewFeedback
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_deepseek.chat_models import ChatDeepSeek
import os
from textwrap import dedent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

def get_llm() -> ChatDeepSeek:
    return ChatDeepSeek(
        model=os.getenv("MODEL_NAME", ""),
        base_url=os.getenv("OPENAI_API_BASE", ""),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        api_base=os.getenv("OPENAI_API_BASE", ""),
        streaming=True,
        )


async def planner_node(state: GraphState) -> Dict[str, Any]:

    llm_planner = get_llm()

    planner_parser = PydanticOutputParser(pydantic_object=PlannerOutput)

    planner_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            dedent("""
            You are a planning agent for a research assistant.
            Return the information in the following JSON format:
            {format_instructions}
            """)
        ),
        (
            "human",
            dedent("""
            Topic: {topic}
            Year from: {year_from}
            Year to: {year_to}
            """)
        ),
    ])

    messages = planner_prompt.format_messages(
        topic=state.user_request.topic,
        year_from=state.user_request.year_from,
        year_to=state.user_request.year_to,
        format_instructions=planner_parser.get_format_instructions(),
    )

    response = await llm_planner.ainvoke(messages)
    plan = planner_parser.parse(response.content)

    return {"plan": plan}


async def writer_node(state: GraphState) -> Dict[str, Any]:
    llm_writer = get_llm()

    writer_parser = PydanticOutputParser(pydantic_object=LiteratureReview)

    writer_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            dedent("""
            You are a scientific writer.
            Return the information in the following JSON format:
            {format_instructions}
            """)
        ),
        (
            "human",
            dedent("""
            Topic: {topic}

            Papers:
            {papers}

            Trends:
            {trends}

            Authors:
            {authors}
            """)
        ),
    ])
    messages = writer_prompt.format_messages(
        topic=state.plan.topic,
        papers=[p.title for p in state.papers],
        trends=[t.trend for t in state.trends],
        authors=[a.author for a in state.authors],
        format_instructions=writer_parser.get_format_instructions(),
    )

    response = await llm_writer.ainvoke(messages)
    final_answer = writer_parser.parse(response.content)

    return {"final_answer": final_answer}



async def reviewer_node(state: GraphState) -> Dict[str, Any]:
    llm_reviewer = get_llm()

    reviewer_parser = PydanticOutputParser(pydantic_object=ReviewFeedback)

    reviewer_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            dedent("""
            You are a scientific reviewer.
            Return the information in the following JSON format:
            {format_instructions}
            """)
        ),
        (
            "human",
            dedent("""
            Review and improve this draft:
            {draft}
            """)
        ),
    ])

    messages = reviewer_prompt.format_messages(
        draft=state.final_answer.model_dump_json(indent=2),
        format_instructions=reviewer_parser.get_format_instructions(),
    )

    response = await llm_reviewer.ainvoke(messages)
    feedback = reviewer_parser.parse(response.content)

    return {"reviewed_answer": feedback.improved_review}

if __name__ == "__main__":

    llm = get_llm()
    print(llm.invoke("Hello"))