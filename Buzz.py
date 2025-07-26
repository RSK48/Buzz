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
            self.show_edit_page(first_time=True)
    
    def show_edit_page(self, first_time=False):
        self.clear_frame()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        tk.Label(header_frame, text="Add Chat Links", 
                font=(self.mono_font[0], 16, 'bold'), 
                bg=self.bg_color, fg=self.text_color).pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Links card
        links_card = self.create_card(main_container)
        tk.Label(links_card, text="Add links to different lines here:", 
                font=(self.mono_font[0], 11), 
                bg=self.card_color, fg=self.text_color).pack(anchor='w', pady=(0, 10))
        
        # Text area container
        text_container = tk.Frame(links_card, bg=self.card_color)
        text_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create rounded text widget
        canvas = RoundedFrame(text_container, radius=8, bg=self.card_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        self.links_text = tk.Text(canvas, height=15, width=50, 
                                font=self.mono_font, wrap=tk.NONE,
                                relief=tk.FLAT, borderwidth=0,
                                bg=self.card_color, fg=self.text_color,
                                insertbackground=self.text_color,
                                highlightthickness=0)
        
        # Add placeholder text if first time
        if first_time and not self.saved_links:
            self.links_text.insert("1.0", "https://discord.com/channels/...\nhttps://messenger.com/...\nhttps://web.whatsapp.com/...")
            self.links_text.tag_add("placeholder", "1.0", "end")
            self.links_text.tag_config("placeholder", foreground="#7a7a7a")
            
            def on_focus_in(event):
                if self.links_text.get("1.0", "end-1c") == "https://discord.com/channels/...\nhttps://messenger.com/...\nhttps://web.whatsapp.com/...":
                    self.links_text.delete("1.0", "end")
                    self.links_text.tag_remove("placeholder", "1.0", "end")
                    self.links_text.config(fg=self.text_color)
            
            self.links_text.bind("<FocusIn>", on_focus_in)
        
        # If not first time, populate with saved links
        if self.saved_links:
            self.links_text.insert("1.0", "\n".join(self.saved_links))
        
        text_window = canvas.create_window(3, 3, anchor='nw', window=self.links_text)
        
        def update_text_window(event):
            canvas.itemconfig(text_window, width=event.width-6, height=event.height-6)
        
        canvas.bind('<Configure>', update_text_window)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.links_text.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.links_text.config(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL, command=self.links_text.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.links_text.config(xscrollcommand=x_scrollbar.set)
        
        # Buttons
        btn_frame = tk.Frame(main_container, bg=self.bg_color)
        btn_frame.pack(pady=20)
        
        if first_time or not self.saved_links:
            ttk.Button(btn_frame, text="Save & Continue", command=self.save_text_links, 
                      style='Accent.TButton').pack(side=tk.LEFT, padx=10, ipadx=20, ipady=5)
        else:
            ttk.Button(btn_frame, text="Save", command=self.save_text_links, 
                      style='Accent.TButton').pack(side=tk.LEFT, padx=10, ipadx=20, ipady=5)
            ttk.Button(btn_frame, text="Continue", command=self.show_send_page, 
                      style='Secondary.TButton').pack(side=tk.LEFT, padx=10, ipadx=20, ipady=5)
    
    def save_text_links(self):
        text_content = self.links_text.get("1.0", tk.END).strip()
        if not text_content:
            messagebox.showerror("Error", "Please add at least one valid link")
            return
        
        # Split by lines and filter out empty lines
        new_links = [line.strip() for line in text_content.split('\n') if line.strip()]
        
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
            
            # Get screen dimensions for more precise clicking
            screen_width, screen_height = pyautogui.size()
            
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
                    # Discord-specific actions with more precise clicking
                    time.sleep(5)
                    
                    # Click more carefully in the message box area
                    click_x = screen_width // 2
                    click_y = screen_height - 100  # Near bottom of screen
                    
                    # Double click to ensure focus
                    pyautogui.click(click_x, click_y)
                    time.sleep(0.3)
                    pyautogui.click(click_x, click_y)
                    time.sleep(0.5)
                    
                    # Type the message
                    pyautogui.write(message)
                    
                    # Wait before sending
                    time.sleep(1)
                    pyautogui.press('enter')
                    
                    # Wait after sending
                    time.sleep(3)
                    
                elif "messenger.com" in link or "facebook.com" in link:
                    # Messenger-specific actions
                    time.sleep(5)  # Extra wait for Messenger to load
                    
                    # Calculate position based on screen size
                    click_x = screen_width // 2
                    click_y = screen_height - 100  # Near bottom of screen
                    
                    pyautogui.click(click_x, click_y)
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'v')  # Paste instead of typing
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    time.sleep(2)
                else:
                    # Default behavior for other sites
                    time.sleep(3)
                    
                    # Calculate position based on screen size
                    click_x = screen_width // 2
                    click_y = screen_height - 100  # Near bottom of screen
                    
                    pyautogui.click(click_x, click_y)
                    time.sleep(1)
                    pyautogui.write(message)
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    time.sleep(1)
                
                # Close the tab after sending
                time.sleep(1)  # Small delay before closing
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(1)  # Wait for tab to close
            
            # Restore the tkinter window
            self.root.deiconify()
            messagebox.showinfo("Success", "Message sent to all chats! All tabs have been closed.")
            
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatLinkSender(root)
    root.mainloop()