# modules/resume_rag.py
# RAG pipeline using ChromaDB + Sentence Transformers
# Drop this file into your existing modules/ folder

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
import streamlit as st

# ── Embedding model (free, runs locally, no API key needed) ──────────────────
EMBED_FN = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# ── Persistent ChromaDB client (survives reruns) ──────────────────────────────
@st.cache_resource
def get_chroma_client():
    """Persistent ChromaDB client cached across Streamlit reruns."""
    return chromadb.Client()  # In-memory for now; change to PersistentClient("./chroma_db") to save to disk

def get_chroma_collection(collection_name: str = "resumes"):
    """Get or create a ChromaDB collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=EMBED_FN,
        metadata={"hnsw:space": "cosine"}  # cosine similarity for text
    )

def get_jd_collection():
    """Separate collection for Job Descriptions — used for JD-based RAG."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="job_descriptions",
        embedding_function=EMBED_FN,
        metadata={"hnsw:space": "cosine"}
    )

# ── Indexing ──────────────────────────────────────────────────────────────────

def build_candidate_document(candidate: Dict) -> str:
    """
    Convert a parsed resume dict into a rich text document for embedding.
    The richer this text, the better the semantic search works.
    """
    skills = ", ".join(candidate.get("skills", []))
    education = ""
    if candidate.get("education"):
        edu = candidate["education"][0]
        education = f"{edu.get('degree', '')} from {edu.get('institution', 'unknown institution')}"

    doc = f"""
Candidate: {candidate.get('name', 'Unknown')}
Skills: {skills}
Experience: {candidate.get('experience_years', 0)} years of professional experience
Education: {education}
Location: {candidate.get('location', 'Not specified')}
Notice Period: {candidate.get('notice_period', 60)} days
Current CTC: {candidate.get('current_ctc', 0)} LPA
Expected CTC: {candidate.get('expected_ctc', 0)} LPA
Match Score: {candidate.get('match_score', 0)}/100
Resume Summary: {candidate.get('raw_text', '')[:800]}
""".strip()
    return doc


def index_candidate(candidate: Dict, candidate_id: str, drive_id: str = "") -> bool:
    """
    Embed and store a single candidate into ChromaDB.
    Call this right after you save a candidate to MongoDB.
    Returns True on success.
    """
    try:
        collection = get_chroma_collection()
        doc = build_candidate_document(candidate)

        collection.upsert(
            documents=[doc],
            ids=[candidate_id],
            metadatas=[{
                "name": candidate.get("name", "Unknown"),
                "email": candidate.get("email", ""),
                "match_score": float(candidate.get("match_score", 0)),
                "experience_years": float(candidate.get("experience_years", 0)),
                "notice_period": int(candidate.get("notice_period", 60)),
                "location": candidate.get("location", ""),
                "drive_id": drive_id,
            }]
        )
        return True
    except Exception as e:
        print(f"[RAG] Failed to index candidate {candidate_id}: {e}")
        return False


def index_all_candidates(candidates: List[Dict]) -> int:
    """
    Bulk index all candidates into ChromaDB.
    Returns count of successfully indexed candidates.
    """
    collection = get_chroma_collection()
    docs, ids, metas = [], [], []

    for c in candidates:
        cid = str(c.get("_id", ""))
        if not cid:
            continue
        docs.append(build_candidate_document(c))
        ids.append(cid)
        metas.append({
            "name": c.get("name", "Unknown"),
            "email": c.get("email", ""),
            "match_score": float(c.get("match_score", 0)),
            "experience_years": float(c.get("experience_years", 0)),
            "notice_period": int(c.get("notice_period", 60)),
            "location": c.get("location", ""),
            "drive_id": str(c.get("drive_id", "")),
        })

    if docs:
        collection.upsert(documents=docs, ids=ids, metadatas=metas)

    return len(docs)


def index_job_description(jd_text: str, jd_id: str, role: str, company: str = "") -> bool:
    """
    Store a Job Description in ChromaDB.
    This lets you do JD-to-JD similarity (find similar past roles).
    """
    try:
        collection = get_jd_collection()
        collection.upsert(
            documents=[jd_text],
            ids=[jd_id],
            metadatas=[{"role": role, "company": company}]
        )
        return True
    except Exception as e:
        print(f"[RAG] Failed to index JD {jd_id}: {e}")
        return False


# ── Retrieval ─────────────────────────────────────────────────────────────────

def semantic_search(
    query: str,
    top_k: int = 5,
    drive_id: str = None
) -> List[Dict[str, Any]]:
    """
    Find the most semantically similar candidates to any natural language query.
    Optionally filter by drive_id.

    Example queries:
    - "backend developer with AWS and microservices"
    - "candidate who can join immediately with Python skills"
    - "IIT graduate with machine learning experience"
    """
    collection = get_chroma_collection()

    # Build where filter if drive_id provided
    where = {"drive_id": drive_id} if drive_id else None

    try:
        results = collection.query(
            query_texts=[query],
            n_results=min(top_k, collection.count() or 1),
            where=where,
            include=["documents", "metadatas", "distances"]
        )
    except Exception as e:
        print(f"[RAG] Search error: {e}")
        return []

    candidates = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        similarity = round((1 - distance) * 100, 1)  # Convert cosine distance to % similarity

        candidates.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "similarity": similarity,
        })

    # Sort by similarity descending
    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    return candidates


def find_similar_candidates(candidate_id: str, top_k: int = 3) -> List[Dict]:
    """
    Given a candidate ID, find other similar candidates.
    Great for finding backup candidates when top choice rejects.
    """
    collection = get_chroma_collection()
    try:
        # Get the candidate's document first
        result = collection.get(ids=[candidate_id], include=["documents"])
        if not result["documents"]:
            return []

        candidate_doc = result["documents"][0]
        # Use the document as the query
        return semantic_search(candidate_doc, top_k=top_k + 1)
    except Exception as e:
        print(f"[RAG] Similar candidates error: {e}")
        return []


def rag_answer(question: str, candidates: List[Dict], drive_info: Dict) -> str:
    """
    RAG-powered Q&A: retrieves relevant candidate context, then passes to Groq LLM.
    This upgrades your existing chat_agent.py with retrieval-augmented generation.
    """
    from groq import Groq
    import os

    # Step 1: Retrieve semantically relevant candidates
    retrieved = semantic_search(question, top_k=5, drive_id=str(drive_info.get("_id", "")))

    # Step 2: Build context from retrieved candidates
    if retrieved:
        context = "MOST RELEVANT CANDIDATES (retrieved by semantic search):\n"
        for r in retrieved:
            meta = r["metadata"]
            context += f"\n- {meta.get('name')}: score {meta.get('match_score')}/100, "
            context += f"{meta.get('experience_years')} yrs exp, notice {meta.get('notice_period')} days\n"
            context += f"  Details: {r['document'][:300]}\n"
    else:
        # Fallback to all candidates if RAG finds nothing
        context = "ALL CANDIDATES:\n"
        for c in candidates[:10]:
            context += f"- {c.get('name')}: score {c.get('match_score', 0)}/100\n"

    # Step 3: Call LLM with retrieved context
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""You are an expert Indian recruiter AI assistant.

Drive: {drive_info.get('drive_name', 'Unknown')} | Role: {drive_info.get('role', 'Unknown')}

{context}

Recruiter question: {question}

Give a clear, helpful answer based on the candidate data above."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {e}"


# ── Utility ───────────────────────────────────────────────────────────────────

def get_indexed_count() -> int:
    """How many candidates are currently in the vector store."""
    try:
        return get_chroma_collection().count()
    except Exception:
        return 0


def clear_collection(collection_name: str = "resumes") -> bool:
    """Clear all candidates from the vector store (useful for testing)."""
    try:
        client = get_chroma_client()
        client.delete_collection(collection_name)
        return True
    except Exception:
        return False