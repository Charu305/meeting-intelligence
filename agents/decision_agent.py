from utils.llm import ask_llm

def should_send_email(tasks):

    prompt = f"""
Do these tasks require notifying participants?

Reply ONLY: YES or NO

Tasks:
{tasks}
"""

    return ask_llm(prompt).strip()
