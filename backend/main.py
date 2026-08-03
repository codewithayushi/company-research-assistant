from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from search import find_official_website, search_web
from scraper import crawl_website
from ai_service import analyze_company_data
from pdf_generator import generate_pdf_report
from discord_service import send_report_to_discord
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str
    model: str = "openai/gpt-3.5-turbo"
    applicant_name: str = None
    applicant_email: str = None
    discord_token: str = None
    discord_channel_id: str = None

@app.post("/api/research")
def research_company(req: ResearchRequest):
    target_url = req.query.strip()
    
    # If user provided a company name instead of URL
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = find_official_website(req.query)
        if not target_url:
            raise HTTPException(status_code=400, detail="Could not find official website for the given company name.")
    
    search_results = search_web(req.query)
    scraped_text = crawl_website(target_url, max_pages=3)
    
    ai_data = analyze_company_data(req.query, scraped_text, search_results, req.model)
    ai_data["website"] = target_url
    
    pdf_filename = f"report_{abs(hash(target_url))}.pdf"
    generate_pdf_report(ai_data, pdf_filename)
    
    if req.discord_token and req.discord_channel_id and req.applicant_name and req.applicant_email:
        send_report_to_discord(
            req.discord_token,
            req.discord_channel_id,
            req.applicant_name,
            req.applicant_email,
            ai_data.get("company_name", req.query),
            target_url,
            pdf_filename
        )
        
    return {"status": "success", "data": ai_data, "pdf_file": pdf_filename}
@app.get("/api/download/{filename}")
def download_pdf(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename, media_type="application/pdf", filename="Company_Research_Report.pdf")
    raise HTTPException(status_code=404, detail="File not found")