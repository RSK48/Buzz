import json
import os
import webbrowser
import pyautogui
import time
import tkinter as tk
from tkinter import ttk, messagebox, font

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, radius=15, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.radius = radius
        self.rect = None
        self.bind("<Configure>", self._draw_rounded_rect)

    def _draw_rounded_rect(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        self.rect = self.create_round_rect(0, 0, width, height, self.radius, fill=self["bg"], outline="")

    def create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

class ChatLinkSender:
    def __init__(self, root):
        self.root = root
        self.root.title("Buzz")
        self.root.geometry("650x550")
        self.root.minsize(600, 500)
        
        # Configure root window background
        self.root.configure(bg='#181f16')
        
        # Dark theme configuration
        self.setup_styles()
        
        self.links_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat_links.json")
        self.saved_links = []
        
        self.load_saved_links()
        self.show_main_page()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Best theme for custom styling
        
        # Dark theme colors
        self.bg_color = '#181f16'  # Application background
        self.card_color = '#20241e'  # Text box/card background
        self.button_color = '#51a12f'  # Button color
        self.button_text = '#0b1706'  # Button text color
        self.text_color = '#e0e0e0'  # General text color
        self.danger_color = '#d13438'
        
        # Custom monospace font
        self.mono_font = ('Consolas', 10)  # Windows monospace font
        
        # Configure styles
        self.style.configure('.', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color,
                           font=self.mono_font)
        self.style.configure('Title.TLabel', font=(self.mono_font[0], 16, 'bold'))
        self.style.configure('Card.TFrame', background=self.card_color, 
                           relief=tk.FLAT, borderwidth=0)
        
        # Button styles with rounded corners
        self.style.configure('TButton', font=self.mono_font, borderwidth=0)
        self.style.configure('Accent.TButton', background=self.button_color, 
                           foreground=self.button_text, borderwidth=0)
        self.style.map('Accent.TButton',
                      background=[('active', '#3d7e24'), ('pressed', '#2a5a1a')])
        self.style.configure('Secondary.TButton', background='#2d3a2d', 
                           foreground=self.text_color)
        self.style.configure('Danger.TButton', background=self.danger_color, 
                           foreground='white')
        
        # Configure rounded entry widgets
        self.style.configure('Rounded.TEntry', 
                           fieldbackground=self.card_color, 
                           foreground=self.text_color,
                           borderwidth=0,
                           relief=tk.FLAT,
                           padding=5)
        
        # Configure scrollbar
        self.style.configure('Vertical.TScrollbar', background=self.card_color,
                           troughcolor=self.bg_color, bordercolor=self.bg_color,
                           arrowcolor=self.text_color)
        
        # Set background for all ttk widgets
        self.style.configure('TNotebook', background=self.bg_color)
        self.style.configure('TNotebook.Tab', background=self.bg_color)
        self.style.map('TNotebook.Tab', background=[('selected', self.card_color)])
    
    def load_saved_links(self):
        try:
            if os.path.exists(self.links_file):
                with open(self.links_file, 'r') as f:
                    self.saved_links = json.load(f)
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load links: {str(e)}")
            self.saved_links = []
    
    def save_links(self):
        try:
            with open(self.links_file, 'w') as f:
                json.dump(self.saved_links, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save links: {str(e)}")
            return False
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_card(self, parent, padx=20, pady=10):
        # Create a rounded frame container
        container = tk.Frame(parent, bg=self.bg_color)
        container.pack(fill=tk.X, padx=padx, pady=pady)
        
        # Create rounded canvas
        card = RoundedFrame(container, radius=12, bg=self.card_color, highlightthickness=0)
        card.pack(fill=tk.X, ipadx=10, ipady=10)
        
        # Add content frame inside the rounded canvas
        content_frame = tk.Frame(card, bg=self.card_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        return content_frame
    
    def create_rounded_entry(self, parent, **kwargs):
        # Create container frame
        container = tk.Frame(parent, bg=self.bg_color)
        
        # Create rounded canvas background
        canvas = RoundedFrame(container, radius=8, bg=self.card_color, highlightthickness=0)
        canvas.pack(fill=tk.X)
        
        # Create actual entry widget
        entry = ttk.Entry(canvas, style='Rounded.TEntry', **kwargs)
        entry_window = canvas.create_window(5, 5, anchor='nw', window=entry, 
                                          width=kwargs.get('width', 50)*8-10, 
                                          height=28)
        
        # Update entry when canvas is resized
        def update_entry(event):
            canvas.itemconfig(entry_window, width=event.width-10)
        
        canvas.bind('<Configure>', update_entry)
        
        return container, entry
    
    def show_main_page(self):
        self.clear_frame()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        tk.Label(header_frame, text="Chat Link Sender", 
                font=(self.mono_font[0], 16, 'bold'), 
                bg=self.bg_color, fg=self.text_color).pack()
        
        if self.saved_links:
            # Links card
            links_card = self.create_card(self.root)
            
            tk.Label(links_card, text="Your Saved Links", 
                    font=(self.mono_font[0], 12, 'bold'), 
                    bg=self.card_color, fg=self.text_color).pack(anchor='w', pady=(0, 10))
            
            for i, link in enumerate(self.saved_links, 1):
                link_frame = tk.Frame(links_card, bg=self.card_color)
                link_frame.pack(fill=tk.X, pady=2)
                tk.Label(link_frame, text=f"{i}. {link}", 
                        font=self.mono_font, 
                        bg=self.card_color, fg=self.text_color).pack(side=tk.LEFT, padx=5)
            
            # Buttons
            btn_frame = tk.Frame(self.root, bg=self.bg_color)
            btn_frame.pack(pady=20)
            
            ttk.Button(btn_frame, text="Edit Links", command=self.show_edit_page, 
                      style='Secondary.TButton').pack(side=tk.LEFT, padx=10, ipadx=20, ipady=5)
            ttk.Button(btn_frame, text="Continue", command=self.show_send_page, 
                      style='Accent.TButton').pack(side=tk.LEFT, padx=10, ipadx=20, ipady=5)
        else:
            self.show_edit_page()
    
    def show_edit_page(self):
        self.clear_frame()
        self.link_entries = []
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        tk.Label(header_frame, text="Add Chat Links", 
                font=(self.mono_font[0], 16, 'bold'), 
                bg=self.bg_color, fg=self.text_color).pack()
        
        # Links card
        links_card = self.create_card(self.root)
        tk.Label(links_card, text="Enter your chat links below:", 
                font=(self.mono_font[0], 11), 
                bg=self.card_color, fg=self.text_color).pack(anchor='w', pady=(0, 10))
        
        entry_frame = tk.Frame(links_card, bg=self.card_color)
        entry_frame.pack(fill=tk.X, pady=5)
        
        for link in self.saved_links:
            self.add_link_entry(entry_frame, link)
        
        if not self.saved_links:
            self.add_link_entry(entry_frame)
        
        # Add more button
        ttk.Button(self.root, text="+ Add Another Link", 
                  command=lambda: self.add_link_entry(entry_frame),
                  style='Secondary.TButton').pack(pady=5, ipadx=10, ipady=3)
        
        # Save button
        ttk.Button(self.root, text="Save Links", command=self.save_link_entries, 
                  style='Accent.TButton').pack(pady=20, ipadx=30, ipady=5)
    
    def add_link_entry(self, frame, link=""):
        entry_frame = tk.Frame(frame, bg=self.card_color)
        entry_frame.pack(fill=tk.X, pady=5)
        
        # Create rounded entry
        entry_container, entry = self.create_rounded_entry(entry_frame, font=self.mono_font, width=50)
        entry_container.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        entry.insert(0, link)
        
        remove_btn = ttk.Button(entry_frame, text="×", 
                              command=lambda: self.remove_link_entry(entry_frame), 
                              style='Danger.TButton', width=2)
        remove_btn.pack(side=tk.LEFT)
        
        self.link_entries.append((entry_frame, entry))
    
    def remove_link_entry(self, frame):
        for i, (entry_frame, entry) in enumerate(self.link_entries):
            if entry_frame == frame:
                entry_frame.destroy()
                self.link_entries.pop(i)
                break
    
    def save_link_entries(self):
        new_links = []
        for _, entry in self.link_entries:
            link = entry.get().strip()
            if link:
                new_links.append(link)
        
        if not new_links:
            messagebox.showerror("Error", "Please add at least one valid link")
            return
        
        self.saved_links = new_links
        if self.save_links():
            self.show_send_page()
    
    def show_send_page(self):
        self.clear_frame()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        tk.Label(header_frame, text="Compose Message", 
                font=(self.mono_font[0], 16, 'bold'), 
                bg=self.bg_color, fg=self.text_color).pack()
        
        # Message card
        message_card = self.create_card(self.root)
        tk.Label(message_card, text="Type your message below:", 
                font=(self.mono_font[0], 11), 
                bg=self.card_color, fg=self.text_color).pack(anchor='w', pady=(0, 10))
        
        # Text area container
        text_container = tk.Frame(message_card, bg=self.card_color)
        text_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create rounded text widget
        canvas = RoundedFrame(text_container, radius=8, bg=self.card_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        self.message_text = tk.Text(canvas, height=10, width=50, 
                                  font=self.mono_font, wrap=tk.WORD,
                                  relief=tk.FLAT, borderwidth=0,
                                  bg=self.card_color, fg=self.text_color,
                                  insertbackground=self.text_color,
                                  highlightthickness=0)
        
        text_window = canvas.create_window(3, 3, anchor='nw', window=self.message_text)
        
        def update_text_window(event):
            canvas.itemconfig(text_window, width=event.width-6, height=event.height-6)
        
        canvas.bind('<Configure>', update_text_window)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.message_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=scrollbar.set)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Fly!", command=self.send_messages, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=10, ipadx=30, ipady=8)
        ttk.Button(btn_frame, text="Back", command=self.show_main_page, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=10, ipadx=20, ipady=5)
    
    def send_messages(self):
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to send")
            return
        
        if not self.saved_links:
            messagebox.showerror("Error", "No chat links found")
            return
        
        if not messagebox.askyesno("Confirm", f"Send this message to {len(self.saved_links)} chats?\n\n{message[:100]}..."):
            return
        
        try:
            # Copy message to clipboard for pasting
            self.root.clipboard_clear()
            self.root.clipboard_append(message)
            
            # Minimize the tkinter window
            self.root.iconify()
            time.sleep(1)
            
            # Open a new browser window first
            webbrowser.open_new("about:blank")
            time.sleep(3)
            
            for i, link in enumerate(self.saved_links):
                # Open the link in a new tab
                if i == 0:
                    webbrowser.open_new_tab(link)
                else:
                    webbrowser.open_new_tab(link)
                
                time.sleep(3)
                
                # Focus on browser window
                pyautogui.hotkey('alt', 'tab')
                time.sleep(1)
                
                # Special handling for different services
                if "discord.com" in link:
                    # Discord-specific actions
                    time.sleep(5)
                    for _ in range(2):
                        pyautogui.click(x=500, y=800)
                        time.sleep(0.5)
                    pyautogui.write(message)
                elif "messenger.com" in link or "facebook.com" in link:
                    # Messenger-specific actions
                    time.sleep(5)  # Extra wait for Messenger to load
                    pyautogui.click(x=700, y=950)  # Adjusted coordinates for Messenger
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'v')  # Paste instead of typing
                else:
                    # Default behavior for other sites
                    pyautogui.click(x=500, y=800)
                    time.sleep(1)
                    pyautogui.write(message)
                
                # Send the message
                time.sleep(0.5)
                pyautogui.press('enter')
                
                # Service-specific delays after sending
                if "discord.com" in link:
                    time.sleep(3)
                elif "messenger.com" in link or "facebook.com" in link:
                    time.sleep(2)
                else:
                    time.sleep(1)
            
            # Restore the tkinter window
            self.root.deiconify()
            messagebox.showinfo("Success", "Message sent to all chats!")
            
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatLinkSender(root)
    root.mainloop()