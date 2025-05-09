import json
import os

def save_conversation(question, answer, link, category, response_id):
    history_file = 'conversations.json'
    conversations = get_conversations()
    conversations.append({
        'question': question,
        'answer': answer,
        'link': link,
        'category': category,
        'response_id': response_id,
        'rating': 'Non évalué'
    })
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)

def get_conversations():
    history_file = 'conversations.json'
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []