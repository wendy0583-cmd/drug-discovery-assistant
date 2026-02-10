import streamlit as st
import chat
import logging
import sys
import requests
import random
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,  # Default to INFO level
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("streamlit")

# title
st.set_page_config(
    page_title='신약 개발 에이전트',
    page_icon='💊',
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

with st.sidebar:
    st.title("🔬 메뉴")
    
    st.markdown(
        "**Strands Agent SDK**를 사용하여 다양한 유형의 에이전트를 구현합니다. "
        "자세한 코드는 [Github](https://github.com/hsr87/drug-discovery-agent)을 참조하세요."
    )

    # model selection box
    modelName = st.selectbox(
        '🖊️ 분석에 사용할 기반 모델을 선택하세요',
        ('Nova Micro', 'Claude 4 Sonnet', 'Claude 3.7 Sonnet', 'Claude 3.5 Sonnet', 'Claude 3.5 Haiku'), index=0
    )
    
    # extended thinking of claude 3.7 sonnet
    select_reasoning = st.checkbox('🧠 추론 모드 (Claude 4 Sonnet 및 Claude 3.7 Sonnet만 지원)', value=False)
    reasoningMode = 'Enable' if select_reasoning and modelName in ["Claude 4 Sonnet", "Claude 3.7 Sonnet"] else 'Disable'
    logger.info(f"reasoningMode: {reasoningMode}")
    
    # 빠른 모드 옵션 (기본 체크)
    fast_mode = st.checkbox('⚡ 빠른 모드 (5분 이내, 간단한 보고서)', value=True)
    st.markdown('<small style="color:#666;">빠른 모드: 각 DB당 3-5개 결과, 직접적인 답변</small>', unsafe_allow_html=True)

    chat.update(modelName, reasoningMode)
    
    clear_button = st.button("🗑️ 대화 초기화", key="clear")
    
    st.markdown("---")
    
    # 데이터 소스 정보
    st.markdown("### 📊 연결된 데이터 소스")
    data_sources = [
        {"name": "arXiv", "icon": "📚", "desc": "과학 논문", "status": "✅"},
        {"name": "PubMed", "icon": "🏥", "desc": "생의학 문헌", "status": "✅"},
        {"name": "Google Scholar", "icon": "🎓", "desc": "학술 논문 + 인용정보", "status": "✅"},
        {"name": "ChEMBL", "icon": "🧪", "desc": "생물활성 분자", "status": "✅"},
        {"name": "ClinicalTrials.gov", "icon": "🔬", "desc": "임상시험", "status": "✅"}
    ]
    
    # 웹 검색 상태 확인
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        # Google Search 상태
        if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID"):
            data_sources.append({"name": "Google Search", "icon": "🌐", "desc": "웹 검색 (무료 100회/일)", "status": "✅"})
        else:
            data_sources.append({"name": "Google Search", "icon": "🌐", "desc": "웹 검색 (무료 100회/일)", "status": "❌"})
            
        # Tavily 상태
        if os.getenv("TAVILY_API_KEY") and os.getenv("TAVILY_API_KEY") != "YOUR_API_KEY_HERE":
            data_sources.append({"name": "Tavily", "icon": "🔍", "desc": "AI 웹 검색 (1000회/월)", "status": "✅"})
        else:
            data_sources.append({"name": "Tavily", "icon": "🔍", "desc": "AI 웹 검색 (1000회/월)", "status": "❌"})
    except:
        data_sources.extend([
            {"name": "Google Search", "icon": "🌐", "desc": "웹 검색 (무료 100회/일)", "status": "❌"},
            {"name": "Tavily", "icon": "🔍", "desc": "AI 웹 검색 (1000회/월)", "status": "❌"}
        ])
    
    for source in data_sources:
        status_color = "#28a745" if source["status"] == "✅" else "#dc3545"
        st.markdown(f'<div style="font-size:13px; margin:2px 0;">{source["icon"]} <strong>{source["name"]}</strong> - {source["desc"]} <span style="color:{status_color};">{source["status"]}</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 사용 팁
    st.markdown("### 💡 사용 팁")
    st.markdown("""
    - 구체적인 타겟 단백질명을 언급하세요
    - '최신 연구', '임상시험', '화합물' 등 키워드 활용
    - Google Scholar로 인용수가 높은 논문 확인 가능
    - 보고서 생성을 요청하면 PDF로 다운로드 가능
    - 5개 과학 DB만으로도 완전한 연구 분석 가능
    """)
    
    # 웹 검색 설정 안내
    st.markdown("### 🌐 웹 검색 활성화 (선택사항)")
    st.markdown("""
    <div style="font-size:12px; background-color:#f8f9fa; padding:10px; border-radius:5px;">
    <strong>🆓 Google Search (권장)</strong><br>
    • 하루 100회 무료<br>
    • <a href="https://developers.google.com/custom-search/v1/overview" target="_blank">Google Custom Search API</a> 설정<br>
    • GOOGLE_API_KEY, GOOGLE_CSE_ID 필요<br><br>
    
    <strong>💰 Tavily (고급)</strong><br>
    • 월 1000회 무료<br>
    • <a href="https://tavily.com" target="_blank">Tavily.com</a> 가입<br>
    • TAVILY_API_KEY 필요
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 20px 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0; font-size: 28px;">💊 신약 개발 연구 어시스턴트</h1>
    <p style="color: #f8f9fa; margin: 5px 0 0 0; font-size: 14px;">AI 기반 통합 과학 데이터베이스 분석 플랫폼</p>
</div>
""", unsafe_allow_html=True)

# 플랫폼 소개
st.markdown("""
<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #007bff;">
    <p style="margin: 0; font-size: 14px; color: #495057;">
        <strong>🔬 전문 연구진을 위한 AI 어시스턴트</strong><br>
        arXiv, PubMed, ChEMBL, ClinicalTrials.gov 등 주요 과학 데이터베이스를 실시간으로 통합 분석하여 
        신약 개발 연구에 필요한 종합적인 인사이트를 제공합니다.
    </p>
</div>
""", unsafe_allow_html=True)

# 예시 질문 섹션
st.markdown('<p style="font-size:18px; font-weight:bold;">💡 예시 질문들</p>', unsafe_allow_html=True)
example_questions = [
    "HER2에 대한 최신 연구와 관련 화합물 보고서를 생성해주세요",
    "BRCA1 억제제에 대한 최근 연구 논문을 찾아주세요", 
    "알츠하이머 치료제 개발 현황을 알려주세요"
]

# 3개 컬럼으로 예시 질문 배치
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎯 " + example_questions[0][:20] + "...", key="q1", help=example_questions[0]):
        st.session_state.selected_question = example_questions[0]

with col2:
    if st.button("🔬 " + example_questions[1][:20] + "...", key="q2", help=example_questions[1]):
        st.session_state.selected_question = example_questions[1]

with col3:
    if st.button("🧠 " + example_questions[2][:20] + "...", key="q3", help=example_questions[2]):
        st.session_state.selected_question = example_questions[2]

# 핫한 타겟 화합물 섹션
st.markdown('<p style="font-size:18px; font-weight:bold;">🔥 현재 주목받는 타겟</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:12px; color:#666; margin-bottom:15px;">* 기준: FDA 승인 현황, 임상시험 수, 시장 규모 (출처: ClinicalTrials.gov, BioPharma Dive, Nature Reviews Drug Discovery 2024)</p>', unsafe_allow_html=True)

hot_targets = [
    {"name": "GLP-1 수용체 작용제", "trend": "📈", "description": "당뇨병 및 비만 치료", "market": "$50B+"},
    {"name": "KRAS G12C 억제제", "trend": "🚀", "description": "폐암 표적치료", "market": "$15B+"},
    {"name": "PD-1/PD-L1 항체", "trend": "🔥", "description": "면역항암치료", "market": "$30B+"}
]

# 3개 컬럼으로 핫한 타겟 표시
col1, col2, col3 = st.columns(3)
for i, target in enumerate(hot_targets):
    col = [col1, col2, col3][i]
    with col:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 12px;
            border-radius: 10px;
            margin: 3px 0;
            border-left: 4px solid #007bff;
            font-size: 13px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="font-weight:bold; color:#007bff;">{target['trend']} {target['name']}</div>
            <div style="color: #666; margin: 4px 0;">{target['description']}</div>
            <div style="color: #28a745; font-weight:bold; font-size:11px;">시장규모: {target['market']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")  

if clear_button is True:
    chat.initiate()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False

# Display chat messages from history on app rerun
def display_chat_messages():
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "images" in message:                
                for url in message["images"]:
                    logger.info(f"url: {url}")

                    file_name = url[url.rfind('/') + 1:]
                    st.image(url, caption=file_name, use_container_width=True)
            st.markdown(message["content"])

display_chat_messages()

# Greet user
if not st.session_state.greetings:
    with st.chat_message("assistant"):
        intro = "Amazon Bedrock 기반 신약 개발 에이전트를 사용해 주셔서 감사합니다. 편안한 대화를 즐기실 수 있습니다."
        st.markdown(intro)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True

if clear_button or "messages" not in st.session_state:
    st.session_state.messages = []        
    st.session_state.greetings = False
    st.rerun()

    chat.clear_chat_history()
       
# Always show the chat input
if prompt := st.chat_input("메시지를 입력하세요."):
    with st.chat_message("user"):  # display user message in chat message container
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})  # add user message to chat history
    prompt = prompt.replace('"', "").replace("'", "")
    logger.info(f"prompt: {prompt}")

    with st.chat_message("assistant"):
        sessionState = ""
        chat.references = []
        chat.image_url = []
        response = chat.run_multi_agent_system(prompt, "Enable", st)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 예시 질문이 선택된 경우 자동으로 실행
if "selected_question" in st.session_state and st.session_state.selected_question:
    prompt = st.session_state.selected_question
    st.session_state.selected_question = None  # 초기화
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        sessionState = ""
        chat.references = []
        chat.image_url = []
        response = chat.run_multi_agent_system(prompt, "Enable", st)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
