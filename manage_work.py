import os
import json
import sys
from collections import Counter

# --- CONFIGURATION ---
# Path where Label Studio exports are stored
EXPORT_DIR = "/home/levi/Documents/Export"

def get_files():
    """Retrieves a list of JSON files from the export directory."""
    try:
        files = [f for f in os.listdir(EXPORT_DIR) if f.endswith('.json')]
        if not files:
            print(f"[-] No JSON files found in {EXPORT_DIR}")
            return None
        return sorted(files)
    except FileNotFoundError:
        print(f"[!] Directory not found: {EXPORT_DIR}")
        return None

def clean_file(filename):
    """Filters out tasks that do not contain any annotations."""
    path = os.path.join(EXPORT_DIR, filename)
    output_path = os.path.join(EXPORT_DIR, f"cleaned_{filename}")
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    # Keep only tasks where the 'annotations' list is not empty
    labeled_only = [t for t in data if t.get('annotations') and len(t['annotations']) > 0]
    
    with open(output_path, 'w') as f:
        json.dump(labeled_only, f, indent=2)
    
    print(f"\n[+] Cleaning Complete: Kept {len(labeled_only)} of {len(data)} tasks.")
    print(f"[*] File saved to: {output_path}")

def inspect_file(filename):
    """Analyzes the distribution of NER labels within the selected file."""
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, 'r') as f:
        data = json.load(f)

    all_labels = []
    for item in data:
        # Navigate the Label Studio JSON structure to find labeled entities
        for ann in item.get('annotations', []):
            for result in ann.get('result', []):
                if 'value' in result and 'labels' in result['value']:
                    all_labels.extend(result['value']['labels'])

    label_counts = Counter(all_labels)
    print(f"\n[i] Inspection: {filename} ({len(data)} total tasks)")
    print("-" * 40)
    for label, count in label_counts.most_common():
        print(f"{label:<20}: {count}")
    print("-" * 40)

def main():
    """Main CLI entry point for the Management Tool."""
    files = get_files()
    if not files:
        return

    print("\n--- DATA MANAGEMENT CONSOLE ---")
    for i, f in enumerate(files):
        print(f"[{i}] {f}")

    try:
        f_idx = int(input("\nSelect file index: "))
        selected_file = files[f_idx]
        
        print(f"\nAction for '{selected_file}':")
        print("1. Clean (Filter annotated data)")
        print("2. Inspect (Analyze label distribution)")
        
        action = input("Selection: ")
        
        if action == "1":
            clean_file(selected_file)
        elif action == "2":
            inspect_file(selected_file)
        else:
            print("[!] Invalid action selected.")
            
    except (ValueError, IndexError):
        print("[!] Input Error: Please enter a valid number from the list.")

if __name__ == "__main__":
    main()
