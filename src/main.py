from scholar_service import search_papers
from export_service import export_to_excel

def main():
    query = "artificial intelligence mental health therapy"
    print(f"Searching for papers about: {query}")
    papers = search_papers(query, num_results=5)
    
    for paper in papers:
        print(f"\nFound paper: {paper.title}")
        print(f"Authors: {', '.join(paper.authors)}")
        print("-" * 50)
    
    export_to_excel(papers, "research_results.xlsx")

if __name__ == "__main__":
    main()