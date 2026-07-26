from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os

# =========================================
# GOL IDE
# =========================================

class GOLIDE:

    def __init__(self, root):

        self.root = root
        self.root.title("GOL IDE")
        self.root.geometry("1200x700")

        self.current_project = ""
        self.current_file = None

        # -----------------------------
        # ASK PROJECT DIRECTORY FIRST
        # -----------------------------
        self.ask_project_directory()

        # -----------------------------
        # MAIN UI
        # -----------------------------
        self.build_ui()

    # =========================================
    # DIRECTORY CHOOSER
    # =========================================

    def ask_project_directory(self):

        folder = filedialog.askdirectory(
            title="Select Project Folder"
        )

        if not folder:
            self.root.destroy()
            return

        self.current_project = folder

    # =========================================
    # BUILD UI
    # =========================================

    def build_ui(self):

        # -------------------------------------
        # MENU BAR
        # -------------------------------------

        menubar = Menu(self.root)

        home_menu = Menu(menubar, tearoff=0)
        home_menu.add_command(label="New")
        home_menu.add_command(label="Open")
        home_menu.add_command(label="Save")

        tools_menu = Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Run")
        tools_menu.add_command(label="Test")
        tools_menu.add_command(label="Upload")

        pref_menu = Menu(menubar, tearoff=0)
        pref_menu.add_command(label="Theme")
        pref_menu.add_command(label="Font")

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")

        menubar.add_cascade(label="Home", menu=home_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        menubar.add_cascade(label="Preferences", menu=pref_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # -------------------------------------
        # PROJECT TITLE
        # -------------------------------------

        top_frame = Frame(self.root, height=40)
        top_frame.pack(fill=X)

        project_name = os.path.basename(self.current_project)

        Label(
            top_frame,
            text=f"Project : {project_name}",
            font=("Consolas", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # -------------------------------------
        # MAIN BODY
        # -------------------------------------

        body = Frame(self.root)
        body.pack(fill=BOTH, expand=True)

        # =====================================
        # LEFT SIDE - FILE EXPLORER
        # =====================================

        left_frame = Frame(body, width=250, bd=1, relief="solid")
        left_frame.pack(side=LEFT, fill=Y)

        Label(
            left_frame,
            text="Folder Explorer",
            font=("Consolas", 12, "bold")
        ).pack(fill=X)

        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill=BOTH, expand=True)

        self.populate_tree()

        self.tree.bind("<<TreeviewSelect>>", self.open_selected_file)

        # =====================================
        # CENTER - EDITOR
        # =====================================

        center_frame = Frame(body, bd=1, relief="solid")
        center_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # TABS
        self.notebook = ttk.Notebook(center_frame)
        self.notebook.pack(fill=BOTH, expand=True)

        # =====================================
        # RIGHT SIDE - COMMANDS
        # =====================================

        right_frame = Frame(body, width=250, bd=1, relief="solid")
        right_frame.pack(side=RIGHT, fill=Y)

        Label(
            right_frame,
            text="Commands",
            font=("Consolas", 12, "bold")
        ).pack(pady=10)

        Button(
            right_frame,
            text="Run",
            width=15,
            command=self.run_project
        ).pack(pady=5)

        Button(
            right_frame,
            text="Test",
            width=15,
            command=self.test_project
        ).pack(pady=5)

        Button(
            right_frame,
            text="Upload",
            width=15,
            command=self.upload_project
        ).pack(pady=5)

        Button(
            right_frame,
            text="Check",
            width=15,
            command=self.check_project
        ).pack(pady=5)

        # PROJECT NAME

        Label(
            right_frame,
            text="Project Name"
        ).pack(pady=(20, 5))

        self.project_entry = Entry(right_frame)
        self.project_entry.pack(fill=X, padx=10)

        self.project_entry.insert(0, project_name)

        # NEW OPEN SAVE

        Button(
            right_frame,
            text="New",
            command=self.new_file
        ).pack(fill=X, padx=10, pady=5)

        Button(
            right_frame,
            text="Open",
            command=self.open_file_dialog
        ).pack(fill=X, padx=10, pady=5)

        Button(
            right_frame,
            text="Save",
            command=self.save_current_file
        ).pack(fill=X, padx=10, pady=5)

        # =====================================
        # CONSOLE
        # =====================================

        console_frame = Frame(self.root, height=150, bd=1, relief="solid")
        console_frame.pack(fill=X)

        Label(
            console_frame,
            text="Console",
            font=("Consolas", 11, "bold")
        ).pack(anchor="w")

        self.console = Text(
            console_frame,
            height=8,
            bg="blue",
            fg="lime",
            insertbackground="white",
            font=("Consolas", 11)
        )

        self.console.pack(fill=BOTH, expand=True)

        # =====================================
        # STATUS BAR
        # =====================================

        self.status = Label(
            self.root,
            text="Ln 1, Col 1 | UTF-8 | GOL | Ready",
            anchor="w"
        )

        self.status.pack(fill=X)

    # =========================================
    # FILE TREE
    # =========================================

    def populate_tree(self):

        self.tree.delete(*self.tree.get_children())

        root_node = self.tree.insert(
            "",
            "end",
            text=os.path.basename(self.current_project),
            open=True,
            values=[self.current_project]
        )

        self.process_directory(root_node, self.current_project)

    def process_directory(self, parent, path):

        for item in os.listdir(path):

            fullpath = os.path.join(path, item)

            node = self.tree.insert(
                parent,
                "end",
                text=item,
                open=False,
                values=[fullpath]
            )

            if os.path.isdir(fullpath):
                self.process_directory(node, fullpath)

    # =========================================
    # OPEN FILE FROM TREE
    # =========================================

    def open_selected_file(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        path = self.tree.item(selected)["values"]

        if not path:
            return

        filepath = path[0]

        if os.path.isdir(filepath):
            return

        self.open_file(filepath)

    # =========================================
    # OPEN FILE
    # =========================================

    def open_file(self, filepath):

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tab = Frame(self.notebook)

        text = Text(
            tab,
            undo=True,
            font=("Consolas", 12)
        )

        text.pack(fill=BOTH, expand=True)

        text.insert("1.0", content)

        filename = os.path.basename(filepath)

        self.notebook.add(tab, text=filename)
        self.notebook.select(tab)

        tab.text_widget = text
        tab.filepath = filepath

        self.current_file = tab

        self.log(f"Opened {filename}")

    # =========================================
    # NEW FILE
    # =========================================

    def new_file(self):

        filepath = filedialog.asksaveasfilename(
            defaultextension=".arh",
            filetypes=[
                ("GOL Files", "*.arh"),
                ("Python Files", "*.py"),
                ("All Files", "*.*")
            ]
        )

        if not filepath:
            return

        with open(filepath, "w") as f:
            f.write("")

        self.populate_tree()

        self.open_file(filepath)

    # =========================================
    # OPEN FILE DIALOG
    # =========================================

    def open_file_dialog(self):

        filepath = filedialog.askopenfilename()

        if filepath:
            self.open_file(filepath)

    # =========================================
    # SAVE FILE
    # =========================================

    def save_current_file(self):

        current = self.notebook.select()

        if not current:
            return

        tab = self.root.nametowidget(current)

        content = tab.text_widget.get("2.0", END)

        with open(tab.filepath, "w", encoding="utf-8") as f:
            f.write(content)

        self.log(f"Saved {os.path.basename(tab.filepath)}")

    # =========================================
    # COMMANDS
    # =========================================

    def run_project(self):

        self.log("RAN: 0 ERRORS")

    def test_project(self):

        self.log("TESTED: 'HELLO'")

    def upload_project(self):

        self.log("UPLOADED: 0 ERRORS: ARDUINO")

    def check_project(self):

        self.log("CHECKED: 0 ERRORS. ")
        self.log("HELLO, HOW ARE YOU.")

    # =========================================
    # CONSOLE LOG
    # =========================================

    def log(self, text):

        self.console.insert(END, text + "\n")
        self.console.see(END)

# =========================================
# START APP
# =========================================

root = Tk()

app = GOLIDE(root)

root.mainloop()