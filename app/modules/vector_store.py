from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from mongo_conn import get_documents
from langchain_core.documents import Document
from config import Config


def init_vector_store():
    raw_docs = get_documents()
    documents = []
    for law_doc in raw_docs:
        metadata = {
            "law_id": str(law_doc["_id"]),
            "법령일련번호": law_doc.get("법령일련번호", ""),
            "법령명한글": law_doc.get("법령명한글", ""),
            "시행일자": law_doc.get("시행일자", ""),
        }

        for clause in law_doc.get("조문", []):
            clause_content = []
            if clause.get("조문제목"):
                clause_content.append(
                    f"제{clause['조문번호']}조 ({clause['조문제목']})"
                )
            else:
                clause_content.append(f"제{clause['조문번호']}조")

            if clause.get("조문내용"):
                clause_content.append(clause["조문내용"])

            for item in clause.get("항", []):
                if item.get("항내용"):
                    clause_content.append(f"항 {item['항내용']}")
                for sub_item in item.get("호", []):
                    if sub_item.get("호내용"):
                        clause_content.append(f"  호 {sub_item['호내용']}")

            clause_metadata = metadata.copy()
            clause_metadata.update(
                {
                    "조문번호": clause["조문번호"],
                    "조문시행일자": clause.get("조문시행일자", ""),
                }
            )

            if clause_content:
                doc = Document(
                    page_content="\n".join(clause_content), metadata=clause_metadata
                )
                documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n제", "\n제", "。", "》", "항", "호"],
        keep_separator=True,
    )
    splits = text_splitter.split_documents(documents)

    return Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        collection_name=Config.COLLECTION_NAME,
        persist_directory="./chroma_db",
    )


vector_store = init_vector_store()
