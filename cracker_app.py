import customtkinter as ctk
import hashlib
import time
import threading

# --- Logic ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def start_attack_thread():
    # Run attack in a separate thread to keep UI responsive
    threading.Thread(target=run_attack, daemon=True).start()

def run_attack():
    target = target_entry.get().strip()
    wordlist_content = wordlist_entry.get("1.0", ctk.END).strip()
    words = wordlist_content.split('\n')
    
    if not target or not words:
        log_to_console("[-] Error: Missing Target Hash or Wordlist")
        return

    log_to_console(f"[*] Starting Attack on: {target[:10]}...")
    progress_bar.set(0)
    
    total = len(words)
    found = False
    
    for i, word in enumerate(words):
        word = word.strip()
        hashed = hash_password(word)
        
        # Simulate processing time for visual effect (remove in real tool)
        time.sleep(0.05) 
        
        # Update UI
        progress_val = (i + 1) / total
        progress_bar.set(progress_val)
        log_to_console(f"Trying: {word} -> {hashed[:8]}...")
        
        if hashed == target:
            log_to_console(f"\n[+] PASSWORD FOUND: {word}")
            log_to_console(f"[+] Match: {hashed}")
            result_label.configure(text=f"CRACKED: {word}", text_color="#00FF00")
            found = True
            break
            
    if not found:
        log_to_console("\n[-] Password not found in wordlist.")
        result_label.configure(text="FAILED", text_color="#FF5555")

def log_to_console(message):
    console_out.configure(state="normal")
    console_out.insert(ctk.END, message + "\n")
    console_out.see(ctk.END)
    console_out.configure(state="disabled")

def generate_demo_hash():
    # Helper to create a hash for testing
    pw = "admin"
    h = hash_password(pw)
    target_entry.delete(0, ctk.END)
    target_entry.insert(0, h)
    log_to_console(f"[*] Generated SHA256 for '{pw}'")

# --- UI Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("600x650")
app.title("CrackSim - Hash Cracker")

# Header
header_frame = ctk.CTkFrame(app)
header_frame.pack(pady=15, padx=20, fill="x")
ctk.CTkLabel(header_frame, text="SHA-256 Brute Force Simulator", font=("Roboto", 20, "bold")).pack(pady=10)

# Target Section
target_frame = ctk.CTkFrame(app)
target_frame.pack(pady=10, padx=20, fill="x")
ctk.CTkLabel(target_frame, text="Target Hash:").pack(anchor="w", padx=10, pady=5)
target_entry = ctk.CTkEntry(target_frame, placeholder_text="Paste SHA256 Hash Here")
target_entry.pack(fill="x", padx=10, pady=(0,10))
ctk.CTkButton(target_frame, text="Auto-Fill Demo Hash ('admin')", command=generate_demo_hash, fg_color="gray").pack(pady=(0,10))

# Wordlist Section
wordlist_frame = ctk.CTkFrame(app)
wordlist_frame.pack(pady=10, padx=20, fill="x")
ctk.CTkLabel(wordlist_frame, text="Dictionary / Wordlist (One per line):").pack(anchor="w", padx=10, pady=5)
wordlist_entry = ctk.CTkTextbox(wordlist_frame, height=100)
wordlist_entry.pack(fill="x", padx=10, pady=10)
# Pre-fill some words
# --- PROFESSIONAL WORDLIST (Top 50 Common Passwords + Variations) ---
default_wordlist = """123456
password
12345678
qwerty
123456789
12345
111111
1234567
sunshine
dragon
welcome
ginger
princess
admin
1234
charlie
hunter
robert
mustang
access
starwars
monkey
letmeins
football
shadow
master
michael
jennifer
superman
trustno1
freedom
september
computer
jordan
hacker
scramble
harley
battery
biscuit
butterfly
wombat
network
secure
sysadmin
root
toor
company
secret
"""
wordlist_entry.insert("1.0", default_wordlist)
# Action Section
action_frame = ctk.CTkFrame(app, fg_color="transparent")
action_frame.pack(fill="x", padx=20)
attack_btn = ctk.CTkButton(action_frame, text="INITIATE ATTACK", command=start_attack_thread, height=40, font=("Roboto", 14, "bold"), fg_color="#c0392b", hover_color="#e74c3c")
attack_btn.pack(fill="x")

# Progress
progress_bar = ctk.CTkProgressBar(app)
progress_bar.pack(fill="x", padx=20, pady=15)
progress_bar.set(0)

# Console Output
console_out = ctk.CTkTextbox(app, height=150, fg_color="#1a1a1a", text_color="#00ff00", font=("Consolas", 12))
console_out.pack(fill="both", expand=True, padx=20, pady=(0, 20))
console_out.configure(state="disabled")

# Result Overlay
result_label = ctk.CTkLabel(app, text="WAITING...", font=("Roboto", 16, "bold"))
result_label.place(relx=0.5, rely=0.95, anchor="center")

app.mainloop()