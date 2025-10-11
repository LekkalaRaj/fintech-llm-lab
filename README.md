# 💹 FinTech LLM Lab

> 🚀 A collection of AI-powered financial intelligence tools and research projects — built using Python, LLMs, and modern data frameworks.

---

## 🧭 Overview

**FinTech LLM Lab** is your personal sandbox for experimenting, building, and deploying intelligent financial applications powered by **Large Language Models (LLMs)**.

This repository brings together projects focused on:
- **Stock market analytics**
- **Portfolio intelligence**
- **Financial data summarization**
- **Expense classification**
- **Conversational AI for finance**

Each subproject is modular, conda-managed, and built with reusable Python components.

---

## ⚙️ Environment Setup

This project uses **Conda** for environment and dependency management.

### 🧱 Create & Activate Environment

```bash
conda env create -f environment.yaml
conda activate fintech-llm-lab
```

## 🔑 Environment Variables

Create a .env file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
ALPHAVANTAGE_API_KEY=your_alpha_vantage_key_here
```


## 🧠 Projects Included

| Project | Description | Tech Stack |
|----------|--------------|-------------|
| **`stockiq`** | Indian Stock Portfolio Intelligence Dashboard with LLM insights and Streamlit UI | Streamlit, YFinance, LangChain |