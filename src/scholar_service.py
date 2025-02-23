from scholarly import scholarly
from models import ResearchPaper

def search_papers(query: str, num_results: int = 5) -> List[ResearchPaper]:
    search_query = scholarly.search_pubs(query)
    results = []
    try:
        for _ in range(num_results):
            paper = next(search_query)
            results.append(ResearchPaper(
                title=paper.bib.get('title', ''),
                authors=paper.bib.get('author', []),
                url=paper.bib.get('url', ''),
                year=int(paper.bib.get('year', 0)),
                key_points=[],
                limitations=[],
                bibtex=paper.bibtex
            ))
    except StopIteration:
        pass
    return results