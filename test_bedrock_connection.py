#!/usr/bin/env python3
"""
AWS Bedrock 연결 테스트 스크립트
"""

import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

def test_bedrock_connection():
    """Bedrock 연결 및 모델 테스트"""
    
    print("=" * 60)
    print("AWS Bedrock 연결 테스트")
    print("=" * 60)
    
    # 1. AWS 자격 증명 확인
    print("\n[1단계] AWS 자격 증명 확인...")
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS 계정: {identity['Account']}")
        print(f"✅ 사용자 ARN: {identity['Arn']}")
    except NoCredentialsError:
        print("❌ AWS 자격 증명을 찾을 수 없습니다.")
        print("\n해결 방법:")
        print("  aws configure --profile drug-discovery")
        print("  export AWS_PROFILE=drug-discovery")
        return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False
    
    # 2. Bedrock 클라이언트 생성
    print("\n[2단계] Bedrock 클라이언트 생성...")
    try:
        # us-west-2 리전 사용 (Claude 모델 지원)
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-west-2"
        )
        print("✅ Bedrock 클라이언트 생성 완료 (us-west-2)")
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False
    
    # 3. 사용 가능한 모델 확인
    print("\n[3단계] 사용 가능한 모델 확인...")
    try:
        bedrock_client = boto3.client(
            service_name="bedrock",
            region_name="us-west-2"
        )
        models = bedrock_client.list_foundation_models()
        
        claude_models = [
            m for m in models.get('modelSummaries', [])
            if 'claude' in m['modelId'].lower()
        ]
        
        if claude_models:
            print(f"✅ Claude 모델 {len(claude_models)}개 발견:")
            for model in claude_models[:5]:  # 처음 5개만 표시
                print(f"   - {model['modelId']}")
        else:
            print("⚠️  Claude 모델을 찾을 수 없습니다.")
    except Exception as e:
        print(f"⚠️  모델 목록 조회 실패: {e}")
    
    # 4. Claude 모델 테스트
    print("\n[4단계] Claude 3.5 Haiku 모델 테스트...")
    
    # 테스트할 모델 ID (가장 빠르고 저렴한 모델)
    model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    
    # 테스트 프롬프트
    prompt = "Summarize recent research trends on KRAS G12C inhibitors in one sentence."
    
    # 요청 본문 (Claude 3 형식)
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        print(f"모델: {model_id}")
        print(f"프롬프트: {prompt}")
        print("\n응답 대기 중...")
        
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body)
        )
        
        # 응답 파싱
        result = json.loads(response["body"].read())
        
        print("\n" + "=" * 60)
        print("✅ Bedrock 연결 성공!")
        print("=" * 60)
        print("\n[응답 내용]")
        print(result["content"][0]["text"])
        print("\n" + "=" * 60)
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        print(f"\n❌ 모델 호출 실패")
        print(f"오류 코드: {error_code}")
        print(f"오류 메시지: {error_message}")
        
        if error_code == "AccessDeniedException":
            print("\n해결 방법:")
            print("1. AWS Console → Bedrock → Model access")
            print("2. Claude 모델들에 대한 액세스 요청")
            print("3. 또는 IAM 권한 확인 (bedrock:InvokeModel)")
        elif error_code == "ResourceNotFoundException":
            print("\n해결 방법:")
            print("1. 모델 ID가 올바른지 확인")
            print("2. 리전이 us-west-2인지 확인")
        
        return False
        
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        return False

def test_all_claude_models():
    """모든 Claude 모델 테스트"""
    
    print("\n" + "=" * 60)
    print("모든 Claude 모델 테스트")
    print("=" * 60)
    
    models = [
        "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        "us.anthropic.claude-4-sonnet-20250219-v1:0"
    ]
    
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2"
    )
    
    prompt = "Say 'Hello' in one word."
    
    for model_id in models:
        print(f"\n테스트 중: {model_id}")
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 10,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = bedrock.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body)
            )
            
            result = json.loads(response["body"].read())
            print(f"✅ 성공: {result['content'][0]['text']}")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            print(f"❌ 실패: {error_code}")
        except Exception as e:
            print(f"❌ 오류: {str(e)[:50]}")

if __name__ == "__main__":
    print("\n🚀 AWS Bedrock 연결 테스트 시작\n")
    
    # 기본 연결 테스트
    success = test_bedrock_connection()
    
    if success:
        # 추가 테스트 (선택사항)
        response = input("\n모든 Claude 모델을 테스트하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            test_all_claude_models()
    
    print("\n✅ 테스트 완료\n")
