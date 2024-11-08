from typing import List, Optional, Dict
import requests
import xml.etree.ElementTree as ET
import time
from pydantic import BaseModel, Field
from fastapi import HTTPException

class Article(BaseModel):
    pmid: str = Field(..., description="PubMed ID")
    title: str = Field(..., description="Article title")
    authors: List[str] = Field(default=[], description="List of authors")
    publication_date: str = Field(..., description="Publication date")
    abstract: Optional[str] = Field(None, description="Article abstract")

class ArticleResponse(BaseModel):
    total_results: int = Field(..., description="Total number of results found")
    articles: List[Article] = Field(..., description="List of articles")

class PubMedClient:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.search_url = f"{self.base_url}/esearch.fcgi"
        self.fetch_url = f"{self.base_url}/efetch.fcgi"
        self.db = "pubmed"

    def _make_request(self, url: str, params: Dict) -> Optional[str]:
        """Make HTTP request to PubMed API with rate limiting"""
        try:
            time.sleep(0.34)  # Rate limit: max 3 requests per second
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"PubMed API error: {str(e)}")

    def _parse_article_details(self, xml_text: str) -> List[Article]:
        """Parse article details from XML response"""
        root = ET.fromstring(xml_text)
        articles = []

        for article_elem in root.findall(".//PubmedArticle"):
            # Extract PMID
            pmid = article_elem.find(".//PMID").text

            # Extract title
            title_elem = article_elem.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No title available"

            # Extract authors
            authors = []
            author_list = article_elem.findall(".//Author")
            for author in author_list:
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                if last_name is not None and fore_name is not None:
                    authors.append(f"{fore_name.text} {last_name.text}")

            # Extract publication date
            pub_date_elem = article_elem.find(".//PubDate")
            pub_date = "Not available"
            if pub_date_elem is not None:
                year = pub_date_elem.find("Year")
                month = pub_date_elem.find("Month")
                day = pub_date_elem.find("Day")
                pub_date = f"{year.text if year is not None else ''}"
                if month is not None:
                    pub_date += f"/{month.text}"
                if day is not None:
                    pub_date += f"/{day.text}"

            # Extract abstract
            abstract_elem = article_elem.find(".//Abstract/AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else None

            articles.append(Article(
                pmid=pmid,
                title=title,
                authors=authors,
                publication_date=pub_date,
                abstract=abstract
            ))

        return articles

    async def search_articles(self, query: str, max_results: int) -> ArticleResponse:
        """Search articles and fetch their details"""
        # Search for articles
        search_params = {
            "db": self.db,
            "term": query,
            "retmax": max_results,
            "retmode": "xml"
        }
        
        search_response = self._make_request(self.search_url, search_params)
        if not search_response:
            return ArticleResponse(total_results=0, articles=[])

        # Parse search results to get PMIDs
        search_root = ET.fromstring(search_response)
        pmids = [id_elem.text for id_elem in search_root.findall(".//Id")]
        total_results = int(search_root.find(".//Count").text)

        if not pmids:
            return ArticleResponse(total_results=total_results, articles=[])

        # Fetch article details
        fetch_params = {
            "db": self.db,
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        fetch_response = self._make_request(self.fetch_url, fetch_params)
        if not fetch_response:
            return ArticleResponse(total_results=total_results, articles=[])

        articles = self._parse_article_details(fetch_response)
        return ArticleResponse(total_results=total_results, articles=articles)