# AWS IAM 권한 요청서

## 요청 목적
**신약 개발 연구 어시스턴트 AI 시스템 구축 및 운영**

Amazon Bedrock의 대규모 언어 모델(Claude 시리즈)을 활용하여 과학 문헌, 임상시험 데이터, 분자 데이터베이스를 통합 분석하는 AI 연구 어시스턴트를 개발하고 운영하기 위함입니다.

## 시스템 개요
- **프로젝트명**: 신약 개발 연구 어시스턴트 (Drug Discovery Research Assistant)
- **기술 스택**: Strands Agents SDK + Amazon Bedrock + Streamlit
- **주요 기능**: 
  - arXiv, PubMed, ChEMBL, ClinicalTrials.gov 등 과학 데이터베이스 통합 검색
  - 타겟 단백질, 화합물, 임상시험 정보 종합 분석
  - 전문가 수준의 연구 보고서 자동 생성

## 필요한 AWS 서비스 및 권한

### 1. Amazon Bedrock 권한
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:us-west-2::foundation-model/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                "arn:aws:bedrock:us-west-2::foundation-model/us.anthropic.claude-3-5-haiku-20241022-v1:0",
                "arn:aws:bedrock:us-west-2::foundation-model/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                "arn:aws:bedrock:us-west-2::foundation-model/us.anthropic.claude-4-sonnet-20250219-v1:0"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:GetFoundationModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. 추가 권한 (선택사항)
**CloudWatch Logs** (로깅 및 모니터링용):
```json
{
    "Effect": "Allow",
    "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
    ],
    "Resource": "arn:aws:logs:us-west-2:*:log-group:/aws/bedrock/*"
}
```

## 권한 범위 및 제한사항
- **지역**: us-west-2 (Oregon) 리전으로 제한
- **모델**: Anthropic Claude 시리즈 모델만 사용
- **용도**: 연구 및 개발 목적으로만 사용
- **비용 관리**: 월 사용량 모니터링 필요

## 보안 고려사항
- API 키는 환경변수(.env)로 관리
- 로컬 개발 환경에서만 사용 (프로덕션 배포 시 별도 검토)
- 외부 API 호출 시 rate limiting 적용
- 민감한 의료/연구 데이터는 처리하지 않음

## 예상 사용량
- **일일 API 호출**: 약 100-500회
- **월간 예상 비용**: $50-200 (사용량에 따라 변동)
- **주요 사용 시간**: 업무시간 (9AM-6PM KST)

## 요청자 정보
- **사용자**: [사용자명]
- **부서**: [부서명]
- **용도**: 연구개발/학습목적
- **승인 필요 기간**: [날짜]

## 참고 자료
- [AWS Bedrock 공식 문서](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Claude 모델 가이드](https://docs.anthropic.com/claude/docs)
- [프로젝트 GitHub 리포지토리](https://github.com/aws-samples/aws-ai-ml-workshop-kr)

---
**검토 요청**: 위 권한들이 신약 개발 연구 어시스턴트 시스템 구축에 필요한 최소한의 권한입니다. 보안 정책에 따라 추가 제한이나 조건이 있다면 협의 가능합니다.