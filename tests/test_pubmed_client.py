import pytest
from pubmed_client import PubMedClient
from datetime import datetime, timedelta

@pytest.fixture
def client():
    return PubMedClient()

async def test_search_by_title(client):
    keywords = "cancer"
    max_results = 5
    response = await client.search_articles(f"{keywords}[Title]", max_results)
    
    assert response.total_results > 0
    assert len(response.articles) <= max_results
    for article in response.articles:
        assert article.pmid is not None
        assert article.title is not None

async def test_search_by_date(client):
    end_date = datetime.now().strftime('%Y/%m/%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y/%m/%d')
    max_results = 5
    
    query = f"(\"{start_date}\"[Date - Publication] : \"{end_date}\"[Date - Publication])"
    response = await client.search_articles(query, max_results)
    
    assert response.total_results > 0
    assert len(response.articles) <= max_results

async def test_search_by_abstract(client):
    keywords = "covid"
    max_results = 5
    response = await client.search_articles(f"{keywords}[Abstract]", max_results)
    
    assert response.total_results > 0
    assert len(response.articles) <= max_results
    assert any(article.abstract is not None for article in response.articles)