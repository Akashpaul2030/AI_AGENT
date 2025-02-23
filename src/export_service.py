import pandas as pd
from models import ResearchPaper
from typing import List

def export_to_excel(papers: List[ResearchPaper], filename: str):
    papers_df = pd.DataFrame([{
        'Title': p.title,
        'Authors': ', '.join(p.authors),
        'Year': p.year,
        'URL': p.url,
        'Key Points': '\n'.join(p.key_points),
        'Limitations': '\n'.join(p.limitations),
        'BibTeX': p.bibtex
    } for p in papers])
    papers_df.to_excel(filename, index=False)
    print(f"Exported {len(papers)} papers to {filename}")