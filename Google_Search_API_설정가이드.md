# Google Custom Search API 설정 가이드

## 🆓 무료 웹 검색 기능 활성화 (하루 100회)

### 1단계: Google Cloud Console 설정

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/ 방문
   - Google 계정으로 로그인

2. **새 프로젝트 생성** (기존 프로젝트가 있다면 생략)
   - 상단의 프로젝트 선택 드롭다운 클릭
   - "새 프로젝트" 선택
   - 프로젝트 이름 입력 (예: "drug-discovery-search")

3. **Custom Search API 활성화**
   - 좌측 메뉴에서 "API 및 서비스" > "라이브러리" 선택
   - "Custom Search API" 검색
   - "Custom Search API" 클릭 후 "사용" 버튼 클릭

4. **API 키 생성**
   - 좌측 메뉴에서 "API 및 서비스" > "사용자 인증 정보" 선택
   - "사용자 인증 정보 만들기" > "API 키" 선택
   - 생성된 API 키 복사 (나중에 사용)

### 2단계: Custom Search Engine 생성

1. **Programmable Search Engine 접속**
   - https://programmablesearchengine.google.com/ 방문
   - Google 계정으로 로그인

2. **새 검색 엔진 생성**
   - "시작하기" 또는 "Add" 버튼 클릭
   - **검색할 사이트**: `*` (전체 웹 검색을 위해)
   - **검색 엔진 이름**: "Drug Discovery Search" (원하는 이름)
   - "만들기" 버튼 클릭

3. **검색 엔진 ID 확인**
   - 생성된 검색 엔진 클릭
   - "설정" 탭에서 "검색 엔진 ID" 복사 (나중에 사용)

4. **전체 웹 검색 활성화**
   - "설정" 탭에서 "검색 기능" 섹션 찾기
   - "전체 웹 검색" 토글을 ON으로 설정

### 3단계: 환경 변수 설정

1. **프로젝트의 .env 파일 열기**
   ```bash
   cd 25_drug_discovery_agent
   nano .env
   ```

2. **API 키 정보 입력**
   ```env
   GOOGLE_API_KEY="여기에_1단계에서_복사한_API_키_입력"
   GOOGLE_CSE_ID="여기에_2단계에서_복사한_검색엔진_ID_입력"
   ```

3. **파일 저장 후 앱 재시작**
   ```bash
   # 현재 실행 중인 앱 종료 (Ctrl+C)
   streamlit run application/app.py
   ```

### 4단계: 테스트

1. **브라우저에서 http://localhost:8501 접속**
2. **사이드바에서 "Google Search" 상태가 ✅ 인지 확인**
3. **"최신 GLP-1 수용체 작용제 뉴스를 검색해주세요" 같은 질문으로 테스트**

## 📊 사용량 및 제한사항

- **무료 할당량**: 하루 100회 검색
- **추가 사용량**: 1,000회당 $5 (필요시)
- **응답 속도**: 평균 2-3초
- **검색 범위**: 전체 웹 (한국어/영어 모두 지원)

## 🔧 문제 해결

### API 키 오류
```
Error: The provided API key is invalid
```
- Google Cloud Console에서 API 키 재확인
- Custom Search API가 활성화되었는지 확인

### 검색 엔진 ID 오류
```
Error: Invalid search engine ID
```
- Programmable Search Engine에서 검색 엔진 ID 재확인
- 전체 웹 검색이 활성화되었는지 확인

### 할당량 초과
```
Error: Quota exceeded for quota metric
```
- 하루 100회 제한 초과
- 내일 다시 시도하거나 유료 플랜 고려

## 💡 팁

1. **효율적 사용**: 구체적인 검색어 사용으로 정확한 결과 획득
2. **언어 설정**: 한국어 결과가 필요하면 검색어에 "한국어" 추가
3. **백업 옵션**: Tavily API도 함께 설정하면 더 안정적

---
**참고 문서**:
- [Google Custom Search API 공식 문서](https://developers.google.com/custom-search/v1/overview)
- [Programmable Search Engine 가이드](https://developers.google.com/custom-search/docs/tutorial/creatingcse)