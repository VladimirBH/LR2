from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import xml.etree.ElementTree as ET

class MainApp(Tk):
	
	def __init__(self):
		super().__init__()
		self.title("name")  
		self.geometry('1000x500')  
		tab_control = ttk.Notebook(self)
		tab1 = ttk.Frame(tab_control)  
		tab2 = ttk.Frame(tab_control) 
		tab3 = ttk.Frame(tab_control)  
		tab_control.add(tab1, text='Признаки')  
		tab_control.add(tab2, text='Правила')  
		tab_control.add(tab3, text='Виды спорта')
		tab_control.grid(row=0)

		treeview1 = ttk.Treeview(tab1, columns=('name'))

		treeview1.grid(row=0, column=0)
		treeview1.column("#0", width=0)
		treeview1.column("name",anchor=CENTER, width=700)


		treeview1.heading("#0",text="",anchor=CENTER)
		treeview1.heading("name",text="Признаки",anchor=CENTER)
		treeview1.grid(column=0, row=0)  

		def onAddClick(id_tab):
			res = self.onAdd(id_tab)
			if id_tab == 0:
				treeview1.insert(parent='',index='end',text='',values=(res))
			elif id_tab == 1:
				print(1)
			elif id_tab == 2:
				print(2)
   
		add_button_tab1 = ttk.Button(tab1, text="Добавить", command=partial(onAddClick, 0))
		add_button_tab1.grid(row=1, column=0)

		delete_button_tab1 = ttk.Button(tab1, text="Удалить", command=partial(self.onDeleteClick, 0))
		delete_button_tab1.grid(row=2, column=0)

		submit_button_tab1 = ttk.Button(tab1, text="Подобрать вид спорта", command=self.onSubmitClick)
		submit_button_tab1.grid(row=3, column=0)

		treeview2 = ttk.Treeview(tab2)

		treeview2['columns'] = ('if', 'else')

		treeview2.column("#0", width=0,  stretch=NO)
		treeview2.column("if",anchor=CENTER, width=350)
		treeview2.column("else",anchor=CENTER,width=350)

		treeview2.heading("#0",text="",anchor=CENTER)
		treeview2.heading("if",text="ЕСЛИ",anchor=CENTER)
		treeview2.heading("else",text="ТО",anchor=CENTER)
		treeview2.grid(column=0, row=0) 

		add_button_tab2 = ttk.Button(tab2, text="Добавить", command=partial(onAddClick, 1))
		add_button_tab2.grid(row=1, column=0)

		delete_button_tab2 = ttk.Button(tab2, text="Удалить", command=partial(self.onDeleteClick, 1))
		delete_button_tab2.grid(row=2, column=0)

		treeview3 = ttk.Treeview(tab3)

		treeview3['columns'] = ('name', 'par1', 'par2', 'par3')

		treeview3.column("#0", width=0,  stretch=NO)
		treeview3.column("name",anchor=CENTER, width=100)
		treeview3.column("par1",anchor=CENTER, width=200)
		treeview3.column("par2",anchor=CENTER, width=200)
		treeview3.column("par3",anchor=CENTER, width=200)

		treeview3.heading("#0",text="",anchor=CENTER)
		treeview3.heading("name",text="Название",anchor=CENTER)
		treeview3.heading("par1",text="Воздействие на выносливость",anchor=CENTER)
		treeview3.heading("par2",text="Воздействие на гибкость",anchor=CENTER)
		treeview3.heading("par3",text="Воздействие на силу",anchor=CENTER)
		treeview3.grid(column=0, row=0)

		add_button_tab3 = ttk.Button(tab3, text="Добавить", command=partial(onAddClick, 2))
		add_button_tab3.grid(row=1, column=0)

		delete_button_tab3 = ttk.Button(tab3, text="Удалить", command=partial(self.onDeleteClick, 2))
		delete_button_tab3.grid(row=2, column=0)

		self.loadXmlRules(treeview2)
		self.loadXmlSport(treeview3)
	
	def loadXmlRules(self, tab2):
		tree = ET.parse('rules.xml')
		rules = tree.getroot()
		i = 0
		for rule in rules:
			tab2.insert(parent='',index='end',iid=i,text='',values=(rule.attrib['if'],rule.attrib['else']))
			i += 1
	
	def loadXmlSport(self, tab3):
		tree = ET.parse('types_of_sports.xml')
		root = tree.getroot()
		i = 0
		for type_sport in root:
			tab3.insert(parent='',index='end',iid=i,text='',values=(
		type_sport.attrib['name'],
		type_sport.find('stamina').text,
		type_sport.find('flexibility').text,
		type_sport.find('power').text))
			i += 1
    
	def onAdd(self, id_tab):
		add_window = Toplevel(self)
		if id_tab == 0:
			add_window.title = "Добавить необходимое свойство"
			text_box = Entry(add_window, width=50)
			text_box.grid(row=0, column=0, padx=20, pady=20)
   
			result = None
			def callback():
				if len(text_box.get()) == 0:
					messagebox.showerror(message="Поле должно быть заполнено")
					return
				nonlocal result
				result = text_box.get()
				list_of_attribs.append(result)
				add_window.destroy()
    
			button = Button(add_window, text="Подтвердить", command=callback)
			button.grid(row=0, column=1, padx=20, pady=20)

			add_window.grab_set()
			add_window.wait_window()
			return result
		elif id_tab == 1:
			add_window.title = "Добавить правило"
			text_box_if = Entry(add_window, width=50)
			text_box_if.grid(row=0, column=0, padx=20, pady=20)
			text_box_else = Entry(add_window, width=50)
			text_box_else.grid(row=1, column=0, padx=20, pady=20)
			result = None
			def callback():
				if len(text_box_if.get()) == 0 and len(text_box_else.get()) == 0:
					messagebox.showerror(message="Поля должны быть заполнены")
					return
				nonlocal result
				result = text_box.get()
				list_of_attribs.append(result)
				add_window.destroy()
    
			button = Button(add_window, text="Добавить", command=callback)
			button.grid(row=2, column=0, padx=20, pady=20)

			add_window.grab_set()
			add_window.wait_window()
			return result
		elif id_tab == 2:
			print(2)
   

	def onDeleteClick(self, id_tab):
		if id_tab == 0:
			print(0)
		elif id_tab == 1:
			print(1)
		elif id_tab == 2:
			print(2)

	def onSubmitClick(self):
		print('what')