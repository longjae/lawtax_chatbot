from langgraph.graph import StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from modules.models import GraphState
from modules.vector_store import vector_store


def retrieve(state: GraphState):
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 5,
        },
    )
    return {"context": retriever.invoke(state["question"])}


def generate(state: GraphState):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "법률 문서 컨텍스트:\n\n{context}\n\n"
        "질문: {question}\n\n"
        "한국 법령에 근거하여 전문가 수준으로 답변하되, "
        "조문 번호와 근거 법령명을 반드시 명시해주세요."
    )
    return {"answer": (prompt | llm).invoke(state).content}


# 워크플로우 구성
def build_workflow():
    """워크플로우를 정의하는 함수"""
    workflow = StateGraph(GraphState)

    workflow.add_node("retriever", retrieve)
    workflow.add_node("generator", generate)
    # edge 설정 확인
    workflow.set_entry_point("retriever")
    workflow.add_edge("retriever", "generator")
    # 컴파일
    return workflow.compile()


app = build_workflow()
