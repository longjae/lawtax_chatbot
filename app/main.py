from modules.workflow import build_workflow
from modules.models import GraphState

app = build_workflow()


def execute_question(question):
    state = GraphState(question=question, context=[], answer="")
    try:
        for output in app.stream(state):
            if "generator" in output:
                return output["generator"]["answer"]
    except GeneratorExit:
        print("워크플로우 조기 종료 처리")
        raise


if __name__ == "__main__":
    questions = input("질문을 입력하세요 (여러 질문은 ,로 구분): ").split(",")

    for q in questions:
        q = q.strip()
        print(f"Q: {q}")
        print(f"A: {execute_question(q)}\n{'='*50}")
