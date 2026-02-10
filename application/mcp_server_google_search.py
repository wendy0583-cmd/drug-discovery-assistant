#!/usr/bin/env python3
"""
Google Custom Search MCP Server
무료 웹검색 기능 (하루 100회 제한)
"""

import asyncio
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import json
import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("google_search_mcp")

# Load environment variables from .env file
load_dotenv()

# Google Custom Search API 설정
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    logger.warning("Google Custom Search API 키 또는 CSE ID가 설정되지 않았습니다. 웹 검색이 비활성화됩니다.")

try:
    mcp = FastMCP(
        name="google_search_tools",
    )
    logger.info("Google Search MCP server initialized successfully")
except Exception as e:
    err_msg = f"Error: {str(e)}"
    logger.error(f"{err_msg}")

def format_search_results(results: dict) -> str:
    """Google 검색 결과를 읽기 쉬운 형태로 포맷"""
    if 'items' not in results:
        return "검색 결과가 없습니다."
    
    output = []
    output.append(f"검색 결과 ({len(results['items'])}개):\n")
    
    for i, item in enumerate(results['items'], 1):
        title = item.get('title', 'No title')
        link = item.get('link', 'No link')
        snippet = item.get('snippet', 'No description')
        
        output.append(f"{i}. **{title}**")
        output.append(f"   URL: {link}")
        output.append(f"   요약: {snippet}")
        output.append("")
    
    return "\n".join(output)

@mcp.tool()
async def google_web_search(
    query: str,
    num_results: int = 5,
    language: str = "ko"
) -> str:
    """
    Google Custom Search API를 사용한 웹 검색
    
    Args:
        query: 검색 쿼리
        num_results: 결과 개수 (최대 10개)
        language: 언어 설정 (ko=한국어, en=영어)
    
    Returns:
        검색 결과 문자열
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return "Google Custom Search API가 설정되지 않았습니다. 환경변수 GOOGLE_API_KEY와 GOOGLE_CSE_ID를 설정해주세요."
    
    try:
        # Google Custom Search API 호출
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'q': query,
            'num': min(num_results, 10),
            'lr': f'lang_{language}' if language else None
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        results = response.json()
        return format_search_results(results)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Google Search API 요청 오류: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"google_web_search 오류: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def google_news_search(
    query: str,
    num_results: int = 5,
    language: str = "ko"
) -> str:
    """
    Google Custom Search API를 사용한 뉴스 검색
    
    Args:
        query: 검색 쿼리
        num_results: 결과 개수 (최대 10개)
        language: 언어 설정 (ko=한국어, en=영어)
    
    Returns:
        뉴스 검색 결과 문자열
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return "Google Custom Search API가 설정되지 않았습니다."
    
    try:
        # 뉴스 관련 검색어 추가
        news_query = f"{query} 뉴스 OR news OR 최신"
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'q': news_query,
            'num': min(num_results, 10),
            'lr': f'lang_{language}' if language else None,
            'sort': 'date'  # 날짜순 정렬
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        results = response.json()
        return format_search_results(results)
        
    except Exception as e:
        error_msg = f"google_news_search 오류: {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    mcp.run()