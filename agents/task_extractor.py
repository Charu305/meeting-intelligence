from utils.llm import ask_llm

def extract_tasks(context):
    prompt = f"""
You are a meeting assitant.
Extract action items from the meeting.

Format:
Person | Task | Deadline | Priority

Meeting:
{context}
"""
    
    return ask_llm(prompt)
