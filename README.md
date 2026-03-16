# 🧠 Meeting Intelligence — Supervisor Agent + Email Notification

> **A production-grade AI application** that transforms raw meeting transcripts into structured intelligence — using a **Supervisor Agent architecture** to orchestrate specialised sub-agents for summarisation, action item extraction, decision capture, and sentiment analysis, with automated **email delivery** of the final report via SMTP.

---

## 📌 Project Overview

Organisations lose enormous value from meetings — decisions made, actions assigned, and context shared that never gets properly captured or followed up on. This project builds an **automated meeting intelligence system** that turns a meeting transcript into a complete, structured intelligence report and delivers it directly to stakeholders via email.

The system uses a **Supervisor Agent pattern** — a master orchestrator that routes the transcript to specialised sub-agents, collects their outputs, assembles a full report, and sends it automatically to the specified recipients.

---

## 🎯 Problem Statement

> *Given a meeting transcript, automatically extract structured intelligence — summary, action items, decisions, and sentiment — and email the final report to participants.*

**Real-world impact:**
- **Saves 30–60 minutes** of manual note-taking per meeting
- **Eliminates lost action items** — every task is captured and attributed
- **Improves accountability** — owner + deadline extracted from conversation
- **Enables async teams** — non-attendees get full context via email instantly

---

## 🏗️ System Architecture

```
Meeting Transcript (text input)
            │
            ▼
┌──────────────────────────────────────────┐
│            app.py  (Streamlit UI)         │
│  Upload transcript, enter recipient      │
│  email, trigger analysis, view report    │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│           Supervisor.py                  │
│           SUPERVISOR AGENT               │
│                                          │
│  Receives full transcript                │
│  Routes to specialised sub-agents        │
│  Collects and assembles outputs          │
│  Passes final report to email sender     │
└──────┬──────────┬──────────┬─────────────┘
       │          │          │
       ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│Summariser│ │ Action   │ │  Sentiment   │
│ Agent    │ │ Extractor│ │  Analyser    │
│          │ │ Agent    │ │  Agent       │
│Generates │ │Extracts  │ │Analyses tone │
│concise   │ │tasks with│ │& engagement  │
│summary   │ │owner +   │ │across the    │
│          │ │deadline  │ │meeting       │
└──────────┘ └──────────┘ └──────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│           mcp_tools.py                   │
│           EMAIL DELIVERY                 │
│                                          │
│  Sends the assembled intelligence        │
│  report to specified recipients          │
│  via Gmail SMTP (smtplib)                │
└──────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
meeting-intelligence/
│
├── app.py                    # Streamlit web UI — upload transcript, view report
├── Supervisor.py             # Supervisor agent — orchestrates all sub-agents
├── mcp_tools.py              # Email delivery — sends report via Gmail SMTP
├── agents/                   # Specialised sub-agents
│   ├── summariser.py         # Generates concise meeting summary
│   ├── action_extractor.py   # Extracts action items with owner + deadline
│   ├── decision_extractor.py # Identifies key decisions made
│   └── sentiment_analyser.py # Analyses tone and engagement
├── utils/                    # Shared utility functions
│   ├── transcript_parser.py  # Cleans and structures raw transcript text
│   ├── llm_client.py         # LLM API wrapper (model-agnostic)
│   └── prompt_templates.py   # All prompts centralised
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
└── Presentation1.pptx        # Project presentation deck
```

---

## 🔬 Technical Deep Dive

### 1. Supervisor Agent Pattern (`Supervisor.py`)

The **Supervisor Agent** implements the **Supervisor-Worker pattern** — a master orchestrator that manages the full pipeline:

```
Transcript → Supervisor → invokes sub-agents in sequence
                       → Summariser Agent      → Summary text
                       → Action Extractor      → Action items JSON
                       → Decision Extractor    → Decisions list
                       → Sentiment Analyser    → Sentiment report
                       → assembles full report
                       → passes to mcp_tools.py for email delivery
```

**Why a Supervisor instead of a flat pipeline?**

| Flat Sequential Pipeline | Supervisor Pattern |
|---|---|
| All steps run regardless of what's needed | Supervisor can selectively invoke agents |
| No coordination or conflict resolution | Supervisor owns output assembly |
| Hard to extend — adding an agent breaks flow | New agents plug in without touching existing ones |
| No retry logic | Supervisor can handle agent failures gracefully |

### 2. Specialised Sub-Agents (`agents/`)

Each agent has a single, tightly scoped responsibility and its own prompt:

**Summariser Agent** — Takes the full transcript and produces a concise narrative summary covering context, key topics, outcomes, and open questions.

**Action Extractor Agent** — Scans for action commitments (*"I'll send that by Friday"*, *"Can you follow up on...?"*) and returns structured output: `{task, owner, deadline, priority}`.

**Decision Extractor Agent** — Identifies moments where a decision was explicitly made or agreed upon. Returns: `{decision, context, agreed_by}`. Tuned to distinguish decisions from ongoing discussions.

**Sentiment Analyser Agent** — Analyses tone and engagement across the transcript. Detects overall sentiment, energy level, conflict moments, and consensus points.

### 3. Email Delivery (`mcp_tools.py`)

The `mcp_tools.py` file handles automated delivery of the assembled intelligence report via **Gmail SMTP** using Python's built-in `smtplib`:

```python
import smtplib
from email.message import EmailMessage

def send_email(to, subject, body):
    sender = "your_email@gmail.com"
    password = os.environ.get("GMAIL_APP_PASSWORD")  # stored as env variable
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
    return "Email sent successfully"
```

Once the Supervisor assembles the final intelligence report, it calls `send_email()` to automatically deliver it to the specified recipient(s) — closing the loop from transcript to actionable report in the recipient's inbox.

> ⚠️ **Security note:** Never hardcode credentials. Always store the Gmail app password as an environment variable (`GMAIL_APP_PASSWORD`) and reference it via `os.environ.get()`. Add `.env` to `.gitignore`.

### 4. Utility Layer (`utils/`)

**`transcript_parser.py`** — Normalises raw transcript formats (plain text, timestamped, speaker-labelled) into a standard structure all agents can consume.

**`llm_client.py`** — Model-agnostic LLM wrapper. All agents call `llm_client.generate(prompt)` — swapping from GPT-4 to Gemini or Claude requires changing one config value.

**`prompt_templates.py`** — All agent prompts stored centrally. Prompt logic is fully separated from agent orchestration logic — prompts can be iterated without touching agent code.

### 5. Docker Containerisation (`Dockerfile`)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

The full system — Supervisor, sub-agents, email delivery, and UI — is packaged as a single container for consistent, reproducible deployment anywhere.

---

## 📊 Sample Output (emailed report)

```
Subject: Meeting Intelligence Report — Product Review Sync

📝 SUMMARY
The team reviewed Q3 product performance and aligned on Q4 roadmap
priorities. Discussion centred on the delayed mobile feature release
and the decision to deprioritise the analytics dashboard...

✅ ACTION ITEMS
• Write mobile release brief — Priya — due Oct 15
• Revise Q4 roadmap deck — Arjun — due Oct 12
• Schedule UX review — Meera — this week

🎯 KEY DECISIONS
• Mobile feature release pushed to Q4 Week 2
• Analytics dashboard deprioritised for Q4
• Weekly sync moved to Thursdays

💬 SENTIMENT
Overall tone: Constructive (7.2/10)
Engagement: High — active participation from all attendees
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.11 |
| Agent Architecture | Custom Supervisor-Worker pattern |
| LLM | OpenAI GPT / Google Gemini (via `llm_client.py`) |
| Email Delivery | Python `smtplib` + Gmail SMTP |
| Web UI | Streamlit |
| Containerisation | Docker |

---

## 🚀 How to Run

### Option A — Local

```bash
git clone https://github.com/Charu305/meeting-intelligence.git
cd meeting-intelligence

# Store credentials securely — never hardcode
export OPENAI_API_KEY="your-llm-api-key"
export GMAIL_APP_PASSWORD="your-gmail-app-password"

pip install -r requirements.txt
streamlit run app.py
```

### Option B — Docker

```bash
docker build -t meeting-intelligence .
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-llm-api-key" \
  -e GMAIL_APP_PASSWORD="your-gmail-app-password" \
  meeting-intelligence
```

---

## 💡 Key Learnings & Takeaways

- **Supervisor pattern scales gracefully** — adding a new agent (e.g., a Follow-up Question Generator) requires only adding a new file in `agents/` and registering it with the Supervisor — no other code changes needed.
- **Single-responsibility agents outperform monolithic prompts** — asking one LLM call to simultaneously summarise, extract actions, identify decisions, and analyse sentiment produces mediocre results at each task. Focused agents with dedicated prompts excel individually.
- **Centralised prompt templates are essential** — storing all prompts in `prompt_templates.py` means prompt iteration (the most frequent activity in LLM app development) never requires touching orchestration code.
- **Model-agnostic LLM client is non-negotiable** — wrapping the API in `llm_client.py` means switching from GPT-4 to Gemini for cost reasons requires one line change, not refactoring every agent.
- **Automated delivery closes the loop** — displaying results in a UI is useful; emailing them to every participant the moment the meeting ends is what turns a demo into a genuinely useful tool.
- **Credential management matters from day one** — any application that connects to external services (LLM APIs, SMTP servers) must handle secrets via environment variables, never hardcoded values.

---

## 🔮 Potential Enhancements

- **Audio ingestion** — add OpenAI Whisper for direct audio/video transcription before the agent pipeline
- **Real-time processing** — stream live meeting audio and update the report in real time
- **Speaker diarisation** — attribute sentiment and actions to specific speakers automatically
- **Calendar integration** — extend `mcp_tools.py` to also create calendar events for follow-up meetings
- **Multi-meeting tracking** — track open action items and recurring themes across a series of meetings

---

## 👩‍💻 Author

**Charunya** 
🔗 [GitHub Profile](https://github.com/Charu305)

---

## 📄 License

This project is developed for educational and research purposes.
