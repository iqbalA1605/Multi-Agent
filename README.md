# Multi Agent System

A Multi-Agent Research System built using LangGraph, LangChain, Google Gemini, Tavily Search, BeautifulSoup, and Streamlit. The system employs multiple AI agents working together in an agentic workflow to perform intelligent web research, analyze information, generate comprehensive reports, and review the quality of the generated output.

## Features

* Web Research Agent powered by Tavily Search for retrieving relevant and up-to-date information.
* Content Reader Agent that extracts information from web pages using BeautifulSoup.
* AI-powered Report Writer that transforms collected research into a structured and detailed report.
* Research Critic Agent that evaluates the generated report and provides constructive feedback.
* Multi-Agent orchestration using LangGraph.
* LCEL (LangChain Expression Language) pipelines with Runnables for modular execution.
* Interactive Streamlit frontend for a user-friendly experience.
* Secure environment variable management using `python-dotenv`.

## System Architecture

```text
User Query
     │
     ▼
Search Agent (Tavily Search)
     │
     ▼
Reader Agent (BeautifulSoup)
     │
     ▼
Writer Chain (Gemini + LCEL)
     │
     ▼
Critic Chain (Gemini + LCEL)
     │
     ▼
Final Research Report
```

## Tech Stack

* Python
* LangChain
* LangGraph
* Google Gemini API
* Tavily Search API
* BeautifulSoup4
* Requests
* Streamlit
* LCEL (LangChain Expression Language)
* `python-dotenv`

## Environment Variables

Create a `.env` file in the project root and add:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit your `.env` file or API keys to GitHub.

## Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository, create a feature branch, and submit a pull request.
