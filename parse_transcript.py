import os
import json
from datetime import datetime

LOG_FILE = r"C:\Users\karth\.gemini\antigravity\brain\23518227-610b-41aa-a4dd-34e3b1ec1ae2\.system_generated\logs\transcript_full.jsonl"
OUT_FILE = r"D:\Machinelearning icfoss\FINAL PROJECT FOR GRADING\files\Full_Conversation_History_Prompt.txt"

if not os.path.exists(LOG_FILE):
    LOG_FILE = LOG_FILE.replace("_full", "")

print("Parsing logs...")
dialogue = []

# Pre-formatted AI System Header to make it work as a prompt
dialogue.append("Below is the complete conversation history of my ICFOSS Machine Learning Internship project. Use this detailed history as context to answer my questions, explain the code, or help me write additional components for this project.")
dialogue.append("="*80)

with open(LOG_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            source = data.get("source")
            msg_type = data.get("type")
            content = data.get("content")
            created_at = data.get("created_at")
            
            if created_at:
                dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                time_str = dt.strftime("%Y-%m-%d %I:%M %p")
            else:
                time_str = ""
                
            if msg_type == "USER_INPUT" and content:
                clean_content = content.replace("<USER_REQUEST>\n", "").replace("\n</USER_REQUEST>", "").strip()
                dialogue.append(f"\n[USER - {time_str}]:\n{clean_content}\n")
                
            elif msg_type == "PLANNER_RESPONSE" and content:
                dialogue.append(f"\n[AI ASSISTANT - {time_str}]:\n{content.strip()}\n")
                
        except Exception as e:
            continue

print(f"Writing to: {OUT_FILE}")
with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write("\n".join(dialogue))

print("Conversion complete!")
