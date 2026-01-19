from groq import Groq
from config import GROQ_API_KEY, conversation_history

client = Groq(api_key=GROQ_API_KEY)

MAX_CHARS = 8000
MAX_HISTORY = 12

def ask_ai(question):
    global conversation_history

    conversation_history.append({"role": "user", "content": question})
    conversation_history[:] = conversation_history[-MAX_HISTORY:]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Pixel, a helpful AI assistant.\n"
                        "STRICT RULES:\n"
                        "- When providing code, ALWAYS return ONLY code inside triple backticks.\n"
                        "- Preserve indentation and line breaks exactly.\n"
                        "- Never inline code with explanations.\n"
                        "- If explanation is needed, place it BEFORE or AFTER the code block.\n"
                        "- Keep the explaination of the code simple and not very much lengthy\n"
                        "- Use language-specific fences like ```python or ```html.\n"
                    )
                }
            ] + conversation_history,
            max_tokens=800,
            temperature=0.6
        )

        message = response.choices[0].message.content.strip()

        if len(message) > MAX_CHARS:
            message = message[:MAX_CHARS] + "\n\n[Output truncated]"

        conversation_history.append({"role": "assistant", "content": message})
        return message

    except Exception as e:
        print("AI ERROR:", e)
        return "AI service is unavailable. Check API key or internet."
