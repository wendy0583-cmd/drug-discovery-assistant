#!/usr/bin/env python3
"""
Google Scholar MCP Server
학술 논문 검색 및 인용 정보 제공
"""

import asyncio
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import json
import os
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("google_scholar_mcp")

try:
    from scholarly import scholarly
    SCHOLARLY_AVAILABLE = True
    logger.info("scholarly library imported successfully")
except ImportError:
    SCHOLARLY_AVAILABLE = False
    logger.warning("scholarly library not found. Install with: pip install scholarly")

try:
    mcp = FastMCP(
        name="google_scholar_tools",
    )
    logger.info("Google Scholar MCP server initialized successfully")
except Exception as e:
    err_msg = f"Error: {str(e)}"
    logger.error(f"{err_msg}")

def format_publication_results(publications: list, max_results: int = 10) -> str:
    """Google Scholar 검색 결과를 읽기 쉬운 형태로 포맷"""
    if not publications:
        return "검색 결과가 없습니다."
    
    output = []
    output.append(f"Google Scholar 검색 결과 (최대 {max_results}개):\n")
    
    count = 0
    for pub in publications:
        if count >= max_results:
            break
            
        try:
            title = pub.get('bib', {}).get('title', 'No title')
            authors = pub.get('bib', {}).get('author', 'No authors')
            year = pub.get('bib', {}).get('pub_year', 'No year')
            venue = pub.get('bib', {}).get('venue', 'No venue')
            abstract = pub.get('bib', {}).get('abstract', 'No abstract')
            citations = pub.get('num_citations', 0)
            url = pub.get('pub_url', 'No URL')
            
            output.append(f"{count + 1}. **{title}**")
            output.append(f"   저자: {authors}")
            output.append(f"   발표년도: {year}")
            output.append(f"   학술지/학회: {venue}")
            output.append(f"   인용수: {citations}")
            if abstract and len(abstract) > 10:
                # 초록을 200자로 제한
                abstract_short = abstract[:200] + "..." if len(abstract) > 200 else abstract
                output.append(f"   초록: {abstract_short}")
            if url and url != 'No URL':
                output.append(f"   URL: {url}")
            output.append("")
            
            count += 1
            
        except Exception as e:
            logger.warning(f"Error formatting publication: {e}")
            continue
    
    return "\n".join(output)

@mcp.tool()
async def google_scholar_search(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance"
) -> str:
    """
    Google Scholar에서 학술 논문 검색
    
    Args:
        query: 검색 쿼리 (논문 제목, 저자, 키워드 등)
        max_results: 최대 결과 개수 (기본값: 10, 최대: 20)
        sort_by: 정렬 방식 ("relevance" 또는 "date")
    
    Returns:
        검색 결과 문자열
    """
    if not SCHOLARLY_AVAILABLE:
        return "scholarly 라이브러리가 설치되지 않았습니다. 'pip install scholarly' 명령으로 설치해주세요."
    
    try:
        # 결과 개수 제한
        max_results = min(max_results, 20)
        
        logger.info(f"Searching Google Scholar for: {query}")
        
        # Google Scholar 검색 실행
        search_query = scholarly.search_pubs(query)
        
        publications = []
        count = 0
        
        for pub in search_query:
            if count >= max_results:
                break
            try:
                # 상세 정보 가져오기 (시간이 오래 걸릴 수 있음)
                filled_pub = scholarly.fill(pub)
                publications.append(filled_pub)
                count += 1
            except Exception as e:
                logger.warning(f"Error filling publication details: {e}")
                # 기본 정보만 사용
                publications.append(pub)
                count += 1
        
        return format_publication_results(publications, max_results)
        
    except Exception as e:
        error_msg = f"Google Scholar 검색 오류: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def google_scholar_author_search(
    author_name: str,
    max_results: int = 5
) -> str:
    """
    Google Scholar에서 특정 저자의 논문 검색
    
    Args:
        author_name: 저자 이름
        max_results: 최대 결과 개수 (기본값: 5, 최대: 10)
    
    Returns:
        저자의 논문 목록
    """
    if not SCHOLARLY_AVAILABLE:
        return "scholarly 라이브러리가 설치되지 않았습니다."
    
    try:
        max_results = min(max_results, 10)
        
        logger.info(f"Searching Google Scholar author: {author_name}")
        
        # 저자 검색
        search_query = scholarly.search_author(author_name)
        
        try:
            # 첫 번째 저자 선택
            author = next(search_query)
            filled_author = scholarly.fill(author)
            
            output = []
            output.append(f"저자: {filled_author.get('name', 'Unknown')}")
            output.append(f"소속: {filled_author.get('affiliation', 'Unknown')}")
            output.append(f"총 인용수: {filled_author.get('citedby', 0)}")
            output.append(f"h-index: {filled_author.get('hindex', 0)}")
            output.append("")
            output.append("주요 논문:")
            
            publications = filled_author.get('publications', [])[:max_results]
            
            for i, pub in enumerate(publications, 1):
                try:
                    filled_pub = scholarly.fill(pub)
                    title = filled_pub.get('bib', {}).get('title', 'No title')
                    year = filled_pub.get('bib', {}).get('pub_year', 'No year')
                    citations = filled_pub.get('num_citations', 0)
                    
                    output.append(f"{i}. {title} ({year}) - 인용수: {citations}")
                except Exception as e:
                    logger.warning(f"Error processing publication: {e}")
                    continue
            
            return "\n".join(output)
            
        except StopIteration:
            return f"저자 '{author_name}'을 찾을 수 없습니다."
        
    except Exception as e:
        error_msg = f"Google Scholar 저자 검색 오류: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def google_scholar_citation_search(
    paper_title: str
) -> str:
    """
    특정 논문의 인용 정보 검색
    
    Args:
        paper_title: 논문 제목
    
    Returns:
        논문의 인용 정보
    """
    if not SCHOLARLY_AVAILABLE:
        return "scholarly 라이브러리가 설치되지 않았습니다."
    
    try:
        logger.info(f"Searching citation info for: {paper_title}")
        
        # 논문 검색
        search_query = scholarly.search_pubs(paper_title)
        
        try:
            # 첫 번째 결과 선택
            pub = next(search_query)
            filled_pub = scholarly.fill(pub)
            
            title = filled_pub.get('bib', {}).get('title', 'No title')
            authors = filled_pub.get('bib', {}).get('author', 'No authors')
            year = filled_pub.get('bib', {}).get('pub_year', 'No year')
            venue = filled_pub.get('bib', {}).get('venue', 'No venue')
            citations = filled_pub.get('num_citations', 0)
            url = filled_pub.get('pub_url', 'No URL')
            
            output = []
            output.append(f"논문 제목: {title}")
            output.append(f"저자: {authors}")
            output.append(f"발표년도: {year}")
            output.append(f"학술지/학회: {venue}")
            output.append(f"총 인용수: {citations}")
            if url and url != 'No URL':
                output.append(f"URL: {url}")
            
            # 인용한 논문들 (최대 5개)
            if 'citedby_url' in filled_pub:
                output.append("\n최근 인용 논문들:")
                try:
                    citing_papers = scholarly.search_pubs(f"cites:{filled_pub['scholar_id']}")
                    for i, citing_paper in enumerate(citing_papers):
                        if i >= 5:  # 최대 5개만
                            break
                        citing_title = citing_paper.get('bib', {}).get('title', 'No title')
                        citing_year = citing_paper.get('bib', {}).get('pub_year', 'No year')
                        output.append(f"{i+1}. {citing_title} ({citing_year})")
                except Exception as e:
                    logger.warning(f"Error getting citing papers: {e}")
            
            return "\n".join(output)
            
        except StopIteration:
            return f"논문 '{paper_title}'을 찾을 수 없습니다."
        
    except Exception as e:
        error_msg = f"Google Scholar 인용 검색 오류: {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    mcp.run()