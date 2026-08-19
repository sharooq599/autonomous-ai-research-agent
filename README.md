# 🤖 Autonomous AI Research Agent

An AI-powered autonomous research system that can understand a user's research question, create a research plan, perform web research, analyze gathered information, manage sources, and generate a structured research report.

The application combines a **multi-agent architecture**, **LangGraph workflow orchestration**, **FastAPI**, **PostgreSQL conversation memory**, and a **React + Tailwind CSS frontend**.

---

## 📌 Project Overview

Traditional AI chatbots generally respond directly to a user's question.

This project takes a different approach.

The system works as an autonomous research pipeline where multiple specialized agents collaborate to:

1. Understand the research question
2. Create a research plan
3. Search the web for relevant information
4. Manage and organize research sources
5. Analyze the collected information
6. Generate a detailed final report
7. Store the conversation for future reference

---

## ✨ Features

- 🤖 Multi-agent AI architecture
- 🧠 Autonomous research workflow
- 🔄 LangGraph-based workflow orchestration
- 🔎 AI-powered web search
- 📚 Source management
- 📊 Information analysis
- 📝 Automated research report generation
- 🧮 Calculator tool
- 💾 PostgreSQL conversation memory
- 💬 Conversation history
- 🆕 Create and manage multiple conversations
- ⚡ FastAPI backend
- ⚛️ React frontend
- 🎨 Tailwind CSS UI
- 🔐 Environment variable configuration
- 🌐 Frontend-backend API integration
- 📱 Responsive user interface

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      React UI       │
                         │  React + Tailwind   │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP API
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      LangGraph      │
                         │     Workflow        │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌────────────┐         ┌────────────┐        ┌────────────┐
      │   Planner  │         │ Researcher │        │  Analyzer  │
      │    Agent   │         │    Agent   │        │    Agent   │
      └────────────┘         └─────┬──────┘        └─────┬──────┘
                                   │                      │
                                   ▼                      │
                            ┌─────────────┐               │
                            │ Web Search  │               │
                            │    Tool     │               │
                            └──────┬──────┘               │
                                   │                      │
                                   ▼                      ▼
                            ┌────────────────────────────────┐
                            │        Source Manager           │
                            └────────────────┬───────────────┘
                                             │
                                             ▼
                                     ┌──────────────┐
                                     │   Reporter   │
                                     │     Agent    │
                                     └──────┬───────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │  Final Research │
                                   │      Report     │
                                   └─────────────────┘

                         ┌─────────────────────┐
                         │     PostgreSQL      │
                         │ Conversation Memory │
                         └─────────────────────┘