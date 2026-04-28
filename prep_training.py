import json
import spacy
from spacy.tokens import DocBin
import os

# --- SETTINGS ---
INPUT_FILE = "labeled_data.json"
OUTPUT_FILE = "train.spacy"
# ----------------

def convert():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Error: {INPUT_FILE} not found. Please check your folder.")
        return

    # Create a blank English model
    nlp = spacy.blank("en")
    db = DocBin()
    
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    count = 0
    skipped = 0

    print(f"[*] Converting {len(data)} tasks to spaCy format...")

    for item in data:
        text = item['data']['text']
        doc = nlp.make_doc(text)
        entities = []
        
        # Navigate Label Studio's JSON structure
        for ann in item.get('annotations', []):
            for result in ann.get('result', []):
                value = result.get('value', {})
                start = value.get('start')
                end = value.get('end')
                labels = value.get('labels')

                if start is not None and end is not None and labels:
                    # Create a span for the entity
                    span = doc.char_span(start, end, label=labels[0], alignment_mode="contract")
                    if span is None:
                        skipped += 1
                    else:
                        entities.append(span)
        
        try:
            doc.ents = entities
            db.add(doc)
            count += 1
        except Exception as e:
            skipped += 1

    # Save to disk
    db.to_disk(OUTPUT_FILE)
    print("\n" + "="*30)
    print(f"✅ SUCCESS: {count} examples processed.")
    print(f"⚠️ SKIPPED: {skipped} examples (alignment issues).")
    print(f"📂 SAVED TO: {OUTPUT_FILE}")
    print("="*30)

if __name__ == "__main__":
    convert()
