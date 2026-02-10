# 💊 신약 개발 연구 어시스턴트

AI 기반 통합 과학 데이터베이스 분석 플랫폼

## 🌟 주요 기능

- **5개 과학 데이터베이스 통합**: arXiv, PubMed, Google Scholar, ChEMBL, ClinicalTrials.gov
- **AI 기반 분석**: AWS Bedrock (Nova Micro, Claude 시리즈)
- **빠른 보고서 생성**: 5분 이내 간단한 보고서
- **인용 분석**: Google Scholar를 통한 논문 영향력 측정
- **PDF 보고서**: 종합 분석 결과 다운로드

## 🚀 빠른 시작

### 1. 설치
```bash
cd 25_drug_discovery_agent
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. AWS 설정
```bash
aws configure --profile drug-discovery
export AWS_PROFILE=drug-discovery
```

### 3. 실행
```bash
streamlit run application/app.py
```

### 4. 접속
```
http://localhost:8501
```

## 📊 데이터 소스

- ✅ **arXiv** - 과학 논문 (프리프린트)
- ✅ **PubMed** - 생의학 문헌 (동료심사)
- ✅ **Google Scholar** - 학술 논문 + 인용정보
- ✅ **ChEMBL** - 생물활성 분자
- ✅ **ClinicalTrials.gov** - 임상시험

## 💡 사용 예시

```
"HER2 억제제에 대한 최근 연구를 찾아주세요"
"알츠하이머 치료제 개발 현황을 알려주세요"
"KRAS G12C 관련 임상시험 정보를 요약해주세요"
```

## 🔧 설정

자세한 설정 방법은 다음 문서를 참조하세요:
- `빠른_시작_가이드.md` - 5분 완성
- `AWS_Bedrock_연결_3단계.md` - Bedrock 연결
- `완전한_설정_가이드.md` - 상세 가이드

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

## 👥 기여자

- AWS AI/ML Workshop KR 기반
- Strands Agents SDK 사용
