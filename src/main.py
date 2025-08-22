import sys
import tkinter as tk
from src.gui import WebsiteBlockerApp

def main():
    """Main entry point for the application."""
    # Create the Tkinter root window
    root = tk.Tk()
    
    # Create the application
    app = WebsiteBlockerApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()