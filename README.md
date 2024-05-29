# lambda_and_langchain

#### ✅ lambda layer 구성
lambda에서 단일 layer 업로드 시, 50mb 용량 제한이 있다.
이에 langchain.zip 에서 numpy 모듈을 제거하여 50mb 이하로 layer size를 조정하고, numpy 관련 모듈 추가를 위해, AWSSDKPandas 레이어를 추가.

- langchain: https://drive.google.com/file/d/1MvLnK4QnbaFEFcx031h_yxu8SSiBvDik/view?usp=drive_link
- AWSSDKPandas

![lambda layer 구성](https://github.com/i-am-shuan/lambda_and_langchain/assets/161431602/4753efe8-c3ff-4f20-8980-b63c76e3c19f)


#### ✅ Lambda Runtime 실행 환경
랭체인 모듈 내부의 바이너리 디펜던시로 인해, Lambda Runtime 실행 환경은 아래와 같이 구성되어야 한다. 
- Python 3.11
- Architecture X86_64


---

#### ✅ AWS GenAI Samples
- https://github.com/aws-samples/generative-ai-demo-using-amazon-sagemaker-jumpstart-kr/tree/main/blogs/multi-rag-and-multi-region-llm-for-chatbot
