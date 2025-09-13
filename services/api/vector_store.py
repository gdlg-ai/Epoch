import os
from typing import List, Dict, Any


class VectorStoreItem(Dict[str, Any]):
    pass


class QueryResult(Dict[str, Any]):
    pass


class VectorStore:
    def add(self, items: List[VectorStoreItem]) -> None:
        raise NotImplementedError

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[QueryResult]:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def list_all(self) -> List[VectorStoreItem]:
        raise NotImplementedError


class ChromaVectorStore(VectorStore):
    def __init__(self, collection: str = "epoch_memory"):
        import chromadb
        from chromadb.config import Settings

        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "/app/data/chroma")
        telemetry = os.getenv("CHROMA_TELEMETRY", "false").lower() == "true"
        self.client = chromadb.Client(
            Settings(
                anonymized_telemetry=telemetry,
                is_persistent=True,
                persist_directory=persist_dir,
            )
        )
        self.col = self.client.get_or_create_collection(
            collection_name=collection, metadata={"hnsw:space": "cosine"}
        )

    def add(self, items: List[VectorStoreItem]) -> None:
        ids = [it["id"] for it in items]
        embs = [it["embedding"] for it in items]
        docs = [it["text"] for it in items]
        metas = [it.get("meta", {}) for it in items]
        self.col.add(ids=ids, embeddings=embs, documents=docs, metadatas=metas)

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[QueryResult]:
        res = self.col.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances", "ids"],
        )
        hits: List[QueryResult] = []
        for i in range(len(res["ids"][0])):
            hits.append(
                {
                    "id": res["ids"][0][i],
                    "text": res["documents"][0][i],
                    "meta": res["metadatas"][0][i],
                    "score": 1.0 - float(res["distances"][0][i]),
                }
            )
        return hits

    def count(self) -> int:
        return self.col.count()

    def list_all(self) -> List[VectorStoreItem]:
        data = self.col.get(include=["documents", "metadatas", "ids"], where={})
        out: List[VectorStoreItem] = []
        for i in range(len(data.get("ids", []))):
            out.append(
                {
                    "id": data["ids"][i],
                    "text": data["documents"][i],
                    "meta": data["metadatas"][i],
                }
            )
        return out


def get_vector_store() -> VectorStore:
    kind = os.getenv("VECTOR_STORE", "jsonl").lower()
    if kind == "chroma":
        return ChromaVectorStore()
    raise NotImplementedError

