import os
import tkinter as tk
from tkinter import filedialog, messagebox

class MassFileRenameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mass File Rename App")
        self.master.geometry("500x250")  # Ukuran fixed

        self.label1 = tk.Label(master, text="1. Browse Directory")
        self.label1.pack(pady=5)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.label2 = tk.Label(master, text="2. Input the part of the name to be changed")
        self.label2.pack(pady=5)

        self.old_name_entry = tk.Entry(master)
        self.old_name_entry.pack()

        self.label3 = tk.Label(master, text="3. Enter a new file name")
        self.label3.pack(pady=5)

        self.new_name_entry = tk.Entry(master)
        self.new_name_entry.pack()

        self.rename_button = tk.Button(master, text="Ubah Nama", command=self.rename_files)
        self.rename_button.pack(pady=10)

    def browse_directory(self):
        self.selected_directory = filedialog.askdirectory()
        if self.selected_directory:
            messagebox.showinfo("Info", "Directory has been selected: {}".format(self.selected_directory))

    def rename_files(self):
        if not hasattr(self, 'selected_directory'):
            messagebox.showerror("Error", "Please select a directory first!")
            return

        old_name = self.old_name_entry.get()
        new_name = self.new_name_entry.get()

        if not old_name or not new_name:
            messagebox.showerror("Error", "Please enter the old and new file names!")
            return

        for filename in os.listdir(self.selected_directory):
            if old_name in filename:
                new_filename = filename.replace(old_name, new_name)
                try:
                    os.rename(os.path.join(self.selected_directory, filename),
                              os.path.join(self.selected_directory, new_filename))
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to change file name: {e}")
        messagebox.showinfo("Info", "File renaming is complete!")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Membuat ukuran fixed
    app = MassFileRenameApp(root)
    root.mainloop()
