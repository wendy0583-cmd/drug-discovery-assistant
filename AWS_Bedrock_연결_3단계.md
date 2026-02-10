# 🚀 AWS Bedrock 연결 - 3단계로 완성

## ✅ 현재 상태
- 앱은 이미 Bedrock을 사용하도록 설정되어 있습니다
- AWS 자격 증명만 설정하면 바로 작동합니다!

---

## 1단계: AWS 자격 증명 설정 (2분)

### 방법 A: AWS Configure 사용 (가장 쉬움)

터미널에서 실행:
```bash
aws configure --profile drug-discovery
```

**입력 정보 (관리자에게 요청):**
```
AWS Access Key ID [None]: AKIA...
AWS Secret Access Key [None]: wJalr...
Default region name [None]: us-west-2
Default output format [None]: json
```

**프로파일 활성화:**
```bash
export AWS_PROFILE=drug-discovery
```

### 방법 B: 환경 변수 사용 (임시)

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="wJalr..."
export AWS_DEFAULT_REGION="us-west-2"
```

---

## 2단계: Bedrock 모델 액세스 활성화 (1분)

1. **AWS Console 접속**: https://console.aws.amazon.com/
2. **Bedrock 검색**: 상단 검색창에 "Bedrock" 입력
3. **Model access 클릭**: 왼쪽 메뉴에서 선택
4. **Manage model access 클릭**
5. **다음 모델 체크:**
   ```
   ✅ Anthropic Claude 4 Sonnet
   ✅ Anthropic Claude 3.7 Sonnet
   ✅ Anthropic Claude 3.5 Sonnet
   ✅ Anthropic Claude 3.5 Haiku
   ```
6. **Request model access 클릭**
7. **승인 대기** (보통 즉시 승인됨)

---

## 3단계: 연결 테스트 (1분)

### 테스트 스크립트 실행:
```bash
cd 25_drug_discovery_agent
source .venv/bin/activate
python test_bedrock_connection.py
```

**성공 시 출력:**
```
✅ AWS 계정: 123456789012
✅ 사용자 ARN: arn:aws:iam::...
✅ Bedrock 클라이언트 생성 완료
✅ Bedrock 연결 성공!

[응답 내용]
KRAS G12C inhibitors have emerged as a promising therapeutic...
```

### 앱에서 테스트:
1. 브라우저에서 `http://localhost:8501` 접속
2. 질문 입력:
   ```
   HER2 억제제에 대한 최근 연구를 찾아주세요
   ```
3. AI가 응답하면 성공! 🎉

---

## 🔧 문제 해결

### ❌ "AWS 자격 증명을 찾을 수 없습니다"

**해결:**
```bash
# 자격 증명 확인
aws configure list

# 없으면 다시 설정
aws configure --profile drug-discovery
export AWS_PROFILE=drug-discovery
```

### ❌ "AccessDeniedException"

**원인:** Bedrock 모델 액세스 권한 없음

**해결:**
1. AWS Console → Bedrock → Model access
2. Claude 모델들이 "Access granted" 상태인지 확인
3. 아니면 "Request model access" 클릭

### ❌ "You don't have access to the model"

**원인:** IAM 권한 부족

**해결:** 관리자에게 다음 권한 요청
```json
{
    "Effect": "Allow",
    "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
    ],
    "Resource": "arn:aws:bedrock:us-west-2::foundation-model/*"
}
```

---

## 📋 IAM 권한 요청서 (관리자 제출용)

**요청 목적:**
신약 개발 연구 어시스턴트 AI 시스템 구축 및 운영

**필요 권한:**
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

**예상 비용:** 월 $50-200 (사용량에 따라)

---

## ✅ 설정 완료 체크리스트

- [ ] AWS 자격 증명 설정 완료
- [ ] AWS_PROFILE 환경 변수 설정
- [ ] Bedrock 모델 액세스 승인
- [ ] test_bedrock_connection.py 테스트 성공
- [ ] 앱에서 질문 응답 확인

---

## 🎉 완료!

모든 단계가 완료되면:
- ✅ 5개 과학 데이터베이스 검색 가능
- ✅ AI 기반 논문 분석
- ✅ 종합 보고서 PDF 생성
- ✅ 인용 정보 분석

**문제가 계속되면:**
- `완전한_설정_가이드.md` 참조
- 터미널 로그 확인
- AWS CloudWatch Logs 확인