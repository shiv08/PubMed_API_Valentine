from fastapi import FastAPI, HTTPException, Query, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import datetime
from pubmed_client import PubMedClient, ArticleResponse

# Initialize FastAPI app
app = FastAPI(
    title="PubMed WebApp",
    description="A web interface for searching PubMed articles",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize PubMed client
pubmed_client = PubMedClient()

# Root endpoint for API documentation
@app.get("/")
async def home(request: Request):
    """
    Render the home page with search form
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None, "search_type": None}
    )

@app.get("/api")
async def api_root():
    """
    API root endpoint showing available endpoints
    """
    return {
        "message": "Welcome to PubMed API Service",
        "available_endpoints": [
            "/api/search/date",
            "/api/search/title",
            "/api/search/abstract"
        ],
        "documentation": "/docs"
    }

# API endpoints
@app.get("/api/search/date", response_model=ArticleResponse)
async def search_by_date(
    start_date: str = Query(..., description="Start date (YYYY/MM/DD)"),
    end_date: str = Query(..., description="End date (YYYY/MM/DD)"),
    max_results: int = Query(default=10, le=100, description="Maximum number of results to return")
):
    """
    Search PubMed articles by publication date range.
    """
    try:
        datetime.strptime(start_date, '%Y/%m/%d')
        datetime.strptime(end_date, '%Y/%m/%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Dates must be in format 'YYYY/MM/DD'")

    query = f"(\"{start_date}\"[Date - Publication] : \"{end_date}\"[Date - Publication])"
    return await pubmed_client.search_articles(query, max_results)

@app.get("/api/search/title", response_model=ArticleResponse)
async def search_by_title(
    keywords: str = Query(..., description="Keywords to search in titles"),
    max_results: int = Query(default=10, le=100, description="Maximum number of results to return")
):
    """
    Search PubMed articles by title keywords.
    """
    query = f"{keywords}[Title]"
    return await pubmed_client.search_articles(query, max_results)

@app.get("/api/search/abstract", response_model=ArticleResponse)
async def search_by_abstract(
    keywords: str = Query(..., description="Keywords to search in abstracts"),
    max_results: int = Query(default=10, le=100, description="Maximum number of results to return")
):
    """
    Search PubMed articles by abstract keywords.
    """
    query = f"{keywords}[Abstract]"
    return await pubmed_client.search_articles(query, max_results)

# Web interface routes
@app.post("/search")
async def search(
    request: Request,
    search_type: str = Form(...),
    keywords: str = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    max_results: int = Form(10)
):
    """
    Handle search form submission and display results
    """
    try:
        if search_type == "title":
            if not keywords:
                raise HTTPException(status_code=400, detail="Keywords are required for title search")
            query = f"{keywords}[Title]"
        elif search_type == "abstract":
            if not keywords:
                raise HTTPException(status_code=400, detail="Keywords are required for abstract search")
            query = f"{keywords}[Abstract]"
        elif search_type == "date":
            if not start_date or not end_date:
                raise HTTPException(status_code=400, detail="Both start and end dates are required")
            # Convert date format from HTML date input (YYYY-MM-DD) to PubMed format (YYYY/MM/DD)
            start_date = start_date.replace('-', '/')
            end_date = end_date.replace('-', '/')
            query = f"(\"{start_date}\"[Date - Publication] : \"{end_date}\"[Date - Publication])"
        else:
            raise HTTPException(status_code=400, detail="Invalid search type")

        results = await pubmed_client.search_articles(query, max_results)
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": results.articles,
                "total_results": results.total_results,
                "search_type": search_type,
                "keywords": keywords,
                "start_date": start_date,
                "end_date": end_date
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e),
                "search_type": search_type,
                "keywords": keywords,
                "start_date": start_date,
                "end_date": end_date
            }
        )

# Optional: Add error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """
    Handle 404 Not Found errors
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": "The requested page was not found",
        },
        status_code=404
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: HTTPException):
    """
    Handle 500 Internal Server Error
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": "An internal server error occurred",
        },
        status_code=500
    )

# Development server configuration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)