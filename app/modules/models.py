from typing import TypedDict, List
from langchain_core.documents import Document


class GraphState(TypedDict):
    question: str
    context: List[Document]
    answer: str
