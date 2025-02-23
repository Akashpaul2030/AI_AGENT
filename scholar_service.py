from typing import List, Dict
from scholarly import scholarly
from models import ResearchPaper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_paper_with_gpt(paper_info: dict) -> tuple[list, list]:
    """Analyze paper using GPT to extract key points and limitations"""
    llm = ChatOpenAI(model="gpt-4")
    
    prompt = f"""
    Analyze this research paper:
    Title: {paper_info.get('title')}
    Abstract: {paper_info.get('abstract', 'Not available')}
    
    Please identify:
    1. Key findings and contributions
    2. Limitations or research gaps
    
    Format your response as two lists.
    """
    
    response = llm.invoke(prompt)
    
    # Simple parsing - you might want to make this more robust
    try:
        parts = response.content.split("Limitations" or "Research gaps")
        key_points = [point.strip('- \n') for point in parts[0].split('\n') if point.strip('- \n')]
        limitations = [point.strip('- \n') for point in parts[1].split('\n') if point.strip('- \n')]
    except:
        key_points = ['Analysis failed']
        limitations = ['Analysis failed']
    
    return key_points, limitations

def search_papers(query: str, num_results: int = 5) -> List[ResearchPaper]:
    search_query = scholarly.search_pubs(query)
    results = []
    
    try:
        for _ in range(num_results):
            paper = next(search_query)
            # Analyze paper with GPT
            key_points, limitations = analyze_paper_with_gpt(paper.bib)
            
            results.append(ResearchPaper(
                title=paper.bib.get('title', ''),
                authors=paper.bib.get('author', []),
                url=paper.bib.get('url', ''),
                year=int(paper.bib.get('year', 0)),
                key_points=key_points,
                limitations=limitations,
                bibtex=paper.bibtex
            ))
    except StopIteration:
        pass
    
    return results