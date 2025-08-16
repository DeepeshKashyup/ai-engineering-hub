
# Decentralized Data Marketplace with GenAI Dataset Summarizer

## Goal
Build a mock data marketplace where datasets are registered on-chain, metadata is summarized by GenAI, and buyers can verify authenticity.

---

## Architecture

```
[CSV / Parquet Datasets] → [Metadata Extractor]
	↓
[Blockchain (Ethereum Testnet)] → [IPFS for actual files]
	↓
[GenAI Summarizer + Embedding Search] → [Web App Frontend]
```

---

## Tech Stack

- **Blockchain:** Ethereum (Goerli testnet)
- **Storage:** IPFS for dataset files
- **Search:** FAISS / Pinecone
- **GenAI:** LLM to auto-generate dataset descriptions and search queries
- **Frontend:** React + Next.js

---

## Dataset

- Open datasets from Kaggle / data.gov
- Store file hash on-chain, file in IPFS

---

## Blockchain Value

- Verifies dataset integrity and ownership before download.

---

## 💡 Tip for Portfolio/Hackathon

For extra wow factor, make the blockchain part verifiable live — for example, after a user queries data, show a **“Proof of Integrity”** button that fetches the hash from the blockchain and validates it.