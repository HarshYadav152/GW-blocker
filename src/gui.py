import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from typing import List, Optional

from src.blocker import WebsiteBlocker
from src.utils import is_valid_url, clean_url, save_blocked_sites, load_config, save_block_until

class WebsiteBlockerApp:
    def __init__(self, root):
        """Initialize the Website Blocker GUI."""
        self.root = root
        self.root.title("GW-blocker")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        self.blocker = WebsiteBlocker()
        self.config = load_config()
        
        # Check admin privileges
        if not self.blocker.is_admin():
            messagebox.showwarning(
                "Administrator Privileges Required",
                "This application requires administrator privileges to modify the hosts file. "
                "Please restart the application as administrator."
            )
        
        self._create_widgets()
        self._update_site_list()
        
    def _create_widgets(self):
        """Create GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL input
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(url_frame, text="Website URL:").pack(side=tk.LEFT)
        
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.url_entry.bind("<Return>", lambda e: self._block_website())
        
        ttk.Button(url_frame, text="Block", command=self._block_website).pack(side=tk.LEFT)
        
        # Time limit options
        time_frame = ttk.LabelFrame(main_frame, text="Block Duration")
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.duration_var = tk.StringVar(value="permanent")
        
        ttk.Radiobutton(
            time_frame, text="Permanent", 
            variable=self.duration_var, value="permanent"
        ).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        ttk.Radiobutton(
            time_frame, text="Until:", 
            variable=self.duration_var, value="until"
        ).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Time widgets
        time_select_frame = ttk.Frame(time_frame)
        time_select_frame.grid(row=0, column=2, sticky=tk.W)
        
        # Hours dropdown (1-12)
        self.hour_var = tk.StringVar(value="12")
        ttk.Combobox(
            time_select_frame, textvariable=self.hour_var,
            values=[str(i).zfill(2) for i in range(1, 13)],
            width=3, state="readonly"
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(time_select_frame, text=":").pack(side=tk.LEFT)
        
        # Minutes dropdown (00-59)
        self.minute_var = tk.StringVar(value="00")
        ttk.Combobox(
            time_select_frame, textvariable=self.minute_var,
            values=[str(i).zfill(2) for i in range(0, 60, 5)],
            width=3, state="readonly"
        ).pack(side=tk.LEFT, padx=2)
        
        # AM/PM
        self.ampm_var = tk.StringVar(value="PM")
        ttk.Combobox(
            time_select_frame, textvariable=self.ampm_var,
            values=["AM", "PM"], width=3, state="readonly"
        ).pack(side=tk.LEFT, padx=2)
        
        # Website list
        list_frame = ttk.LabelFrame(main_frame, text="Blocked Websites")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Website listbox
        self.site_listbox = tk.Listbox(list_frame)
        self.site_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        self.site_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.site_listbox.yview)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame, text="Unblock Selected", 
            command=self._unblock_selected
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame, text="Unblock All", 
            command=self._unblock_all
        ).pack(side=tk.LEFT)
    
    def _update_site_list(self):
        """Update the list of blocked websites."""
        # Clear the listbox
        self.site_listbox.delete(0, tk.END)
        
        # Get blocked sites and add to listbox
        blocked_sites = self.blocker.get_blocked_websites()
        for site in blocked_sites:
            self.site_listbox.insert(tk.END, site)
    
    def _block_website(self):
        """Block the website entered in the URL field."""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a website URL.")
            return
        
        # Clean and validate URL
        url = clean_url(url)
        if not is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid website URL (e.g., example.com).")
            return
        
        # Set block duration
        if self.duration_var.get() == "until":
            try:
                # Parse time
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                is_pm = self.ampm_var.get() == "PM"
                
                # Convert to 24-hour format
                if is_pm and hour < 12:
                    hour += 12
                elif not is_pm and hour == 12:
                    hour = 0
                
                now = datetime.datetime.now()
                block_until = now.replace(hour=hour, minute=minute)
                
                # If the time is in the past, set it for tomorrow
                if block_until <= now:
                    block_until += datetime.timedelta(days=1)
                
                # Save block duration
                save_block_until(block_until.isoformat())
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid time format: {e}")
                return
        else:
            save_block_until(None)  # Permanent block
        
        # Block the website
        if self.blocker.block_website(url):
            messagebox.showinfo("Success", f"Successfully blocked {url}")
            self.url_entry.delete(0, tk.END)
            self._update_site_list()
            
            # Save to config
            blocked_sites = self.blocker.get_blocked_websites()
            save_blocked_sites(blocked_sites)
        else:
            messagebox.showerror(
                "Error", 
                "Failed to block website. Make sure you're running as administrator."
            )
    
    def _unblock_selected(self):
        """Unblock the selected website."""
        selection = self.site_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a website to unblock.")
            return
        
        website = self.site_listbox.get(selection[0])
        if self.blocker.unblock_website(website):
            messagebox.showinfo("Success", f"Successfully unblocked {website}")
            self._update_site_list()
            
            # Update config
            blocked_sites = self.blocker.get_blocked_websites()
            save_blocked_sites(blocked_sites)
        else:
            messagebox.showerror(
                "Error", 
                "Failed to unblock website. Make sure you're running as administrator."
            )
    
    def _unblock_all(self):
        """Unblock all websites."""
        if messagebox.askyesno("Confirm", "Are you sure you want to unblock all websites?"):
            if self.blocker.unblock_all():
                messagebox.showinfo("Success", "Successfully unblocked all websites")
                self._update_site_list()
                
                # Update config
                save_blocked_sites([])
            else:
                messagebox.showerror(
                    "Error", 
                    "Failed to unblock websites. Make sure you're running as administrator."
                )