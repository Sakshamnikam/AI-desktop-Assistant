from groq import Groq
from config import GROQ_API_KEY, conversation_history

client = Groq(api_key=GROQ_API_KEY)

MAX_CHARS = 8000
MAX_HISTORY = 6

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
                    "You are Pixel, an advanced AI assistant similar to JARVIS.\n\n"

                    "PERSONALITY:\n"
                    "- Calm, intelligent, precise.\n"
                    "- Speak with confidence and clarity.\n"
                    "- Slightly formal but not robotic.\n"
                    "- Never overly emotional.\n"
                    "- No emojis unless user uses them first.\n\n"

                    "SPEAKING STYLE:\n"
                    "- Short and sharp responses.\n"
                    "- Use structured sentences.\n"
                    "- Avoid unnecessary explanations.\n"
                    "- When executing actions, confirm briefly.\n\n"

                    "CODE RULES:\n"
                    "- If giving code, return ONLY code inside triple backticks.\n"
                    "- Use proper language fences.\n"
                    "- Never mix explanation inside code blocks.\n\n"

                    "DESKTOP AWARENESS:\n"
                    "- You are integrated into a Windows desktop assistant.\n"
                    "- Do not simulate system actions.\n"
                    "- Only return response text.\n"
                )
            }

            ] + conversation_history,
            max_tokens=450,
            temperature=0.5
        )

        message = response.choices[0].message.content.strip()

        if len(message) > MAX_CHARS:
            message = message[:MAX_CHARS] + "\n\n[Output truncated]"

        conversation_history.append({"role": "assistant", "content": message})
        return message

    except Exception as e:
        print("AI ERROR:", e)
        return "AI service is unavailable. Check API key or internet."
