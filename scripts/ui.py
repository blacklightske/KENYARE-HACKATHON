import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time

# Import the main processing function (direct file access)
from main import process_files_directly, stop_processing

# Global flag to control processing
is_processing = False

def create_ui():
    def load_config():
        try:
            with open("config.txt", "r") as f:
                shared_folder = f.readline().strip()
                done_projects_folder = f.readline().strip()
                return shared_folder, done_projects_folder
        except FileNotFoundError:
            return '', ''

    def save_config(shared_folder, done_projects_folder):
        with open("config.txt", "w") as f:
            f.write(f"{shared_folder}\n{done_projects_folder}")

    def browse_shared_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            shared_folder_entry.delete(0, tk.END)
            shared_folder_entry.insert(0, folder_selected)
            save_config(folder_selected, done_projects_entry.get())

    def browse_done_projects():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            done_projects_entry.delete(0, tk.END)
            done_projects_entry.insert(0, folder_selected)
            save_config(shared_folder_entry.get(), folder_selected)

    def update_progress(message):
        progress_var.set(message)
        root.update_idletasks()

    def start_processing():
        global is_processing
        shared_folder = shared_folder_entry.get()
        done_projects_folder = done_projects_entry.get()

        if not shared_folder or not done_projects_folder:
            messagebox.showwarning("Warning", "Please set shared and done projects folders.")
            return

        # Ensure we are not starting multiple threads if already running
        if is_processing:
            messagebox.showinfo("Info", "Processing is already running.")
            return

        is_processing = True
        update_progress("Processing started...")
        
        # Start the processing in a separate thread to keep the UI responsive
        threading.Thread(target=process_files_directly, args=(shared_folder, done_projects_folder)).start()

    def stop_processing():
        global is_processing
        is_processing = False
        update_progress("Processing stopped.")
        messagebox.showinfo("Stopped", "Processing has been stopped.")

    root = tk.Tk()
    root.title("Claims Processing App")

    # Center the UI window
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Shared folder UI elements
    tk.Label(root, text="Shared Folder:").grid(row=0, column=0, pady=10, padx=10)
    shared_folder_entry = tk.Entry(root, width=50)
    shared_folder_entry.grid(row=0, column=1, pady=10, padx=10)
    tk.Button(root, text="Browse", command=browse_shared_folder).grid(row=0, column=2, pady=10, padx=10)

    # Done projects folder UI elements
    tk.Label(root, text="Done Projects Folder:").grid(row=1, column=0, pady=10, padx=10)
    done_projects_entry = tk.Entry(root, width=50)
    done_projects_entry.grid(row=1, column=1, pady=10, padx=10)
    tk.Button(root, text="Browse", command=browse_done_projects).grid(row=1, column=2, pady=10, padx=10)

    # Start and Stop buttons
    tk.Button(root, text="Start Processing", command=start_processing).grid(row=2, column=0, pady=10, padx=10)
    tk.Button(root, text="Stop Processing", command=stop_processing).grid(row=2, column=1, pady=10, padx=10)

    # Progress display
    progress_var = tk.StringVar()
    progress_label = tk.Label(root, textvariable=progress_var, width=50)
    progress_label.grid(row=4, column=0, columnspan=3, pady=20)

    # Load the last used config (shared and done folders)
    shared_folder_path, done_projects_folder_path = load_config()
    shared_folder_entry.insert(0, shared_folder_path)
    done_projects_entry.insert(0, done_projects_folder_path)

    root.mainloop()

# Main function to start the application
def main():
    create_ui()

if __name__ == "__main__":
    main()
