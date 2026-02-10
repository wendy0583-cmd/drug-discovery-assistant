# 🧬 Drug Discovery Research Assistant
**Agent-style Research Summarization using Amazon Bedrock**

---

## 📌 Overview

This project is a **prototype AI research assistant for drug discovery**,  
designed to **summarize and interpret biomedical research content** using  
**Amazon Bedrock foundation models**.

The primary goal of this project is **architectural validation** —  
to understand how **agent-style AI systems** can be built for scientific research workflows,  
rather than to deliver a production-ready service.

---

## 🎯 What I Built

- Implemented a **minimal text summarization pipeline** using Amazon Bedrock
- Verified **Bedrock model invocation via Python (boto3)**
- Designed a **tool → LLM → response** flow suitable for agent-based systems
- Structured the project for **future multi-agent orchestration**
- Focused on **cost-efficient model usage and reproducibility**

---

## 🏗️ Architecture (Conceptual)

```text
User Input (Research Query / IDs)
        ↓
Data Preparation / Tool Logic
        ↓
Amazon Bedrock (Foundation Model)
        ↓
Summarized Research Output


🧪 Current Status

✅ Amazon Bedrock connectivity verified

✅ Single-model invocation tested successfully

✅ Text summarization output validated

⏳ External data integration at prototype level

⏳ Multi-agent orchestration planned (not yet implemented)

📂 Project Structure
drug-discovery-assistant/
├── application/               # Core application logic
├── assets/                    # Diagrams or reference assets
├── test_bedrock_connection.py # Bedrock connectivity validation script
├── README.md                  # Project overview (English)
├── README_KR.md               # Project overview (Korean)
└── .gitignore

🔬 Why This Project

Modern drug discovery increasingly relies on AI-assisted literature analysis.
This project explores:

How foundation models can support scientific reasoning

How agent-like workflows can be structured on AWS

How to design extensible AI systems without overengineering

The emphasis is on system design understanding and validation,
not on UI polish or full automation.

🚀 Future Work

Multi-agent orchestration (Orchestrator / Tool / LLM roles)

Integration with biomedical data sources (e.g., PubMed, ChEMBL)

Optional serverless execution (Lambda-based flow)

Enhanced retrieval and ranking strategies (RAG)

⚠️ Disclaimer

This repository is a research and learning prototype.
It is not intended for clinical, regulatory, or production use.

👩‍🔬 Author

wendy0583-cmd
Background in biomedical research and AI-assisted drug discovery
Focused on AI architecture validation and scientific applications

📎 For the Korean version, see README_KR.md
