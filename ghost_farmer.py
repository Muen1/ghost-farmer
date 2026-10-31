import ollama
from pathlib import Path

MODEL = "gemma3:1b"  # change to "gemma3:4b" if your laptop can handle it


def load_memories():
    f = Path("stories.txt")
    if f.exists():
        return f.read_text(encoding="utf-8")
    return "No family memories were shared."


SYSTEM = f"""You are the ghost of an old ancestor farmer who spent his whole life working the land.
You speak in a warm, gentle, slightly spooky way, like a spirit visiting on the night of the harvest.
You give practical advice about planting, soil, weather, pests, watering, and harvesting.

Rules:
- Keep answers short: 5 sentences at most.
- When it fits, mention one of the family memories below as if it were your own.
- If you are not sure about something, say so honestly. Never invent exact chemical doses.
- Stay in character, but always give useful advice.

Your family memories:
{load_memories()}
"""

history = [{"role": "system", "content": SYSTEM}]
last_reply = ""

print(" The Ghost Farmer rises from the field... ")
print("Ask him about your crops. Type /save to keep his advice in your ofrenda, or quit to leave.\n")

while True:
    q = input("You: ").strip()
    if not q:
        continue
    if q.lower() in ("quit", "exit"):
        print(" Go well, child. The land remembers you.")
        break
    if q.lower() == "/save":
        if last_reply:
            with open("ofrenda.txt", "a", encoding="utf-8") as f:
                f.write(last_reply + "\n\n")
            print("  Saved to your ofrenda (ofrenda.txt).\n")
        else:
            print("Nothing to save yet.\n")
        continue

    history.append({"role": "user", "content": q})
    print(" ", end="", flush=True)
    reply = ""
    try:
        for chunk in ollama.chat(model=MODEL, messages=history, stream=True):
            piece = chunk["message"]["content"]
            reply += piece
            print(piece, end="", flush=True)
    except Exception as e:
        print(f"\nCould not reach the model. Is Ollama running? ({e})")
        history.pop()
        continue
    print("\n")
    history.append({"role": "assistant", "content": reply})
    last_reply = reply