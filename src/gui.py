import sys
import ctypes
import platform
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import datetime

from src.blocker import WebsiteBlocker
from src.utils import (
    is_valid_url,
    clean_url,
    save_blocked_sites,
    load_config,
    save_block_until,
    build_export_data,
    parse_import_data,
    is_password_set,
    set_password,
    verify_password,
    remove_password,
)



class WebsiteBlockerApp:
    def __init__(self, root):
        """Initialize the Website Blocker GUI."""
        self.root = root
        self.root.title("GW-blocker")
        self.root.geometry("720x600")
        self.root.minsize(650, 550)
        self.root.resizable(True, True)

        self.blocker = WebsiteBlocker()
        self.config = load_config()

        # Master list that always holds the full blocked-sites state.
        # The listbox may show a filtered subset; this is the source of truth.
        self._all_blocked: list = []

        if not self.blocker.is_admin():
            if platform.system().lower() == "windows":
                self._handle_admin_elevation()
            else:
                messagebox.showwarning(
                "Administrator Privileges Required",
                "This application requires administrator privileges to modify the hosts file. "
                "Please restart the application as administrator.",
            )
        
        self._create_menu()
        self._configure_styles()
        self._create_widgets()
        self._update_site_list()
        
    def _create_menu(self):
        """Build the menu bar with the Security (password) options."""
        menubar = tk.Menu(self.root)

        security_menu = tk.Menu(menubar, tearoff=0)
        security_menu.add_command(label="Set Password", command=self._set_password)
        security_menu.add_command(label="Change Password", command=self._change_password)
        security_menu.add_command(label="Remove Password", command=self._remove_password)
        menubar.add_cascade(label="Security", menu=security_menu)

        self.root.config(menu=menubar)
    
    def _configure_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 18, "bold")
        )

        style.configure(
            "SubHeader.TLabel",
            font=("Segoe UI", 10)
        )

    def _require_password(self) -> bool:
        """Gate an unblock action behind the password, if one is set.

        Returns True if the action may proceed: either no password is
        configured, or the user entered the correct one. Returns False if the
        user cancels or enters the wrong password.
        """
        if not is_password_set():
            return True

        entered = simpledialog.askstring(
            "Password Required",
            "Enter your password to unblock:",
            show="*",
            parent=self.root,
        )
        if entered is None:
            return False  # user cancelled
        if verify_password(entered):
            return True

        messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")
        return False

    def _set_password(self):
        """Create a password (only when none is set yet)."""
        if is_password_set():
            messagebox.showinfo(
                "Password",
                "A password is already set. Use 'Change Password' to update it.",
            )
            return

        new = simpledialog.askstring(
            "Set Password", "Enter a new password:", show="*", parent=self.root
        )
        if new is None:
            return
        if len(new) < 4:
            messagebox.showerror("Password", "Password must be at least 4 characters.")
            return

        confirm = simpledialog.askstring(
            "Set Password", "Re-enter the password:", show="*", parent=self.root
        )
        if confirm is None:
            return
        if new != confirm:
            messagebox.showerror("Password", "Passwords do not match.")
            return

        if set_password(new):
            messagebox.showinfo("Password", "Password protection enabled.")
        else:
            messagebox.showerror("Password", "Could not save the password.")

    def _change_password(self):
        """Change an existing password (current password required)."""
        if not is_password_set():
            messagebox.showinfo("Password", "No password is set. Use 'Set Password' first.")
            return

        current = simpledialog.askstring(
            "Change Password", "Enter your current password:", show="*", parent=self.root
        )
        if current is None:
            return
        if not verify_password(current):
            messagebox.showerror("Password", "Current password is incorrect.")
            return

        new = simpledialog.askstring(
            "Change Password", "Enter a new password:", show="*", parent=self.root
        )
        if new is None:
            return
        if len(new) < 4:
            messagebox.showerror("Password", "Password must be at least 4 characters.")
            return

        confirm = simpledialog.askstring(
            "Change Password", "Re-enter the new password:", show="*", parent=self.root
        )
        if confirm is None:
            return
        if new != confirm:
            messagebox.showerror("Password", "Passwords do not match.")
            return

        if set_password(new):
            messagebox.showinfo("Password", "Password changed.")
        else:
            messagebox.showerror("Password", "Could not save the new password.")

    def _remove_password(self):
        """Remove password protection (current password required)."""
        if not is_password_set():
            messagebox.showinfo("Password", "No password is set.")
            return

        current = simpledialog.askstring(
            "Remove Password",
            "Enter your current password to remove protection:",
            show="*",
            parent=self.root,
        )
        if current is None:
            return
        if not verify_password(current):
            messagebox.showerror("Password", "Password is incorrect.")
            return

        if remove_password():
            messagebox.showinfo("Password", "Password protection removed.")
        else:
            messagebox.showerror("Password", "Could not remove the password.")

    def _handle_admin_elevation(self):
        """Handle Windows UAC elevation when Administrator privileges are required."""

        restart = messagebox.askyesno(
            "Administrator Privileges Required",
            (
                "Administrator privileges are required to modify the Windows hosts file.\n\n"
                "Would you like GW-Blocker to restart as Administrator?"
            ),
        )

        if not restart:
            self.root.destroy()
            sys.exit(0)

        try:
            if getattr(sys, "frozen", False):
                result = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    sys.executable,
                    None,
                    None,
                    1,
                )
            else:
                result = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    sys.executable,
                    "-m src.main",
                    os.getcwd(),
                    1,
                )

            # ShellExecute returns values > 32 on success.
            if result > 32:
                self.root.destroy()
                sys.exit(0)

            messagebox.showerror(
                "Elevation Failed",
                (
                    "GW-Blocker could not restart with Administrator privileges.\n\n"
                    "Please launch the application as Administrator."
                ),
            )

        except Exception:
            messagebox.showerror(
                "Elevation Failed",
                (
                    "GW-Blocker could not restart with Administrator privileges.\n\n"
                    "Please launch the application as Administrator."
                ),
            )

        self.root.destroy()
        sys.exit(1)

    def _create_widgets(self):
        """Create GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="10")
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            header_frame,
            text="Block distracting websites quickly and safely",
            style="SubHeader.TLabel"
        ).pack(anchor="w")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- URL input ---
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(url_frame, text="Website URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.url_entry.bind("<Return>", lambda e: self._block_website())
        ttk.Button(url_frame, text="Block", command=self._block_website).pack(side=tk.LEFT)

        # --- Block duration ---
        time_frame = ttk.LabelFrame(main_frame, text="Block Duration")
        time_frame.pack(fill=tk.X, pady=(0, 10))

        self.duration_var = tk.StringVar(value="permanent")
        ttk.Radiobutton(
            time_frame, text="Permanent",
            variable=self.duration_var, value="permanent",
        ).grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Radiobutton(
            time_frame, text="Until:",
            variable=self.duration_var, value="until",
        ).grid(row=0, column=1, sticky=tk.W, padx=5)

        time_select_frame = ttk.Frame(time_frame)
        time_select_frame.grid(row=0, column=2, sticky=tk.W)

        self.hour_var = tk.StringVar(value="12")
        ttk.Combobox(
            time_select_frame, textvariable=self.hour_var,
            values=[str(i).zfill(2) for i in range(1, 13)],
            width=3, state="readonly",
        ).pack(side=tk.LEFT, padx=2)

        ttk.Label(time_select_frame, text=":").pack(side=tk.LEFT)

        self.minute_var = tk.StringVar(value="00")
        ttk.Combobox(
            time_select_frame, textvariable=self.minute_var,
            values=[str(i).zfill(2) for i in range(0, 60, 5)],
            width=3, state="readonly",
        ).pack(side=tk.LEFT, padx=2)

        self.ampm_var = tk.StringVar(value="PM")
        ttk.Combobox(
            time_select_frame, textvariable=self.ampm_var,
            values=["AM", "PM"], width=3, state="readonly",
        ).pack(side=tk.LEFT, padx=2)

        # --- Blocked websites list ---
        list_frame = ttk.LabelFrame(main_frame, text="Blocked Websites")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Search bar (issue #6)
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=(5, 2))

        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 4))

        ttk.Button(
            search_frame, text="✕", width=2,
            command=self._clear_search,
        ).pack(side=tk.LEFT)

        # Listbox + scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.site_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.site_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.site_listbox.yview)

        # --- Action buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            button_frame, text="Unblock Selected",
            command=self._unblock_selected,
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            button_frame, text="Unblock All",
            command=self._unblock_all,
        ).pack(side=tk.LEFT)

        ttk.Button(
            button_frame, text="Export",
            command=self._export_blocklist,
        ).pack(side=tk.RIGHT)

        ttk.Button(
            button_frame, text="Import",
            command=self._import_blocklist,
        ).pack(side=tk.RIGHT, padx=(0, 5))

    # ------------------------------------------------------------------
    # Search helpers (issue #6)
    # ------------------------------------------------------------------

    def _on_search_change(self, *_):
        """Filter the listbox in real-time as the user types."""
        query = self.search_var.get().lower()
        self.site_listbox.delete(0, tk.END)
        for site in self._all_blocked:
            if query in site.lower():
                self.site_listbox.insert(tk.END, site)

    def _clear_search(self):
        """Clear the search field, restoring the full list."""
        self.search_var.set("")
        self.search_entry.focus()

    # ------------------------------------------------------------------
    # List management
    # ------------------------------------------------------------------

    def _update_site_list(self):
        """Refresh _all_blocked from the hosts file, then re-apply any active search."""
        self._all_blocked = self.blocker.get_blocked_websites()
        self._on_search_change()  # honours whatever is currently in the search box

    # ------------------------------------------------------------------
    # Block / unblock actions
    # ------------------------------------------------------------------

    def _block_website(self):
        """Block the website entered in the URL field."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a website URL.")
            return

        url = clean_url(url)
        if not is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid website URL (e.g., example.com).")
            return

        if self.duration_var.get() == "until":
            try:
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                is_pm = self.ampm_var.get() == "PM"

                if is_pm and hour < 12:
                    hour += 12
                elif not is_pm and hour == 12:
                    hour = 0

                now = datetime.datetime.now()
                block_until = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if block_until <= now:
                    block_until += datetime.timedelta(days=1)

                save_block_until(block_until.isoformat())
            except Exception as e:
                messagebox.showerror("Error", f"Invalid time format: {e}")
                return
        else:
            save_block_until(None)

        if self.blocker.block_website(url):
            messagebox.showinfo("Success", f"Successfully blocked {url}")
            self.url_entry.delete(0, tk.END)
            self._update_site_list()
            save_blocked_sites(self._all_blocked)
        else:
            messagebox.showerror(
                "Error",
                "Failed to block website. Make sure you're running as administrator.",
            )

    def _unblock_selected(self):
        """Unblock the selected website."""
        selection = self.site_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a website to unblock.")
            return

        website = self.site_listbox.get(selection[0])

        if not self._require_password():
            return

        if self.blocker.unblock_website(website):
            messagebox.showinfo("Success", f"Successfully unblocked {website}")
            self._update_site_list()
            save_blocked_sites(self._all_blocked)
        else:
            messagebox.showerror(
                "Error",
                "Failed to unblock website. Make sure you're running as administrator.",
            )

    def _unblock_all(self):
        """Unblock all websites."""
        if messagebox.askyesno("Confirm", "Are you sure you want to unblock all websites?"):
            if not self._require_password():
                return
            if self.blocker.unblock_all():
                messagebox.showinfo("Success", "Successfully unblocked all websites")
                self._update_site_list()
                save_blocked_sites([])
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to unblock websites. Make sure you're running as administrator.",
                )

    # ------------------------------------------------------------------
    # Import / Export (issue #7)
    # ------------------------------------------------------------------

    def _export_blocklist(self):
        """Export the current block list to a JSON file."""
        if not self._all_blocked:
            messagebox.showinfo("Export", "There are no blocked websites to export.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export Block List",
            defaultextension=".json",
            initialfile="gw-blocker-blocklist.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            config = load_config()
            data = build_export_data(self._all_blocked, config)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo(
                "Export",
                f"Exported {len(self._all_blocked)} website(s) to:\n{file_path}",
            )
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export block list:\n{e}")

    def _import_blocklist(self):
        """Import a block list from a JSON file."""
        file_path = filedialog.askopenfilename(
            title="Import Block List",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showerror("Import Failed", f"The selected file is not valid JSON:\n{e}")
            return
        except Exception as e:
            messagebox.showerror("Import Failed", f"Could not read the file:\n{e}")
            return

        valid_domains, skipped = parse_import_data(raw)

        if not valid_domains:
            messagebox.showwarning(
                "Import",
                "No valid websites were found in the selected file."
                + (
                    f"\n\nSkipped {len(skipped)} invalid entr"
                    f"{'y' if len(skipped) == 1 else 'ies'}."
                    if skipped
                    else ""
                ),
            )
            return

        already_blocked = set(self._all_blocked)
        to_block = [d for d in valid_domains if d not in already_blocked]
        duplicates = len(valid_domains) - len(to_block)

        if not to_block:
            messagebox.showinfo("Import", "All valid websites in the file are already blocked.")
            return

        if not self.blocker.block_websites(to_block):
            messagebox.showerror(
                "Import Failed",
                "Failed to block websites. Make sure you're running as administrator.",
            )
            return

        self._update_site_list()
        save_blocked_sites(self._all_blocked)

        summary = [f"Imported and blocked {len(to_block)} website(s)."]
        if duplicates:
            summary.append(
                f"Skipped {duplicates} already-blocked entr"
                f"{'y' if duplicates == 1 else 'ies'}."
            )
        if skipped:
            preview = ", ".join(skipped[:5])
            if len(skipped) > 5:
                preview += ", ..."
            summary.append(
                f"Skipped {len(skipped)} invalid entr"
                f"{'y' if len(skipped) == 1 else 'ies'}: {preview}"
            )
        messagebox.showinfo("Import Complete", "\n".join(summary))