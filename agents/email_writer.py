from utils.llm import ask_llm

def generate_email(tasks):

    prompt = f"""
Write a professional follow-up email based on these meeting action items:

{tasks}

Keep it concise and corporate tone.
"""

    return ask_llm(prompt)
