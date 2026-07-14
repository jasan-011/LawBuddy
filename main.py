import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import os
import json
import urllib.request
import urllib.error
import time
import re
import math
import random
import threading

# 1. API Key Matrix Verification
API_KEY = os.environ.get("GEMINI_API_KEY")

# 2. Frame System Blueprint
root = tk.Tk()
root.title("LawBuddy - Indian Legal Literacy Terminal")
root.geometry("1200x700")
root.resizable(False, False)
root.configure(bg="#000000") # Pure Void Black

SYSTEM_PROMPT = """You are LawBuddy, an elite Indian Legal Literacy Assistant. 
Always answer strictly based on current valid Indian laws (e.g., Bharatiya Nyaya Sanhita (BNS), Consumer Protection Act).
Format your answers cleanly using clear bullet points. Explain complex terms in simple words.
You must not provide direct legal advice. Provide information only."""

# 3. Secure Data Packet API Routing Protocol (With Auto-Failover)
def ask_gemini(query, use_search):
    if not API_KEY:
        return "ERROR: Missing GEMINI_API_KEY environment variable. Run 'set GEMINI_API_KEY=your_key' in CMD first."
    
    # Fully upgraded to active model variants
    models_to_try = [
        "gemini-3.5-flash", 
        "gemini-3.1-flash-lite"
    ]
    
    headers = {"Content-Type": "application/json", "x-goog-api-key": API_KEY}
    
    for model_index, model_name in enumerate(models_to_try):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        
        payload = {
            "contents": [{"parts": [{"text": query}]}],
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]}
        }
        if use_search:
            payload["tools"] = [{"googleSearch": {}}]

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
                
        except urllib.error.HTTPError as e:
            # Safely catch deprecated/overloaded endpoints to cascade to backup models
            if (e.code in [404, 429, 503]) and model_index < len(models_to_try) - 1:
                next_model = models_to_try[model_index + 1]
                
                # Render rerouting matrix trace log into terminal display window
                chat_display.configure(state='normal')
                chat_display.insert(
                    tk.END, 
                    f"\n[SYSTEM_NOTICE]: DEPLOYING COGNITIVE BRIDGE... MODEL '{model_name}' RETRIED WITH CODE {e.code}.\n[SYSTEM_RE-ROUTE]: DIVERTING PACKETS TO '{next_model}'...\n\n", 
                    "bold_style"
                )
                chat_display.configure(state='disabled')
                root.update()
                
                # Advance tracking index assignment loop
                continue
                
            try:
                error_msg = e.read().decode('utf-8')
            except Exception:
                error_msg = "Unknown API Error Context"
            return f"API Error {e.code}: {error_msg}"
        except Exception as e:
            return f"Network Connection Failure: {str(e)}"
            
    return "ERROR: All cognitive server cores are currently unresponsive. Please check your network or API configurations."

# 4. Sharp Markdown Processing Log Matrix
def insert_markdown_text(widget, text):
    widget.configure(state='normal')
    lines = text.split('\n')
    for line in lines:
        if line.strip() in ['***', '---', '___']:
            widget.insert(tk.END, "\n" + "="*70 + "\n\n", "divider_style")
            continue
        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading_match:
            widget.insert(tk.END, f"\n>>> {heading_match.group(2).upper()} <<<\n", "heading_style")
            continue
        parts = re.split(r'(\*\*.*?\*\*)', line)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                widget.insert(tk.END, part[2:-2], "bold_style")
            else:
                widget.insert(tk.END, part, "normal_style")
        widget.insert(tk.END, "\n")
    widget.configure(state='disabled')
    widget.see(tk.END)

# 5. Core Application Execution Pipeline
def handle_submit(event=None):
    user_input_text = entry_box.get().strip()
    if not user_input_text:
        return
        
    # 1. Clear input box and display user message immediately
    entry_box.delete(0, tk.END)
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"\n[USER]: {user_input_text}\n", "user_style")
    
    # 2. Show a dynamic matrix loading indicator so they know it's working
    chat_display.insert(tk.END, "[SYSTEM]: COMPUTING RESPONSE VECTORS...\n", "bold_style")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)
    
    # Read the search parameter toggle state directly from UI matrix
    is_search_active = search_var.get()
    
    # 3. Spawn a background thread for the API call so the GUI never lags
    threading.Thread(target=async_api_worker, args=(user_input_text, is_search_active), daemon=True).start()

def async_api_worker(query, use_search):
    # Call your existing ask_gemini function (runs safely in background)
    ai_response = ask_gemini(query, use_search=use_search)
    
    # Safely push the result back into the main GUI thread window
    root.after(0, update_chat_ui, ai_response)

def update_chat_ui(response_text):
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"\n[LAWBUDDY]:\n", "bot_header_style")
    chat_display.configure(state='disabled')
    # Run the response through markdown layout processors
    insert_markdown_text(chat_display, response_text)
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, "\n" + "="*70 + "\n", "divider_style")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)

# 6. Dynamic Matrix Core Layout Framing
# Left Column: Neural Synapse Analyzer
left_panel = tk.Frame(root, width=500, height=700, bg="#000000", bd=2, relief=tk.SOLID, highlightbackground="#00FF66", highlightthickness=1)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
left_panel.pack_propagate(False)

# Right Column: Programming & Decoding Engine Console
right_panel = tk.Frame(root, width=700, height=700, bg="#000000")
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
right_panel.pack_propagate(False)

# Header Title Card inside Left Panel
title_lbl = tk.Label(left_panel, text="[ NEURAL JURISDICTION MATRIX ]", bg="#000000", fg="#00FF66", font=("Courier New", 12, "bold"))
title_lbl.pack(fill=tk.X, pady=10)

# Vector Mesh Space Engine
canvas = tk.Canvas(left_panel, width=480, height=620, bg="#000500", highlightthickness=1, highlightbackground="#005511")
canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# 7. Dense High-Performance Vector Node Core Assembly
nodes_3d = []
labels = [
    "SYS.BNS_CODE", "SYS.CIVIL_PROC", "SYS.CONS_FORUM",
    "SYS.CONST_RIGHTS", "SYS.CORP_ACTS", "SYS.CYBER_JURIS",
    "SYS.FIR_LOG", "SYS.BAIL_PROC", "SYS.PROP_RIGHTS", "SYS.IT_ACT"
]

# Create Core High-Value Hubs
for i, name in enumerate(labels):
    nodes_3d.append({
        "x": int(150 * math.cos(i * (2 * math.pi / 10))),
        "y": int(150 * math.sin(i * (2 * math.pi / 10))),
        "z": random.randint(-40, 40),
        "label": name,
        "is_core": True
    })

# Add Dense Global Synapse Intersections (Ultra-Crisp Vector Logic)
random.seed(101)
for _ in range(45):
    nodes_3d.append({
        "x": random.randint(-200, 200),
        "y": random.randint(-240, 240),
        "z": random.randint(-80, 80),
        "label": "",
        "is_core": False
    })

angle_y = 0.0
angle_x = 0.25 # Sharp perspective tilt factor

def cycle_matrix_render():
    global angle_y
    canvas.delete("all")
    
    # Grid Background overlay
    for i in range(0, 500, 30):
        canvas.create_line(i, 0, i, 650, fill="#001805", width=1)
    for j in range(0, 650, 30):
        canvas.create_line(0, j, 500, j, fill="#001805", width=1)
        
    c_x, c_y = 240, 280
    projected = []
    
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    
    for node in nodes_3d:
        # Rotational calculations
        x1 = node["x"] * cos_y - node["z"] * sin_y
        z1 = node["x"] * sin_y + node["z"] * cos_y
        y2 = node["y"] * cos_x - z1 * sin_x
        z2 = node["y"] * sin_x + z1 * cos_x
        
        dist = 400
        scale = dist / (dist + z2)
        
        s_x = int(c_x + x1 * scale)
        s_y = int(c_y + y2 * scale)
        projected.append((s_x, s_y, scale, node["is_core"], node["label"]))

    # Fast Single-Pass Linear Synapse Connections
    for i, p1 in enumerate(projected):
        for j, p2 in enumerate(projected):
            if i < j:
                dx = p1[0] - p2[0]
                dy = p1[1] - p2[1]
                if dx*dx + dy*dy < (7000 if (p1[3] or p2[3]) else 2500):
                    line_color = "#005511" if not (p1[3] and p2[3]) else "#00BC44"
                    canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=line_color, width=1)

    # Render vector dots and sharp terminal text fields
    for p in projected:
        if p[3]: # Master Node Hubs
            r = max(3, int(5 * p[2]))
            canvas.create_oval(p[0]-r-2, p[1]-r-2, p[0]+r+2, p[1]+r+2, fill="", outline="#00FF66", width=1)
            canvas.create_oval(p[0]-r, p[1]-r, p[0]+r, p[1]+r, fill="#FFFFFF", outline="#00FF66")
            canvas.create_text(p[0], p[1]-r-10, text=p[4], fill="#00FF66", font=("Courier New", 8, "bold"))
        else: # Standard dense grid coordinates
            r = max(1, int(2 * p[2]))
            canvas.create_oval(p[0]-r, p[1]-r, p[0]+r, p[1]+r, fill="#00AA44", outline="")

    angle_y += 0.008
    root.after(35, cycle_matrix_render)

cycle_matrix_render()

# 8. Right Panel Modular Component Assemblies
# Top Sub-Box: Coding Console Log
console_box = tk.Frame(right_panel, bg="#000000", bd=2, relief=tk.SOLID, highlightbackground="#00FF66", highlightthickness=1)
console_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 10))

console_header = tk.Label(console_box, text=" ⚡ AGENT RESPONSE", bg="#00FF66", fg="#000000", font=("Courier New", 10, "bold"), anchor="w")
console_header.pack(fill=tk.X)

chat_display = scrolledtext.ScrolledText(
    console_box, wrap=tk.WORD, state='disabled',
    font=("Courier New", 10), bg="#000000", fg="#00FF66",
    insertbackground="#00FF66", relief=tk.FLAT, highlightthickness=0
)
chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Terminal Styling configuration mapping
chat_display.tag_config("normal_style", foreground="#00FF66")
chat_display.tag_config("user_style", foreground="#FFFFFF", font=("Courier New", 10, "bold"))
chat_display.tag_config("bot_header_style", foreground="#00FF66", font=("Courier New", 10, "bold"))
chat_display.tag_config("bold_style", foreground="#FFFFFF", font=("Courier New", 10, "bold"))
chat_display.tag_config("heading_style", foreground="#FFFFFF", font=("Courier New", 11, "bold"))
chat_display.tag_config("divider_style", foreground="#004411")

# Bottom Sub-Box: Decoding Console / Input Entry Framework
input_box = tk.Frame(right_panel, bg="#000000", bd=2, relief=tk.SOLID, highlightbackground="#00FF66", highlightthickness=1)
input_box.pack(fill=tk.X, padx=5, pady=(0, 5))

input_header = tk.Label(input_box, text=" 💾 INPUT ", bg="#00FF66", fg="#000000", font=("Courier New", 10, "bold"), anchor="w")
input_header.pack(fill=tk.X)

action_bar = tk.Frame(input_box, bg="#000000")
action_bar.pack(fill=tk.X, padx=10, pady=15)

search_var = tk.BooleanVar(value=False)
search_check = tk.Checkbutton(
    action_bar, text="[LIVE_SEARCH]", variable=search_var,
    bg="#000000", fg="#00FF66", selectcolor="#001100",
    activebackground="#000000", activeforeground="#00FF66",
    font=("Courier New", 9, "bold")
)
search_check.pack(side=tk.LEFT, padx=(0, 15))

# FIXED: Standardized to entry_box variable to match handle_submit reference loop
entry_box = tk.Entry(
    action_bar, font=("Courier New", 11), bg="#000000", fg="#00FF66", insertbackground="#00FF66",
    relief=tk.SOLID, bd=1, highlightthickness=1, highlightcolor="#00FF66", highlightbackground="#004411"
)
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=5)

# FIXED: Correctly routes return key events to the submission pipeline handler
entry_box.bind("<Return>", handle_submit)

send_button = tk.Button(
    action_bar, text="[RUN ANALYSIS]", bg="#000000", fg="#00FF66",
    activebackground="#00FF66", activeforeground="#000000",
    font=("Courier New", 10, "bold"), relief=tk.SOLID, bd=1,
    highlightthickness=1, command=handle_submit
)
send_button.pack(side=tk.RIGHT, padx=5, ipady=5, ipadx=15)

# Boot Initialized Log Stream
welcome_text = """ACCESS GRANTED // SERVER INITIALIZATION SUCCESSFUL
[SYSTEM_STATUS] : SECURE LOGS ACTIVE
[DOMAIN]        : REPUBLIC OF INDIA CENTRAL CODES

Ready for entry assignment. Enter conceptual key parameters below to compile analysis."""

chat_display.configure(state='normal')
chat_display.insert(tk.END, "[SYSTEM_NOTIFICATION]:\n", "bot_header_style")
chat_display.configure(state='disabled')
insert_markdown_text(chat_display, welcome_text)
chat_display.configure(state='normal')
chat_display.insert(tk.END, "\n" + "="*70 + "\n", "divider_style")
chat_display.configure(state='disabled')

root.mainloop()
