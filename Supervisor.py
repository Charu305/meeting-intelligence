from agents.transcriber import transcribe
from agents.silde_reader import read_slides
from agents.chat_analyzer import parse_chat
from agents.rag_memory import store_context, retrieve
from agents.task_extractor import extract_tasks
from agents.decision_agent import should_send_email
from agents.email_writer import generate_email
from mcp_tools import send_email


def run_meeting(audio, ppt, chat):

    transcript = transcribe(audio)
    slides = read_slides(ppt)
    chats = parse_chat(chat)

    full_context = transcript + "\n" + slides + "\n" + chats

    store_context(full_context)
    context = retrieve("who should do what tasks")

    tasks = extract_tasks(context)
    decision = should_send_email(tasks)

    email_text = None

    if decision.strip().upper() == "YES":
        email_text = generate_email(tasks)

        # call MCP tool (real email action)
        send_email(
            "charu2830@gmail.com",
            "Meeting Follow-up",
            email_text
        )

    return tasks, decision, email_text
