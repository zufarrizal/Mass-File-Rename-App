import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class MassFileRenameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mass File Rename App")

        # Frame untuk formulir
        self.form_frame = tk.Frame(master)
        self.form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Membuat widget untuk formulir
        self.create_form_widgets()

        # Membuat widget tombol
        self.create_button_widgets()

        # Membuat tabel file
        self.create_file_table()

        # Mengisi tabel file dengan file-file dalam direktori yang dipilih pengguna
        self.populate_file_table()

        # Menyiapkan event bindings untuk tabel
        self.setup_table_bindings()

    def create_form_widgets(self):
        # Label dan entry untuk memasukkan bagian nama file yang akan diubah
        self.label1 = tk.Label(self.form_frame, text="1. Browse Directory")
        self.label1.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.browse_button = tk.Button(self.form_frame, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Label dan entry untuk memasukkan bagian nama file yang akan diubah
        self.label2 = tk.Label(self.form_frame, text="2. Input the part of the name to be changed")
        self.label2.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.old_name_entry = tk.Entry(self.form_frame)
        self.old_name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Label dan entry untuk memasukkan nama baru file
        self.label3 = tk.Label(self.form_frame, text="3. Enter a new file name")
        self.label3.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.new_name_entry = tk.Entry(self.form_frame)
        self.new_name_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Label dan entry untuk memfilter ekstensi file
        self.label4 = tk.Label(self.form_frame, text="4. Enter file extension filter (optional)")
        self.label4.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.extension_entry = tk.Entry(self.form_frame)
        self.extension_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

    def create_button_widgets(self):
        # Frame untuk tombol
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Tombol untuk mengeksekusi proses renaming
        self.rename_button = tk.Button(self.button_frame, text="Rename", command=self.rename_files)
        self.rename_button.pack(side=tk.LEFT, padx=5)

        # Tombol untuk mengembalikan proses renaming sebelumnya
        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo_rename, state=tk.DISABLED)
        self.undo_button.pack(side=tk.LEFT, padx=5)

    def create_file_table(self):
        # Frame untuk tabel file
        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Tabel untuk menampilkan daftar file
        self.file_table = ttk.Treeview(self.table_frame, columns=("Name"))
        self.file_table.heading("#0", text="No.")
        self.file_table.column("#0", width=50)
        self.file_table.heading("Name", text="File Name")

        # Scrollbar untuk tabel
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.file_table.yview)
        self.file_table.configure(yscroll=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.file_table.pack(side="left", fill="both", expand=True)

    def populate_file_table(self):
        # Mengisi tabel file dengan file-file dalam direktori yang dipilih pengguna
        if hasattr(self, 'selected_directory'):
            file_names = os.listdir(self.selected_directory)
            for idx, file_name in enumerate(file_names, start=1):
                self.file_table.insert("", "end", text=str(idx), values=(file_name,))

    def setup_table_bindings(self):
        # Menyiapkan event bindings untuk tabel file
        self.file_table.bind("<Double-1>", self.on_table_click)

    def on_table_click(self, event):
        # Mengambil nama file yang dipilih pengguna dari tabel dan memasukkannya ke dalam entry "Input the part of the name to be changed"
        item = self.file_table.selection()[0]
        file_name = self.file_table.item(item, "values")[0]
        self.old_name_entry.delete(0, tk.END)
        self.old_name_entry.insert(0, file_name)

    def browse_directory(self):
        # Memilih direktori tempat file-file berada
        self.selected_directory = filedialog.askdirectory()
        if self.selected_directory:
            messagebox.showinfo("Info", "Directory has been selected: {}".format(self.selected_directory))
            self.file_table.delete(*self.file_table.get_children())
            self.populate_file_table()

    def rename_files(self):
        # Melakukan proses renaming berdasarkan input dari pengguna
        if not hasattr(self, 'selected_directory'):
            messagebox.showerror("Error", "Please select a directory first!")
            return

        old_name = self.old_name_entry.get()
        new_name = self.new_name_entry.get()
        extension_filter = self.extension_entry.get()

        if not old_name or not new_name:
            messagebox.showerror("Error", "Please enter the old and new file names!")
            return

        self.old_names = []
        self.new_names = []

        for filename in os.listdir(self.selected_directory):
            if old_name in filename and filename.endswith(extension_filter):
                new_filename = filename.replace(old_name, new_name)
                try:
                    os.rename(os.path.join(self.selected_directory, filename),
                              os.path.join(self.selected_directory, new_filename))
                    self.old_names.append(filename)
                    self.new_names.append(new_filename)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to change file name: {e}")
        messagebox.showinfo("Info", "File renaming is complete!")
        self.reload_file_table()  # Panggil metode reload setelah operasi selesai
        self.undo_button.config(state=tk.NORMAL)

    def undo_rename(self):
        # Mengembalikan proses renaming sebelumnya
        if hasattr(self, 'old_names') and hasattr(self, 'new_names'):
            for old_name, new_name in zip(self.old_names, self.new_names):
                try:
                    os.rename(os.path.join(self.selected_directory, new_name),
                              os.path.join(self.selected_directory, old_name))
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to undo file name change: {e}")
            messagebox.showinfo("Info", "Undo successful!")
            self.old_names = []
            self.new_names = []
            self.reload_file_table()  # Panggil metode reload setelah operasi selesai
            self.undo_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "No renaming operation to undo!")

    def reload_file_table(self):
        # Memuat ulang tabel file setelah proses renaming selesai
        self.file_table.delete(*self.file_table.get_children())
        self.populate_file_table()

if __name__ == "__main__":
    # Membuat instance Tkinter dan menjalankan aplikasi
    root = tk.Tk()
    app = MassFileRenameApp(root)
    root.mainloop()
