import tkinter as tk
from tkinter import ttk, scrolledtext
import asyncio
import threading
from datetime import datetime
from core.database import Database
from core.types import TaskStatus

class NexusGUI:
    def __init__(self, brain, voice):
        self.brain = brain
        self.voice = voice
        self.db = Database()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Nexus - Universal Digital Agent")
        self.root.geometry("900x600")
        self.root.configure(bg='#0f172a')
        
        # Make window appear on top
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#0f172a')
        style.configure('Dark.TLabel', background='#0f172a', foreground='#38bdf8', font=('Arial', 10))
        style.configure('Title.TLabel', background='#0f172a', foreground='#38bdf8', font=('Arial', 16, 'bold'))
        
        self.setup_ui()
        self.update_task_list()
        
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.root, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = ttk.Label(header_frame, text="NEXUS", style='Title.TLabel')
        title.pack(side=tk.LEFT)
        
        status = ttk.Label(header_frame, text="● ACTIVE", style='Dark.TLabel', foreground='#22c55e')
        status.pack(side=tk.RIGHT)
        
        # Command Input
        input_frame = ttk.Frame(self.root, style='Dark.TFrame')
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(input_frame, text="Command:", style='Dark.TLabel').pack(anchor=tk.W)
        
        self.command_entry = tk.Entry(input_frame, bg='#1e293b', fg='#e2e8f0', font=('Arial', 11), 
                                      insertbackground='#38bdf8', relief=tk.FLAT, bd=5)
        self.command_entry.pack(fill=tk.X, pady=5)
        self.command_entry.bind('<Return>', lambda e: self.submit_command())
        
        submit_btn = tk.Button(input_frame, text="Execute", command=self.submit_command,
                              bg='#38bdf8', fg='#0f172a', font=('Arial', 10, 'bold'),
                              relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        submit_btn.pack(pady=5)
        
        # Task List
        task_frame = ttk.Frame(self.root, style='Dark.TFrame')
        task_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(task_frame, text="Task Queue:", style='Dark.TLabel').pack(anchor=tk.W)
        
        # Scrolled text for tasks
        self.task_display = scrolledtext.ScrolledText(task_frame, bg='#1e293b', fg='#e2e8f0',
                                                       font=('Consolas', 9), relief=tk.FLAT,
                                                       wrap=tk.WORD, height=20)
        self.task_display.pack(fill=tk.BOTH, expand=True, pady=5)
        self.task_display.config(state=tk.DISABLED)
        
        # Voice Status
        voice_frame = ttk.Frame(self.root, style='Dark.TFrame')
        voice_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.voice_status = ttk.Label(voice_frame, text="🎤 Voice: Listening for 'Nexus'...", 
                                      style='Dark.TLabel', foreground='#22c55e')
        self.voice_status.pack()
        
        # Auto-refresh tasks every 2 seconds
        self.root.after(2000, self.auto_refresh)
        
    def submit_command(self):
        command = self.command_entry.get().strip()
        if command:
            print(f"[GUI] Command received: {command}")
            self.command_entry.delete(0, tk.END)
            
            # Schedule the async task in the main event loop
            def run_async():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.brain.process_input(command))
                finally:
                    loop.close()
            
            threading.Thread(target=run_async, daemon=True).start()
            
            # Force immediate refresh
            self.root.after(500, self.update_task_list)
            
    def update_task_list(self):
        tasks = self.db.get_all_tasks()
        
        self.task_display.config(state=tk.NORMAL)
        self.task_display.delete(1.0, tk.END)
        
        if not tasks:
            self.task_display.insert(tk.END, "No tasks yet. Say 'Nexus' or type a command above.\n")
        else:
            for task in tasks[:20]:  # Show last 20 tasks
                status_color = {
                    'pending': '🟡',
                    'running': '🔵',
                    'completed': '🟢',
                    'failed': '🔴'
                }.get(task.status.value, '⚪')
                
                self.task_display.insert(tk.END, f"{status_color} {task.status.value.upper()}\n", 'status')
                self.task_display.insert(tk.END, f"   {task.description}\n", 'desc')
                if task.result:
                    self.task_display.insert(tk.END, f"   ✓ {task.result}\n", 'result')
                if task.error:
                    self.task_display.insert(tk.END, f"   ✗ {task.error}\n", 'error')
                self.task_display.insert(tk.END, "\n")
        
        self.task_display.tag_config('status', foreground='#38bdf8')
        self.task_display.tag_config('desc', foreground='#e2e8f0')
        self.task_display.tag_config('result', foreground='#22c55e')
        self.task_display.tag_config('error', foreground='#ef4444')
        
        self.task_display.config(state=tk.DISABLED)
        self.task_display.see(tk.END)
        
    def auto_refresh(self):
        self.update_task_list()
        self.root.after(2000, self.auto_refresh)
        
    def run(self):
        self.root.mainloop()
