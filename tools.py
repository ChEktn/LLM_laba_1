
from models import GraphState, PlannerOutput, AuthorStats, Paper, TrendSummary
from typing import List, Dict, Any
import arxiv
from tenacity import retry, stop_after_attempt, wait_exponential

async def paper_search_node(state: GraphState) -> Dict[str, Any]:
    papers = await search_arxiv_papers(state.plan)
    return {"papers": papers}


async def trend_analysis_node(state: GraphState) -> Dict[str, Any]:
    trends = await extract_trends(state.papers)
    return {"trends": trends}


async def author_analysis_node(state: GraphState) -> Dict[str, Any]:
    authors = await extract_author_statistics(state.papers)
    return {"authors": authors}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
async def search_arxiv_papers(plan: PlannerOutput, max_results: int = 5) -> List[Paper]:
    query = f"{plan.topic}"

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in search.results():
        papers.append(Paper(
            title=result.title,
            abstract=result.summary,
            authors=[a.name for a in result.authors],
            year=result.published.year,
        ))

    return papers


async def extract_trends(papers: List[Paper]) -> List[TrendSummary]:
    trends = []
    if any("Transformer" in p.title for p in papers):
        trends.append(TrendSummary(
            trend="Transformer architectures",
            explanation="Widespread adoption of transformer-based models across NLP tasks."
        ))
    if any("Few-Shot" in p.title or "Few-Shot" in p.abstract for p in papers):
        trends.append(TrendSummary(
            trend="Few-shot and zero-shot learning",
            explanation="Models increasingly perform well with minimal labeled data."
        ))
    return trends


async def extract_author_statistics(papers: List[Paper]) -> List[AuthorStats]:
    author_freq: Dict[str, int] = {}
    for paper in papers:
        for author in paper.authors:
            author_freq[author] = author_freq.get(author, 0) + 1

    return [AuthorStats(author=k, paper_count=v) for k, v in author_freq.items()]

