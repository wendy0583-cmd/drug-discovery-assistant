"""
빠른 보고서 생성 모드 (5분 이내)
- 병렬 검색
- 결과 개수 제한
- 간단한 요약
"""

from strands import Agent, tool
from strands.models import BedrockModel
from botocore.config import Config
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("chat_fast")

def get_fast_model():
    """빠른 Nova Micro 모델 사용"""
    model = BedrockModel(
        boto_client_config=Config(
            read_timeout=300,
            connect_timeout=300,
            retries=dict(max_attempts=2, mode="adaptive"),
        ),
        model_id="us.amazon.nova-micro-v1:0",
        max_tokens=2000,  # 짧은 응답
        temperature=0.3,
    )
    return model

@tool
def fast_search_all_databases(query: str, max_results: int = 3) -> str:
    """
    모든 데이터베이스를 병렬로 빠르게 검색
    
    Args:
        query: 검색 쿼리
        max_results: 각 DB당 최대 결과 수 (기본 3개)
    
    Returns:
        통합 검색 결과
    """
    
    results = {
        "arxiv": "검색 중...",
        "pubmed": "검색 중...",
        "chembl": "검색 중...",
        "clinicaltrials": "검색 중..."
    }
    
    # 실제로는 MCP 클라이언트를 사용하여 병렬 검색
    # 여기서는 간단한 구조만 제시
    
    output = f"""
=== 빠른 검색 결과 (각 DB당 최대 {max_results}개) ===

📚 arXiv: {results['arxiv']}
🏥 PubMed: {results['pubmed']}
🧪 ChEMBL: {results['chembl']}
🔬 ClinicalTrials: {results['clinicaltrials']}
"""
    
    return output

@tool
def generate_fast_report(query: str, search_results: str) -> str:
    """
    빠른 보고서 생성 (요약본)
    
    Args:
        query: 원본 질문
        search_results: 검색 결과
    
    Returns:
        간단한 보고서
    """
    
    model = get_fast_model()
    
    prompt = f"""
다음 검색 결과를 바탕으로 1페이지 분량의 간단한 보고서를 작성하세요.

질문: {query}

검색 결과:
{search_results}

보고서 구성:
1. 핵심 요약 (3-5문장)
2. 주요 발견사항 (3-5개 bullet points)
3. 참고문헌 (3-5개)

간결하고 핵심만 담아주세요.
"""
    
    agent = Agent(
        model=model,
        system_prompt="당신은 과학 보고서를 빠르고 간결하게 작성하는 전문가입니다."
    )
    
    response = agent(prompt)
    return str(response)

def run_fast_report(question: str) -> str:
    """
    5분 이내 빠른 보고서 생성
    
    Args:
        question: 사용자 질문
    
    Returns:
        보고서 내용
    """
    
    logger.info(f"빠른 보고서 생성 시작: {question}")
    
    # 1단계: 빠른 검색 (병렬)
    search_results = fast_search_all_databases(question, max_results=3)
    
    # 2단계: 빠른 보고서 생성
    report = generate_fast_report(question, search_results)
    
    logger.info("빠른 보고서 생성 완료")
    
    return report
