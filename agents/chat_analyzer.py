def parse_chat(chat_text):
    return "\n".join([line for line in chat_text.split("\n") if ":" in line])
