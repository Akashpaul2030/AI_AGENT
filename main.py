from typing import List
from pydantic import BaseModel, Field
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    summary: str
    key_points: List[str]
    limitations: List[str]
    methodology: str
    future_directions: str

def analyze_paper(title: str) -> ResearchPaper:
    """Use GPT-4 to analyze a research paper title and generate insights"""
    
    prompt = f"""
    Analyze this research paper title in depth:
    "{title}"
    
    Provide a detailed analysis including:
    1. Potential authors (suggest 3-4 realistic author names)
    2. A comprehensive summary (2-3 paragraphs)
    3. Key findings/points (4-5 points)
    4. Research limitations (2-3 points)
    5. Methodology used
    6. Future research directions
    
    Make the analysis specific to AI in mental health therapy.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        
        # Parse the response into sections
        sections = content.split("\n\n")
        
        # Extract information
        authors = []
        summary = ""
        key_points = []
        limitations = []
        methodology = ""
        future_directions = ""
        
        for section in sections:
            if "Authors" in section:
                authors = [a.strip() for a in section.split("\n")[1:] if a.strip()]
            elif "Summary" in section:
                summary = section.split("Summary:")[1].strip()
            elif "Key findings" in section or "Key points" in section:
                key_points = [p.strip("- ") for p in section.split("\n")[1:] if p.strip()]
            elif "Limitations" in section:
                limitations = [l.strip("- ") for l in section.split("\n")[1:] if l.strip()]
            elif "Methodology" in section:
                methodology = section.split("Methodology:")[1].strip()
            elif "Future" in section:
                future_directions = section.split("Future")[1].split(":")[1].strip()
        
        return ResearchPaper(
            title=title,
            authors=authors,
            summary=summary,
            key_points=key_points,
            limitations=limitations,
            methodology=methodology,
            future_directions=future_directions
        )
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        raise

def export_to_excel(paper: ResearchPaper, filename: str):
    """Export paper analysis to Excel with proper formatting"""
    
    # Create DataFrame with expanded information
    df = pd.DataFrame({
        'Title': [paper.title],
        'Authors': [', '.join(paper.authors)],
        'Summary': [paper.summary],
        'Key Points': ['\n'.join(f"• {point}" for point in paper.key_points)],
        'Limitations': ['\n'.join(f"• {limit}" for limit in paper.limitations)],
        'Methodology': [paper.methodology],
        'Future Directions': [paper.future_directions]
    })
    
    # Export to Excel with formatting
    try:
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Research Analysis')
        
        # Get the workbook and the worksheet
        workbook = writer.book
        worksheet = writer.sheets['Research Analysis']
        
        # Adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = min(adjusted_width, 50)
        
        # Save the file
        writer.close()
        print(f"\nAnalysis exported to {filename}")
        
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")

def main():
    title = "Artificial Intelligence in Enhancing Cognitive Behavioural Therapy Outcomes for Depression: A Review"
    
    print("Analyzing research paper...")
    paper = analyze_paper(title)
    
    # Display results
    print("\nAnalysis Results:")
    print("-" * 80)
    print(f"Title: {paper.title}")
    print("\nAuthors:", ", ".join(paper.authors))
    print("\nSummary:", paper.summary)
    print("\nKey Points:")
    for point in paper.key_points:
        print(f"• {point}")
    print("\nLimitations:")
    for limit in paper.limitations:
        print(f"• {limit}")
    print("\nMethodology:", paper.methodology)
    print("\nFuture Directions:", paper.future_directions)
    
    # Export to Excel
    export_to_excel(paper, "research_analysis.xlsx")

if __name__ == "__main__":
    main()