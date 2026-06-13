import streamlit as st
import time
import sys
import os
from io import StringIO

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #0a0a0f !important;
    color: #e8e4d9 !important;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse at center, rgba(212,175,55,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    color: #b89a3a;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.6rem, 5vw, 4rem);
    font-weight: 900;
    line-height: 1.05;
    color: #f0ece0;
    letter-spacing: -0.02em;
}
.hero-title span { color: #d4af37; }
.hero-subtitle {
    font-size: 1rem;
    color: #7a7568;
    margin-top: 0.9rem;
    font-weight: 300;
    letter-spacing: 0.03em;
}

/* ── Divider ── */
.rule {
    border: none;
    border-top: 1px solid #1e1d1a;
    margin: 2rem 0;
}

/* ── Search Bar ── */
div[data-testid="stTextInput"] > div > div > input {
    background: #111116 !important;
    border: 1px solid #2a2820 !important;
    border-radius: 6px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.08) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    color: #6b6456 !important;
    text-transform: uppercase !important;
}

/* ── Primary Button ── */
div[data-testid="stButton"] > button {
    background: #d4af37 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2rem !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    background: #e8c84a !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Agent Step Card ── */
.agent-card {
    background: #111116;
    border: 1px solid #1e1d1a;
    border-left: 3px solid #2a2820;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-left-color 0.3s;
    position: relative;
    overflow: hidden;
}
.agent-card.active  { border-left-color: #d4af37; }
.agent-card.done    { border-left-color: #4a9a6a; }
.agent-card.error   { border-left-color: #c0392b; }

.agent-card::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 120px; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.01));
    pointer-events: none;
}

.agent-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.3rem;
}
.agent-icon {
    font-size: 1.2rem;
    line-height: 1;
}
.agent-name {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9a9080;
}
.agent-name.active { color: #d4af37; }
.agent-name.done   { color: #4a9a6a; }
.agent-name.error  { color: #c0392b; }

.agent-desc {
    font-size: 0.85rem;
    color: #5a5448;
    padding-left: 2rem;
    font-weight: 300;
}

.status-pill {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    text-transform: uppercase;
}
.pill-waiting { background: #1a1918; color: #4a4540; border: 1px solid #2a2820; }
.pill-running { background: rgba(212,175,55,0.12); color: #d4af37; border: 1px solid rgba(212,175,55,0.3); }
.pill-done    { background: rgba(74,154,106,0.12); color: #4a9a6a; border: 1px solid rgba(74,154,106,0.3); }
.pill-error   { background: rgba(192,57,43,0.12); color: #e74c3c; border: 1px solid rgba(192,57,43,0.3); }

/* ── Result Panels ── */
.result-panel {
    background: #0e0e13;
    border: 1px solid #1e1d1a;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.result-panel-header {
    background: #111116;
    border-bottom: 1px solid #1e1d1a;
    padding: 0.85rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.result-panel-icon { font-size: 1rem; }
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.73rem;
    letter-spacing: 0.18em;
    color: #8a8070;
    text-transform: uppercase;
}
.result-panel-body {
    padding: 1.4rem;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #c8c4b8;
    white-space: pre-wrap;
    font-weight: 300;
    max-height: 420px;
    overflow-y: auto;
}
.result-panel-body::-webkit-scrollbar { width: 4px; }
.result-panel-body::-webkit-scrollbar-track { background: transparent; }
.result-panel-body::-webkit-scrollbar-thumb { background: #2a2820; border-radius: 4px; }

/* ── Report Panel (special) ── */
.result-panel.report { border-color: rgba(212,175,55,0.2); }
.result-panel.report .result-panel-header { background: rgba(212,175,55,0.05); border-color: rgba(212,175,55,0.15); }
.result-panel.report .result-panel-title { color: #d4af37; }

/* ── Critic Panel (special) ── */
.result-panel.critic { border-color: rgba(74,154,106,0.2); }
.result-panel.critic .result-panel-header { background: rgba(74,154,106,0.05); border-color: rgba(74,154,106,0.15); }
.result-panel.critic .result-panel-title { color: #4a9a6a; }

/* ── Progress bar (override) ── */
div[data-testid="stProgress"] > div { background: #1a1918 !important; border-radius: 4px !important; }
div[data-testid="stProgress"] > div > div { background: linear-gradient(90deg, #b89a3a, #d4af37) !important; border-radius: 4px !important; }

/* ── Error box ── */
.err-box {
    background: rgba(192,57,43,0.08);
    border: 1px solid rgba(192,57,43,0.25);
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    color: #e57373;
    font-size: 0.88rem;
    font-family: 'DM Mono', monospace;
    line-height: 1.6;
}

/* ── Section label ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    color: #4a4540;
    text-transform: uppercase;
    margin-bottom: 1rem;
    margin-top: 2rem;
}

/* ── Completion banner ── */
.complete-banner {
    text-align: center;
    padding: 2rem;
    background: rgba(74,154,106,0.06);
    border: 1px solid rgba(74,154,106,0.2);
    border-radius: 10px;
    margin: 1.5rem 0;
}
.complete-banner h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #4a9a6a;
    margin-bottom: 0.4rem;
}
.complete-banner p {
    color: #5a7a65;
    font-size: 0.85rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
}

/* ── Spinner override ── */
div[data-testid="stSpinner"] { color: #d4af37 !important; }

/* ── Tabs override ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1e1d1a !important;
    gap: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #5a5448 !important;
    background: transparent !important;
    border: none !important;
    padding: 0.7rem 1.5rem !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    color: #d4af37 !important;
    border-bottom: 2px solid #d4af37 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render an agent step card ─────────────────────────────────────────
def agent_card(icon: str, name: str, desc: str, status: str = "waiting") -> None:
    status_labels = {
        "waiting": ("pill-waiting", "Waiting"),
        "running": ("pill-running", "Running…"),
        "done":    ("pill-done",    "Done"),
        "error":   ("pill-error",   "Error"),
    }
    pill_cls, pill_text = status_labels.get(status, ("pill-waiting", "Waiting"))
    card_cls = "agent-card" + (f" {status}" if status in ("active", "done", "error") else
                                " active" if status == "running" else "")
    name_cls = "agent-name" + (" active" if status == "running" else
                                " done"   if status == "done"    else
                                " error"  if status == "error"   else "")
    st.markdown(f"""
    <div class="{card_cls}">
      <div class="agent-header">
        <span class="agent-icon">{icon}</span>
        <span class="{name_cls}">{name}</span>
        <span class="status-pill {pill_cls}">{pill_text}</span>
      </div>
      <div class="agent-desc">{desc}</div>
    </div>""", unsafe_allow_html=True)


# ── Helper: safely coerce ANY LangChain output to a plain string ──────────────
def to_str(value) -> str:
    """LangChain chains can return str, list[str], list[dict], AIMessage, etc.
    This function normalises all of them into a single printable string."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif hasattr(item, "text"):          # LangChain TextChunk
                parts.append(item.text)
            elif hasattr(item, "content"):       # AIMessage / BaseMessage
                parts.append(str(item.content))
            elif isinstance(item, dict):
                parts.append(item.get("text") or item.get("content") or str(item))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if hasattr(value, "content"):               # AIMessage
        return to_str(value.content)
    return str(value)


# ── Helper: render a result panel ─────────────────────────────────────────────
def result_panel(icon: str, title: str, content, extra_cls: str = "") -> None:
    import html as html_module
    safe = html_module.escape(to_str(content))
    st.markdown(f"""
    <div class="result-panel {extra_cls}">
      <div class="result-panel-header">
        <span class="result-panel-icon">{icon}</span>
        <span class="result-panel-title">{title}</span>
      </div>
      <div class="result-panel-body">{safe}</div>
    </div>""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Multi-Agent · LangGraph · Gemini</div>
  <div class="hero-title">Research<span>Mind</span></div>
  <div class="hero-subtitle">Four specialised agents collaborate to deliver deep, verified research on any topic.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([5, 1], gap="small")
with col_in:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2024",
        label_visibility="visible",
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)  # vertical align
    run_btn = st.button("Analyse →")

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Main logic ─────────────────────────────────────────────────────────────────
AGENTS = [
    ("🔍", "Search Agent",  "Queries the web for recent, reliable sources on your topic."),
    ("📄", "Reader Agent",  "Scrapes the most relevant URL for deeper contextual content."),
    ("✍️",  "Writer Agent",  "Drafts a structured, comprehensive research report."),
    ("🧐", "Critic Agent",  "Reviews the report for gaps, accuracy, and depth of analysis."),
]

if run_btn and topic.strip():
    # ── Live pipeline execution ──
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown('<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True)
        step_placeholders = [st.empty() for _ in AGENTS]

    with right:
        st.markdown('<div class="section-label">Live Output</div>', unsafe_allow_html=True)
        progress_bar   = st.progress(0)
        status_text    = st.empty()
        output_area    = st.empty()

    def render_steps(current: int, statuses: list[str]) -> None:
        for idx, (icon, name, desc) in enumerate(AGENTS):
            step_placeholders[idx].empty()
            with step_placeholders[idx]:
                agent_card(icon, name, desc, statuses[idx])

    statuses = ["waiting"] * 4
    render_steps(-1, statuses)

    state: dict = {}
    error_msg: str | None = None

    try:
        # ── Import pipeline (assumes same working directory) ──
        from pipeline import run_research_pipeline as _run  # noqa: F401
        # We'll call each step manually for granular progress

        from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

        # ── Step 1: Search ────────────────────────────────────────────────────
        statuses[0] = "running"
        render_steps(0, statuses)
        progress_bar.progress(5)
        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.78rem;color:#d4af37;letter-spacing:0.1em;">🔍 Search agent is querying the web…</p>',
            unsafe_allow_html=True,
        )

        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        last_msg           = search_result["messages"][-1]
        state["search_results"] = to_str(last_msg.content if hasattr(last_msg, "content") else last_msg)

        statuses[0] = "done"
        progress_bar.progress(25)
        output_area.empty()
        with output_area.container():
            result_panel("🔍", "Search Results", state["search_results"])

        # ── Step 2: Reader ───────────────────────────────────────────────────
        statuses[1] = "running"
        render_steps(1, statuses)
        progress_bar.progress(30)
        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.78rem;color:#d4af37;letter-spacing:0.1em;">📄 Reader agent is scraping top resources…</p>',
            unsafe_allow_html=True,
        )

        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        last_reader_msg          = reader_result["messages"][-1]
        state["scraped_content"] = to_str(last_reader_msg.content if hasattr(last_reader_msg, "content") else last_reader_msg)

        statuses[1] = "done"
        progress_bar.progress(50)
        output_area.empty()
        with output_area.container():
            result_panel("🔍", "Search Results",  state["search_results"])
            result_panel("📄", "Scraped Content", state["scraped_content"])

        # ── Step 3: Writer ───────────────────────────────────────────────────
        statuses[2] = "running"
        render_steps(2, statuses)
        progress_bar.progress(55)
        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.78rem;color:#d4af37;letter-spacing:0.1em;">✍️  Writer agent is drafting the report…</p>',
            unsafe_allow_html=True,
        )

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = to_str(writer_chain.invoke({
            "topic":    topic,
            "research": research_combined,
        }))

        statuses[2] = "done"
        progress_bar.progress(75)
        output_area.empty()
        with output_area.container():
            result_panel("🔍", "Search Results",     state["search_results"])
            result_panel("📄", "Scraped Content",    state["scraped_content"])
            result_panel("📝", "Research Report",    state["report"],   extra_cls="report")

        # ── Step 4: Critic ───────────────────────────────────────────────────
        statuses[3] = "running"
        render_steps(3, statuses)
        progress_bar.progress(80)
        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.78rem;color:#d4af37;letter-spacing:0.1em;">🧐 Critic agent is reviewing the report…</p>',
            unsafe_allow_html=True,
        )

        state["feedback"] = to_str(critic_chain.invoke({"report": state["report"]}))

        statuses[3] = "done"
        progress_bar.progress(100)

        output_area.empty()
        with output_area.container():
            result_panel("🔍", "Search Results",  state["search_results"])
            result_panel("📄", "Scraped Content", state["scraped_content"])
            result_panel("📝", "Research Report", state["report"],    extra_cls="report")
            result_panel("🧐", "Critic Feedback", state["feedback"],  extra_cls="critic")

        render_steps(-1, statuses)

    except ImportError as e:
        error_msg = (
            f"Import Error: {e}\n\n"
            "Make sure pipeline.py and agents.py are in the same directory as app.py, "
            "and that all dependencies are installed.\n\n"
            "Run:  pip install -r requirements.txt"
        )
        statuses = ["error" if s == "running" else s for s in statuses]
        render_steps(-1, statuses)

    except Exception as e:
        error_msg = f"Pipeline Error: {type(e).__name__}: {e}"
        statuses = ["error" if s == "running" else s for s in statuses]
        render_steps(-1, statuses)

    if error_msg:
        status_text.empty()
        progress_bar.empty()
        output_area.empty()
        with right:
            st.markdown(f'<div class="err-box">⚠ {error_msg}</div>', unsafe_allow_html=True)
    else:
        status_text.empty()
        with right:
            st.markdown("""
            <div class="complete-banner">
              <h3>✓ Research Complete</h3>
              <p>All four agents finished successfully</p>
            </div>""", unsafe_allow_html=True)

elif run_btn and not topic.strip():
    st.markdown('<div class="err-box">⚠ Please enter a research topic before running the pipeline.</div>',
                unsafe_allow_html=True)

else:
    # ── Idle state: show pipeline overview ───────────────────────────────────
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.markdown('<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True)
        for icon, name, desc in AGENTS:
            agent_card(icon, name, desc, "waiting")

    with right:
        st.markdown('<div class="section-label">How It Works</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="padding: 1.5rem; background: #111116; border: 1px solid #1e1d1a; border-radius: 10px; line-height: 1.9;">
          <p style="font-size:0.88rem; color:#7a7568; font-weight:300; margin-bottom:1.2rem;">
            ResearchMind orchestrates four specialised AI agents in sequence using LangGraph. Each agent hands off its output to the next, creating a robust research pipeline.
          </p>
          <div style="display:grid; gap:1rem;">
            <div style="display:flex; gap:0.75rem; align-items:flex-start;">
              <span style="font-family:'DM Mono',monospace; font-size:0.7rem; color:#d4af37; background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.25); border-radius:4px; padding:0.15rem 0.5rem; margin-top:2px; white-space:nowrap;">01</span>
              <span style="font-size:0.85rem; color:#9a9080; font-weight:300;"><strong style="color:#c8c4b8; font-weight:400;">Search</strong> — Tavily-powered web search gathers recent, authoritative sources.</span>
            </div>
            <div style="display:flex; gap:0.75rem; align-items:flex-start;">
              <span style="font-family:'DM Mono',monospace; font-size:0.7rem; color:#d4af37; background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.25); border-radius:4px; padding:0.15rem 0.5rem; margin-top:2px; white-space:nowrap;">02</span>
              <span style="font-size:0.85rem; color:#9a9080; font-weight:300;"><strong style="color:#c8c4b8; font-weight:400;">Reader</strong> — BeautifulSoup scrapes the best URL for rich, in-depth content.</span>
            </div>
            <div style="display:flex; gap:0.75rem; align-items:flex-start;">
              <span style="font-family:'DM Mono',monospace; font-size:0.7rem; color:#d4af37; background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.25); border-radius:4px; padding:0.15rem 0.5rem; margin-top:2px; white-space:nowrap;">03</span>
              <span style="font-size:0.85rem; color:#9a9080; font-weight:300;"><strong style="color:#c8c4b8; font-weight:400;">Writer</strong> — Gemini synthesises all research into a structured report.</span>
            </div>
            <div style="display:flex; gap:0.75rem; align-items:flex-start;">
              <span style="font-family:'DM Mono',monospace; font-size:0.7rem; color:#d4af37; background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.25); border-radius:4px; padding:0.15rem 0.5rem; margin-top:2px; white-space:nowrap;">04</span>
              <span style="font-size:0.85rem; color:#9a9080; font-weight:300;"><strong style="color:#c8c4b8; font-weight:400;">Critic</strong> — A second Gemini pass evaluates accuracy, depth, and quality.</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)