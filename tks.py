import shutil
from shutil import rmtree
import datetime as dt
from pygame import mixer
import serial


from tkinter.simpledialog import askinteger, askstring
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import colorchooser
from tkinter.colorchooser import askcolor

from nodes.General import ProgramNode
from lexer import Lexer
from parser import *
from transpiler import Transpiler
from platformdirs import user_config_dir



import os
import sys
import subprocess
import json as data_handle
from pathlib import Path

project_path = Path(user_config_dir("HobbySpark transpiler",appauthor=False, roaming=True))/"GUI"
print(project_path)

ALL_BOARDS = {}

result = subprocess.run(
	["arduino-cli", "board", "listall", "--format", "json"],
	capture_output=True,
	text=True
)



data = data_handle.loads(result.stdout)

for board in data["boards"]:
	print(board["name"], board["fqbn"])
	ALL_BOARDS[board["name"]] = board["fqbn"]


class Welcome:
	def __init__(self, root:Tk) -> None:
		self.root = Toplevel(root)
		self.root.title("HobbySpark Welcome")
		self.first = Frame(self.root)
		Label(self.first, text="------WELCOME TO HOBBYSPARK------").pack()
		Label(self.first, text="Enter your name please: ", anchor="w").pack()
		self.text1 = Entry(self.first)
		self.text1.pack()
		Button(self.first, text="OK", command=self.but1, anchor="s").pack()

		self.second =Frame(self.root)
		Label(self.second, text="Enter your current age: ", anchor="w").pack()
		self.text2 = Entry(self.second)
		self.text2.pack()
		Button(self.second, text="OK", command=self.but2, anchor="s").pack()

		self.third =Frame(self.root)
		Label(self.third, text="Enter your birthday (M-D): ", anchor="w").pack()
		self.text3 = Entry(self.third)
		self.text3.pack()
		Button(self.third, text="OK", command=self.but3, anchor="s").pack()
		
		self.name = ""
		self.age = 0
		self.birthday = None
		self.start_animation()
		print("HEHQBHWHBQN", self.birthday, self.age, self.name)

	def start_animation(self):
		self.first.pack()


	def but1(self):
		self.name = self.text1.get()
		self.first.pack_forget()
		self.second.pack()

	def but2(self):
		self.age = int(self.text2.get())
		self.second.pack_forget()
		self.third.pack()

	def but3(self):
		self.birthday = dt.date(2026,*map(int,self.text3.get().split("-")))
		self.third.pack_forget()
		self.root.destroy()

class Console:
	def __init__(self, root ,text="Console") -> None:
		self.frame = LabelFrame(root, text=text)
		self.str = Text(self.frame, fg="green", bg="black")
		self.str.config(state="disabled")
		self.str.tag_configure("n", foreground="green")
		self.str.tag_configure("e", foreground="red")
		self.str.tag_configure("w", foreground="yellow")

	def write(self, *text):
		self.str.config(state="normal")
		self.str.insert("end", "\n".join(text)+"\n", "n")
		self.str.config(state="disabled")
	def write_error(self, *text):
		self.str.config(state="normal")
		self.str.insert("end", "\n".join(text)+"\n", "e")
		self.str.config(state="disabled")
	def write_warning(self, *text):
		self.str.config(state="normal")
		self.str.insert("end", "\n".join(text)+"\n", "w")
		self.str.config(state="disabled")
	def clear(self):
		self.str.config(state="normal")
		self.str.delete("1.0", END)
		self.str.config(state="disabled")

def askcom(root, out = None, console:Console = None):
	print("OUT", out)
	com = ""
	new = Toplevel(root)
	new.title("Select COM port")
	result = subprocess.run(["arduino-cli", "board", "list", "--format", "json"], capture_output=True, text=True)
	print(result.stdout)
	data:dict = (data_handle.loads(result.stdout))["detected_ports"]
	real_data = []
	print("OUT2", out)

	for w in data:
		dat = {
			"match":w["matching_boards"][0]["name"] if "matching_boards" in w else "Unknown",
			"com":w["port"]["address"],
			"serial":w["port"]["properties"]["serialNumber"]

		}
		real_data.append(dat)

	with_board = {
		b["com"]:{"com":b["com"], "match":b["match"]} for b in real_data
	}

	print("OUT3", out)


	box = ttk.Combobox(new, values=[a["match"]+"-"+a["com"] for a in real_data], width=50)
	def use():
		nonlocal com
		com = (box.get()).split("-")[1]
		print("H", with_board[com]["match"])
		print("dao",out)
		if with_board[com]["match"]=="Unknown":
			console.write_warning(f"Could not find board name, {com}. ")
		if with_board[com]["match"]!=out:
			a=mb.askokcancel("Board warning",f"Using another board than the {out}. This may cause an error", icon=mb.WARNING)
			if not a:
				new.destroy()
				console.write("Process stopped: User abort")
		
		new.destroy()

	button = Button(new, text="Use board", command=use)
	new.columnconfigure(0, weight=1)
	new.columnconfigure(1, weight=1)
	new.rowconfigure(0, weight=1)
	box.grid(column=0, row=0, columnspan=2)
	button.grid(column=1, row=1, sticky="nsew")
	new.wait_window()
	return com





def askprompt(root):
	board = ""
	fqbn = ""
	new = Toplevel(root)
	new.title("Select board")
	box = ttk.Combobox(new, values=list(ALL_BOARDS.keys()), width=50)
	def use():
		nonlocal board
		nonlocal fqbn
		fqbn = ALL_BOARDS[box.get()]
		board = box.get()
		print("SELECTED", board)
		new.destroy()
	button = Button(new, text="Use", command=use)
	new.columnconfigure(0, weight=1)
	new.columnconfigure(1, weight=1)
	new.rowconfigure(0, weight=1)
	box.grid(column=0, row=0, columnspan=2)
	button.grid(column=1, row=1, sticky="nsew")
	new.wait_window()
	return fqbn, board


class AST_visualizer:
	def __init__(self, r, console:Console, parsed:ProgramNode) -> None:
		root = Toplevel(r)
		root.title("AST visualizer")
		frame = ttk.Frame(root)
		frame.pack(fill="both", expand=True)

		scroll = ttk.Scrollbar(frame)
		scroll.pack(side="right", fill="y")
		xscroll = ttk.Scrollbar(frame, orient="horizontal")
		xscroll.pack(side="bottom", fill="x")

		self.tree = ttk.Treeview(frame, yscrollcommand=scroll.set)
		self.tree.pack(side="left", fill="both", expand=True)

		scroll.config(command=self.tree.yview)
		xscroll.config(command=self.tree.xview)

		self.tree.config(xscrollcommand=xscroll.set, yscrollcommand=scroll.set)
		self.visualize(parsed, "")
		self.tree.pack(fill=BOTH, expand=True)

	def visualize(self, node, parent):
		print("VISITING", type(node).__name__)
		current = self.tree.insert(parent, "end", text=type(node).__name__)
		print(type(node).__name__)
		print(vars(node))
		for name, value in vars(node).items():
			print(type(value), isinstance(value, Node))
			if isinstance(value, Node):
				field = self.tree.insert(current, END, text=name)
				self.visualize(value, field)
			elif isinstance(value, list):
				lst = self.tree.insert(current, "end", text=name)
				print("LIST:", name)

				for item in value:
					print(type(item), isinstance(item, Node))
					if isinstance(item, Node):
						self.visualize(item, lst)
					else:
						self.tree.insert(lst, "end", text=repr(item))
			else:
				self.tree.insert(current, END, text=f"{name} = {value!r}")



class WritingArea:
	def __init__(self, parent) -> None:
		self.f = Frame(parent)
		self.inner = Frame(self.f)

		self.text = Text(self.inner, undo=True, wrap=NONE)
		self.lines = Text(self.inner, width=5, bg="#f0f0f0", wrap=NONE, state=DISABLED)
		self.scroll = Scrollbar(self.inner)
		self.scroll2 = Scrollbar(self.f, orient="horizontal")

		self.scroll.config(command=self.callback)
		self.scroll2.config(command=self.text.xview)

		self.text.config(xscrollcommand=self.scroll2.set)
		self.text.config(yscrollcommand=self.callback2)

		self.text.bind("<<Modified>>", self.update)

		self.inner.pack(expand=True, fill="both")
		self.lines.pack(side=LEFT,fill=Y)
		self.text.pack(side=LEFT,fill=BOTH, expand=True)
		self.scroll.pack(side=RIGHT,fill=Y)
		self.scroll2.pack(side=BOTTOM,fill=X)
		self.f.config(width=500)

	def callback(self, *args):
		self.lines.yview(*args)
		self.text.yview(*args)

	def callback2(self, first, last):
		self.scroll.set(first, last)
		self.lines.yview_moveto(first)

	def update(self, e):
		lines = int(self.text.index("end-1c").split(".")[0])
		adding = "\n".join([str(i) for i in range(1, lines+1)])

		self.lines.config(state=NORMAL)
		self.lines.delete("1.0", END )
		self.lines.insert("1.0", adding)
		self.lines.config(state=DISABLED)

		self.text.edit_modified(False)

class Tab:
	def __init__(self, tab_parent, editor_parent,manager,path=None) -> None:

		print("NEW TAB CREATED")
		self.path=path
		if path:
			self.name= os.path.basename(path)
		else:
			self.name = "Untitled"
		self.header = Frame(tab_parent, relief=RAISED, bd=1)
		self.label1=Label(self.header,text=self.name)
		self.label2=Label(self.header, text="X")
		self.label1.pack(side=LEFT)
		self.label2.pack(side=LEFT)
		self.header.pack(side=LEFT)

		self.label1.bind("<Button-1>", lambda e:manager.change(self))
		self.label2.bind("<Button-1>", lambda e:manager.delete(self))

		self.frame= Frame(editor_parent)
		self.editor = WritingArea(self.frame)
		self.editor.f.pack(expand=True, fill="both")
	def __repr__(self) -> str:
		return f"Tab at {self.name}"

class TabManager:
	def __init__(self, parent) -> None:
		self.mainframe = Frame(parent)
		self.tabframe = Frame(self.mainframe)
		self.tabframe.pack(side=TOP, anchor=W, fill=BOTH)
		self.current = None
		self.current_frame = Frame(self.mainframe)
		self.tabs:list[Tab] = []
		self.current_frame.pack(side=BOTTOM, expand=True, fill=BOTH)
		self.add_tab()

	def add_tab(self, path=None):
		if self.current: 
			self.current.frame.pack_forget()
		current = Tab(self.tabframe, self.current_frame ,self,path)
		self.tabs.append(current)
		self.change(current)
		self.current = current
		

	def delete(self, tab):
		print("Deleting:", tab)
		print("Current before:", self.current)
		print("Tabs before:", [t.name for t in self.tabs])
		was_current = self.current is tab
		index=self.tabs.index(tab)-1 if tab in self.tabs else -1
		self.tabs.remove(tab)
		tab.header.destroy()
		tab.frame.destroy()

		if not self.tabs:
			self.current = None
			return
		if was_current:
			index = min(index, len(self.tabs)-1)
			self.change(self.tabs[index])
		print("Current after:", self.current)
		print("Tabs after:", [t.name for t in self.tabs])

	def change(self, tab:Tab):
		print("=== CHANGE ===")
		print("Current:", self.current)
		print("Switching to:", tab)

		print("Children before:")
		for child in self.current_frame.winfo_children():
			print(child, child.winfo_manager())
		if self.current: self.current.frame.pack_forget()

		self.current = tab

		self.current.frame.pack(side=BOTTOM, fill="both", expand=True)





class GUI:
	def __init__(self, root:Tk) -> None:
		mixer.init()
		root.title("HobbySpark")
		self.config_file = project_path/"user_data.json"
		if not os.path.exists(str(self.config_file)):
			new = Welcome(root)
			root.wait_window(new.root)
			a = {
				"name":new.name,
				"birth":new.birthday.strftime("%d|%m"),
				"age":new.age,
				"fin":None

			}
			with open(self.config_file,"w") as f:
				data_handle.dump(a, f)

		with open(self.config_file) as f:
			data = data_handle.load(f)
			self.name = data["name"]
			self.birthday = data["birth"]
			self.age = data["age"]
			self.fin = data["fin"]

		root.after(100, self.open_project)
		self.root = root
		self.opened = set()

		self.side = Frame(root)
		self.dir = ttk.Treeview(self.side)

		self.console = Console(root)
		self.editor = TabManager(root)

		self.run = LabelFrame(root, text="Run", width=300)
		self.upload_ = Button(self.run, text="Upload", command=self.upload)
		self.test_ = Button(self.run, text="Test", command=self.test)
		self.run_ = Button(self.run, text="Run", command=self.run__)
		self.transpile_check_ = Button(self.run, text="Transpile check", command=self.transpile_check)
		self.clear = Button(self.run, text="Clear console", command=lambda:self.console.clear())
		self.serial_ = Button(self.run, text="Serial monitor", command=self.serial)

		self.extra = LabelFrame(root, text="Extra options", width=300)
		self.lex_ = Button(self.extra, text="Lex", command=self.lex)
		self.parse_ = Button(self.extra, text="Parse", command=self.parse)
		self.transpile_ = Button(self.extra, text="Transpile", command=self.transpile)

		self.dir.bind("<ButtonRelease-1>", self.open_file)
		root.bind("<Control-s>", self.save)
		self.dir.bind("<Button-3>", self.on_right_click)

		root.columnconfigure(0, weight=1)
		root.columnconfigure(1,weight=1)
		root.columnconfigure(2, weight=1)
		root.columnconfigure(3, weight=1)

		root.rowconfigure(0, weight=1)
		root.rowconfigure(1,weight=1)

		self.side.config(width = 250)
		self.side.grid_propagate(False)

		self.console.str.config(height=10)
		self.console.str.grid_propagate(False)
		
		self.dir.pack(fill=BOTH, expand=True)
		self.side.grid(column=0, row=0, sticky="nsew")

		self.console.str.pack(expand=True, fill=BOTH)
		self.console.frame.grid(column=0,row=1, sticky = "nsew", columnspan=4)

		self.editor.mainframe.grid(column=1, row=0, sticky="nsew")

		self.upload_.pack(pady=5, fill=BOTH)
		self.test_.pack(pady=5, fill=BOTH)
		self.transpile_check_.pack(pady=5, fill=BOTH)
		self.run_.pack(pady=5, fill=BOTH)
		self.serial_.pack(pady=5, fill=BOTH)
		self.clear.pack(pady=5, fill=BOTH)

		self.lex_.pack(pady=5, fill=BOTH)
		self.parse_.pack(pady=5, fill=BOTH)
		self.transpile_.pack(pady=5, fill=BOTH)

		self.run.grid(row=0, column=2, sticky="nsew")
		self.extra.grid(row=0, column=3, sticky="nsew")
		self.had_last = None
		print("HELLO:", dt.date.today().strftime("%d|%m"))

		if dt.date.today().strftime("%d|%m") == self.birthday and dt.date.today().year!=self.fin:
			mb.showinfo("Happy birthday!!!!!", f"HAPPY BIRTHDAY, {self.name}. Our best wishes from the HobbySpark team. You're finally {self.age+1} years old!")
			self.age+=1
			self.fin = dt.date.today().year
			mixer.music.load(os.path.join("assets", "h.mp3"))
			mixer.music.play()

		########################################################
		#MENUS
		########################################################

		main = Menu(root)
		file = Menu(main, tearoff=False)
		file.add_command(label="Open project", command=self.open_project)
		file.add_command(label="New project", command=self.new)
		main.add_cascade(label="File", menu=file)

		preferences = Menu(main, tearoff=False)
		preferences.add_command(label="Change user data", command=self.change_pr)

		main.add_cascade(label="Preferences", menu=preferences)

		root.config(menu=main)


	def serial(self):
		com = askcom(self.root,askprompt(self.root)[1], self.console)
		baud = int(askinteger("Baudrate ", "Baud (must be int): "))
		ser = serial.Serial(com, baud)
		new = Toplevel(self.root)
		mon = Console(new, "Serial monitor")
		errr = False

		def see():
			nonlocal errr
			while ser.in_waiting:
				line = ser.readline().decode().strip()
				if line=="[@@@HOBBYSPARK ERROR 123@@@]":
					errr = True
					mon.write_error("ERROR!!!")
					break
				if errr:
					mon.write_error(line)
				else:
					mon.write(line)

			new.after(50, see)

		def finish(self):
			if ser.is_open:
				ser.close()
			new.destroy()

		new.protocol("WM_DELETE_WINDOW", finish)

		mon.str.pack(expand=True, fill=BOTH)
		mon.frame.pack(expand=True, fill=BOTH)





		



	def change_pr(self):
		def f():
			print("BIRTH", int(self.birthday.split("|")[0]))
			ab = {
				"name":name.get() if name.get()!="" else self.name,
				"birth":dt.date(2026, int(birthm.get()) if birthm.get()!="" else int(self.birthday.split("|")[1]), int(birthd.get()) if birthd.get()!="" else int(self.birthday.split("|")[0])).strftime("%d|%m"),
				"age":int(age.get()) if age.get()!="" else self.age

			}
			with open(self.config_file,"w") as f:
				data_handle.dump(ab, f)

			a.destroy()
		a = Toplevel(self.root)
		lb1 = Label(a, text="Name: ")
		name = Entry(a)
		name.insert(0, self.name)
		lb2 = Label(a, text="Age: ")
		age = Entry(a)
		age.insert(0, self.age)
		lb3 = Label(a, text="Birth Month: ")
		birthm = Entry(a)
		birthm.insert(0, int(self.birthday.split("|")[1]))
		lb4 = Label(a, text="Birth Day: ")
		birthd = Entry(a)
		birthd.insert(0, int(self.birthday.split("|")[0]))
		setb = Button(a, text="Set preferences", command=f)

		lb1.grid(row=0, column=0)
		name.grid(row=0, column=1)

		lb2.grid(row=1, column=0)
		age.grid(row=1, column=1)

		lb3.grid(row=2, column=0)
		birthm.grid(row=2, column=1)

		lb4.grid(row=3, column=0)
		birthd.grid(row=3, column=1)

		setb.grid(row=4, column=1)




	def check_if_open(self, item=""):
		for i in self.dir.get_children(item):
			value = self.dir.item(i, "values")

			if value and self.dir.item(i, "open"):
				self.opened.add(value[0])

			self.check_if_open(i)

	def new(self):
		self.path = fd.askdirectory(title="New project")
		self.check_if_open()
		for tab in self.editor.tabs:
			self.editor.delete(tab)
		with open(os.path.join(self.path, "settings.json"), "w") as f:
			default = {
				"def_board":None,
				"def_port":None
			}
			data_handle.dump(default,f)

		with open(os.path.join(self.path, "README.md"), "w") as f:
			greeter = self.get_greet()

			match greeter:
				case 0:
					greeter = f"""Good morning, {self.name}. You're early. """
				case 1:
					greeter = f"""Good afternoon, {self.name}. Had your lunch? Hopefully. """
				case 2:
					greeter = f"""Good evening, {self.name}."""
				case _:
					greeter = f"""Good night, {self.name}. You're quite late today."""

			GREETING = \
f"""#This is an automatically generated file by the HobbySpark GUI
{greeter}
---
A few folders and files in your project:
	* settings.json - You can edit this file to reduce the hassle to select com ports or boards while uploading.
		'def_board' - The **default** board. 
		'def_port' - The **default** COM port.
	
	* README.md - The file you're reading now. Just some help if it's your first time.

	* .src - Where you put your python code.

	* .src\\main.py - The main file.

	* COMPILATION - The C++ source code. Note that this appears **only after** you have either checked, uploaded, or transpiled. 

	* COMPILATION\\package.h - The HobbySpark C++ module. Feel free to see what's inside.

	* COMPILATION\\COMPILATION.ino - The transpiled code. Note: The indent levels may or may not be match your preferences. 



			"""
			f.write(GREETING)

		os.makedirs(os.path.join(self.path, ".src"), exist_ok=True)

		with open(os.path.join(self.path, ".src", "main.py"), "w") as f:
			code = \
"""from stub import *
set_board("board_name", True)
###############
#Your code here
###############
			"""
			f.write(code)

		self.dir.delete(*self.dir.get_children())
		self.build_tree("", self.path)


	def get_greet(self):
		hour = dt.datetime.now().hour

		if 5 <= hour < 12:
			return 0
		elif 12 <= hour < 17:
			return 1
		elif 17 <= hour < 21:
			return 2
		else:
			return 3
	


	def build_tree(self, parent, root):
		for tab in self.editor.tabs:
			self.editor.delete(tab)
		if parent == "":
			parent = self.dir.insert(
	    		"",
	    		END,
	    		text=os.path.basename(root),
	    		values=(root,)
	        )

			if root in self.opened:
				self.dir.item(parent, open=True)

		for a in os.listdir(root):

			full = os.path.join(root, a)

			node = self.dir.insert(parent, END, text=a, values=(full,))

			if full in self.opened:
				self.dir.item(node, open=True)

			if os.path.isdir(full):
				self.build_tree(node, full)

	def lex(self):
		if self.run__():return
		text = self.editor.current.editor.text.get("1.0",END)
		self.console.write("Lexing is the process of turning text into a list of tokens. Tokens can have a position, a type and a value. ")
		try:
			lexed = Lexer(text).evaluate()
		except Exception as e:
			self.console.write(f"Whoops, you made an error. {e}")

		self.console.write(f"An example of a token list is {lexed}.")
		self.console.write_warning("Do not worry if you do not understand this. This command is merely for curious users to see what happens inside of HobbySpark. ")

	def parse(self): 
		if self.run__(): return
		text = self.editor.current.editor.text.get("1.0",END)
		try:
			lexed = Lexer(text).evaluate()
		except Exception as e:
			self.console.write(f"Whoops, you made an error while lexing. {e}")

		try:
			parsed = Parser(lexed).parse()
		except Exception as e:
			self.console.write(f"Whoops, you made an error {e}.")

		self.console.write(
		"Parsing is the process of turning a list of tokens into an Abstract Syntax Tree (AST). "
		"The AST describes the structure and meaning of your program."
		)

		self.console.write_warning(
			"Do not worry if you do not understand the AST. "
			"This command is mainly for curious users who want to see how HobbySpark understands their code."
		)

		AST_visualizer(self.root, self.console, parsed)

	def transpile(self): 
		if self.run__(): return
		text = self.editor.current.editor.text.get("1.0",END)
		try:
			lexed = Lexer(text).evaluate()
		except Exception as e:
			self.console.write(f"Whoops, you made an error while lexing. {e}")

		try:
			parsed = Parser(lexed).parse()
		except Exception as e:
			self.console.write(f"Whoops, you made an error  while parsing {e}.")

		try:
			transpiled = Transpiler(parsed).translate()

		except Exception as e:
			self.console.write(f"Whoops, you made an error {e}.")

		self.console.write("HobbySpark at it's core, uses transpilation from python to C++.", "Transpiling is the process of turning source code (like python) to destination code (like C++). ", "A example of your code transpiled to C++ is: ", "\n".join(transpiled))
		self.console.write_warning("The transpiled code is NOT supposed to be ''reader friendly''. ", "The code may have unreadable code.", "Do not worry if you cannot articulate or understand the C++. ")
		

	def upload(self):
		if self.run__():
			return
		text = self.editor.current.editor.text.get("1.0",END)
		self.console.write("Lexing")
		try: 
			lexed = Lexer(text).evaluate()
			self.console.write("Lexed")
		except Exception as e:
			self.console.write_error(f"Failed to lex code, {e}")
			return

		self.console.write("Parsing")
		try: 
			parsed = Parser(lexed).parse()
			self.console.write("Parsed")
		except Exception as e:
			self.console.write_error(f"Failed to parse code, {e}")
			return

		self.console.write("Transpiling")
		try: 
			transpiled = Transpiler(parsed).translate()
			self.console.write("Transpiled")
		except Exception as e:
			self.console.write_error(f"Failed to transpile code, {e}")
			return

		self.check_if_open()

		os.makedirs(os.path.join(self.path, "COMPILATION"), exist_ok=True)
		with open(os.path.join(self.path, "COMPILATION", "COMPILATION.ino"), "w") as f:
			f.write("\n".join(transpiled))

		with open(os.path.join(self.path, "COMPILATION", "package.h"), "w") as f:
			with open("package.h", "r") as f2:
				f.write(f2.read())

		
		self.dir.delete(*self.dir.get_children())
		self.build_tree("", self.path)
		if os.path.exists(os.path.join(self.path, "settings.json")):
			with open(os.path.join(self.path, "settings.json")) as f:
				loaded = data_handle.load(f)["def_board"]
				if loaded is not None: fqbn = ALL_BOARDS[loaded], loaded
				else: fqbn = askprompt(self.root)
		else: fqbn = askprompt(self.root)

		result = subprocess.run(
		    [
		        "arduino-cli",
		        "compile",
		        "--fqbn",
		        fqbn[0],
		        os.path.join(self.path, "COMPILATION")
		    ],
		    capture_output=True,
		    text=True
		)
		if result.stderr:
			self.console.write_error(f"Failed to compile, {result.stderr}")
			return
		self.console.write("Compiled sucessfully")
		self.console.write("Uploading...")
		print("A",fqbn[1])
		if os.path.exists(os.path.join(self.path, "settings.json")):
			with open(os.path.join(self.path, "settings.json")) as f:
				loaded=data_handle.load(f)["def_port"]
				if loaded is not None: board = loaded
				else: board=askcom(self.root, fqbn[1], self.console)
		else: board=askcom(self.root, fqbn[1], self.console)
		
		self.console.write("Uploading...")
		result = subprocess.run(
		    [
		        "arduino-cli",
		        "upload",
		        "-p",
		        board,
		        "--fqbn",
		        fqbn[0],
		        os.path.join(self.path, "COMPILATION")
		    ],
		    capture_output=True,
		    text=True
		)
		if result.stderr:
			self.console.write_error(f"Could not upload, {result.stderr}")
			return
		self.console.write(f"Uploaded, {result.stdout}")


	def test(self):
		if self.run__():
			return
		text = self.editor.current.editor.text.get("1.0",END)
		self.console.write("Lexing")
		try: 
			lexed = Lexer(text).evaluate()
			self.console.write("Lexed")
		except Exception as e:
			self.console.write_error(f"Failed to lex code, {e}")
			return

		self.console.write("Parsing")
		try: 
			parsed = Parser(lexed).parse()
			self.console.write("Parsed")
		except Exception as e:
			self.console.write_error(f"Failed to parse code, {e}")
			return

		self.console.write("Transpiling")
		try: 
			transpiled = Transpiler(parsed).translate()
			self.console.write("Transpiled")
		except Exception as e:
			self.console.write_error(f"Failed to transpile code, {e}")
			return

		os.makedirs(os.path.join(self.path, "COMPILATION", self.editor.current.name), exist_ok=True)
		with open(os.path.join(self.path, "COMPILATION",self.editor.current.name, "COMPILATION.ino"), "w") as f:
			f.write("\n".join(transpiled))

		with open(os.path.join(self.path, "COMPILATION", "package.h"), "w") as f:
			with open("package.h", "r") as f2:
				f.write(f2.read())
		self.check_if_open()
		self.dir.delete(*self.dir.get_children())
		self.build_tree("", self.path)
		if os.path.exists(os.path.join(self.path, "settings.json")):
			with open(os.path.join(self.path, "settings.json")) as f:
				loaded = data_handle.load(f)["def_board"]
				if loaded is not None: fqbn = ALL_BOARDS[loaded]
				else: fqbn = askprompt(self.root)[0]
		else: fqbn = askprompt(self.root)[0]
		print("FQBN", fqbn)

		result = subprocess.run(
		    [
		        "arduino-cli",
		        "compile",
		        "--fqbn",
		        fqbn,
		        os.path.join(self.path, "COMPILATION")
		    ],
		    capture_output=True,
		    text=True
		)
		if result.stderr:
			self.console.write_error(f"Failed to compile, {result.stderr}")
			return
		self.console.write("Compiled sucessfully")


		


	def transpile_check(self):
		self.run__()
		text = self.editor.current.editor.text.get("1.0",END)
		self.console.write("Lexing")
		try: 
			lexed = Lexer(text).evaluate()
			self.console.write("Lexed")
		except Exception as e:
			self.console.write_error(f"Failed to lex code, {e}")
			return

		self.console.write("Parsing")
		try: 
			parsed = Parser(lexed).parse()
			self.console.write("Parsed")
		except Exception as e:
			self.console.write_error(f"Failed to parse code, {e}")
			return

		self.console.write("Transpiling")
		try: 
			transpiled = Transpiler(parsed).translate()
			self.console.write("Transpiled")
		except Exception as e:
			self.console.write_error(f"Failed to transpile code, {e}")
			return

	def run__(self):
		self.save()
		self.console.write("Running")
		result = subprocess.run([sys.executable, self.editor.current.path], capture_output=True, text=True)
		if result.stderr:
			self.console.write_error(f"Could not run: {result.stderr}")
			return True
		self.console.write("Ran sucessfully: ")
		self.console.write(result.stdout)
		

	def open_project(self):
		self.dir.delete(*self.dir.get_children())
		for a in self.editor.tabs:
			self.editor.delete(a)
		self.path = fd.askdirectory()
		if self.path:
			self.build_tree("",self.path)

	def open_file(self, e):
		if self.editor.tabs.__len__()>0:
			if self.editor.tabs[0].name=="Untitled":
				self.editor.tabs[0].frame.pack_forget()
				self.editor.tabs[0].header.pack_forget()
				self.editor.tabs.pop()

		if len((self.dir.item(self.dir.focus()))['values'])<=0: return
		real = (self.dir.item(self.dir.focus()))['values'][0]
		ext = (os.path.splitext(real)[1].lower())[1:]


		if not os.path.isfile(real):
			return

		try:	
			with open(real, 'r') as f:
				data = f.read()
				paths = [t.path for t in self.editor.tabs]

				if real in paths:
					self.editor.change(self.editor.tabs[paths.index(real)])
					return
				else:
					self.editor.add_tab(real)

				self.editor.current.editor.text.delete("1.0", END)
				self.editor.current.editor.text.insert("1.0", data)
		except UnicodeError:
			mb.showwarning("Unsupported file format warning", f"The file {os.path.basename(real)} with extension '{ext}' is not a supported file format. ", detail="Try file formats like .py, .hb, .ino, etc. ")

	def save(self, e=0):
		self.console.write("Saving... ")

		read = self.editor.current.editor.text.get("1.0", END)
		try:
			with open(self.editor.current.path, 'w') as f:
				f.write(read)
				self.console.write(f"Saved {os.path.basename(self.editor.current.name)}")
		except Exception as f:
			self.console.write_error(f"Failed to save: {f}")

	def on_right_click(self, event):
		obj = self.dir.identify_row(event.y)
		if not obj:return
		path = self.dir.item(obj)['values'][0]

		def new_file():
			name = askstring("New file","New file: ")
			new = os.path.join(path, name)
			if os.path.exists(new): 
				mb.showerror("File exists", f"The file {name} already exists") 
				return
			open(new,"w").close()
			self.check_if_open()
			self.dir.delete(*self.dir.get_children())
			self.build_tree("", self.path)
			self.editor.add_tab(new)


		def new_folder():
			name = askstring("New folder","New folder: ")
			new = os.path.join(path, name)
			if os.path.exists(new): 
				mb.showerror("Folder exists" , f"The folder {name} already exists. ") 
				return
			os.makedirs(new)
			self.check_if_open()
			self.dir.delete(*self.dir.get_children())
			self.build_tree("", self.path)

		def delete():
			if os.path.isfile(path):
				os.remove(path)
				current = [a.path for a in self.editor.tabs]


				if path in current:
					self.editor.delete(self.editor.tabs[current.index(path)])

				self.dir.selection_remove(self.dir.selection())
				self.dir.focus("")
				self.check_if_open()
				self.dir.delete(*self.dir.get_children())
				self.build_tree("", self.path)
			else:
				current = [a.name for a in self.editor.tabs]
				all_files = os.listdir(path)

				for a in all_files:
					if a in current:
						self.editor.delete(self.editor.tabs[current.index(a)])
				shutil.rmtree(path)
				self.check_if_open()
				self.dir.delete(*self.dir.get_children())
				self.build_tree("", self.path)
				



		def rename():
			name = os.path.join(os.path.dirname(path),askstring("Rename","Rename: "))
			if os.path.exists(name):
				mb.showerror("Name already exists" , f"The name {name} already exists. ")
				return
			os.rename(path, name)
			self.check_if_open()
			self.dir.delete(*self.dir.get_children())
			self.build_tree("", self.path)

		fo_m = Menu(self.root, tearoff=0)
		fo_m.add_command(label="New file", command=new_file)
		fo_m.add_command(label="New folder", command=new_folder)
		fo_m.add_separator()
		fo_m.add_command(label="Delete", command=delete)
		fo_m.add_command(label="Rename", command=rename)

		f_m = Menu(self.root, tearoff=0)
		f_m.add_command(label="Delete", command=delete)
		f_m.add_command(label="Rename", command=rename)

		if os.path.isdir(path):
			fo_m.tk_popup(event.x_root, event.y_root)
		else:
			f_m.tk_popup(event.x_root,event.y_root)




	

a = Tk()
b = GUI(a)
a.mainloop()
