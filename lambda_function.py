import json
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, BotoCoreError

from langchain.llms.bedrock import Bedrock
from langchain.retrievers.bedrock import AmazonKnowledgeBasesRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

region = 'us-east-1'
bedrock_client = boto3.client('bedrock-runtime', region_name=region)

def lambda_handler(event, context):
    # 모델 설정
    model_kwargs_claude = {
        "temperature": 0,
        "top_k": 10,
        "max_tokens_to_sample": 3000
    }
    llm = Bedrock(model_id="anthropic.claude-v2:1",
                  model_kwargs=model_kwargs_claude,
                  client=bedrock_client)

    # Retrieve API를 사용한 AmazonKnowledgeBasesRetriever 설정
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="RQ7PKC2IZP",  # 실제 Knowledge Base ID로 교체해야 합니다.
        retrieval_config={
            "vectorSearchConfiguration": {
                "numberOfResults": 4
            }
        }
    )

    # 질문
    query = "By what percentage did AWS revenue grow year-over-year in 2022?"
    try:
        docs = retriever.get_relevant_documents(query=query)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving documents: {str(e)}")
        }

    # 프롬프트 템플릿 설정
    PROMPT_TEMPLATE = """
    Human: You are a financial advisor AI system, and provides answers to questions by using fact based and statistical information.
    Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    <question>
    {question}
    </question>

    The response should be specific and use statistics or numbers when possible.

    Assistant:"""
    claude_prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

    # RetrievalQA 체인 설정
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": claude_prompt}
    )

    # 질문 수행
    try:
        answer = qa.invoke(query)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error invoking QA chain: {str(e)}")
        }
    
    # Document 객체를 JSON으로 변환
    def document_to_dict(doc):
        return {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }

    # JSON 직렬화 가능한 형태로 변환
    if isinstance(answer, dict):
        answer["source_documents"] = [document_to_dict(doc) for doc in answer.get("source_documents", [])]

    return {
        'statusCode': 200,
        'body': json.dumps(answer)
    }
