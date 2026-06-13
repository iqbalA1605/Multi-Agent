from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrap_url
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# agnet1
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

# agent2
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrap_url]
    )

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior research analyst and professional report writer.

Your task is to transform raw research data into a comprehensive, well-structured, factual, and insightful report.

Guidelines:
- Write in a professional and objective tone.
- Prioritize accuracy and factual correctness.
- Synthesize information from multiple sources rather than simply listing facts.
- Explain concepts clearly and provide context where necessary.
- Highlight important trends, insights, and implications.
- Avoid repetition and unnecessary filler.
- Use clear headings and subheadings.
- Ensure the report is easy to read for both technical and non-technical audiences.
- Include all relevant sources at the end.
"""
    ),
    (
        "human",
        """
Create a detailed research report based on the information provided below.

TOPIC:
{topic}

RESEARCH DATA:
{research}

Generate a report using the following structure:

# Executive Summary
Provide a concise overview of the topic and the most important findings.

# Introduction
Explain the topic, its background, and why it is important.

# Key Findings
Provide at least 3–5 major findings.
For each finding:
- Give a clear heading.
- Explain the finding in detail.
- Include supporting evidence, facts, statistics, or examples when available.
- Discuss its significance and impact.

# Analysis and Insights
Analyze patterns, trends, opportunities, challenges, or future implications revealed by the research.

# Conclusion
Summarize the most important takeaways and overall conclusions.

# Sources
List all source URLs referenced in the research.

Requirements:
- Be comprehensive and detailed.
- Use factual information only.
- Do not invent information that is not present in the research.
- Maintain logical flow between sections.
- Use markdown formatting.
"""
    )
])


writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior research reviewer and quality assurance analyst.

Your role is to critically evaluate research reports for:
- Accuracy
- Completeness
- Clarity
- Structure
- Depth of analysis
- Quality of evidence
- Professional writing standards

Be objective, constructive, and specific.
Do not provide vague feedback.
Identify both strengths and weaknesses clearly.
"""
    ),
    (
        "human",
        """
Review the research report below and evaluate it rigorously.

Research Report:
{report}

Evaluate the report on:

1. Accuracy and factual reliability
2. Depth of research
3. Clarity and readability
4. Organization and structure
5. Quality of insights and analysis
6. Source usage and credibility

Respond in the following format:

# Overall Score
Score: X/10

# Strengths
- ...
- ...
- ...

# Areas for Improvement
- ...
- ...
- ...

# Missing Information
- ...
- ...

# Recommendations
- ...
- ...

# Final Verdict
One concise sentence summarizing the overall quality of the report.
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()