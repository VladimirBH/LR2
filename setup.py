from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import xml.etree.ElementTree as ET


list_of_attribs = []


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
		#tab_control.pack(expand=1, fill='both') 
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
				treeview1.insert(parent='',index='end', text='', values=(res,))
			elif id_tab == 1:
				treeview2.insert(parent='',index='end',text='',values=(res.attrib['if'],res.attrib['else']))
			elif id_tab == 2:
				treeview3.insert(parent='',index='end',text='',values=(res.attrib['name']))
    
    
		def onDeleteClick(id_tab):
			if id_tab == 0:
				treeview1.delete(treeview1.selection()[0])
			elif id_tab == 1:
				values = treeview2.item(treeview2.selection()[0], option="values")
				treeview2.delete(treeview2.selection()[0])
				self.onDelete(id_tab, values)
			elif id_tab == 2:
				values = treeview3.item(treeview3.selection()[0], option="values")
				treeview3.delete(treeview3.selection()[0])
				self.onDelete(id_tab, values)
	
 
		def onSubmitClick():
			self.onSubmit(treeview1)
			
		add_button_tab1 = ttk.Button(tab1, text="Добавить", command=partial(onAddClick, 0))
		add_button_tab1.grid(row=1, column=0)

		delete_button_tab1 = ttk.Button(tab1, text="Удалить", command=partial(onDeleteClick, 0))
		delete_button_tab1.grid(row=2, column=0)

		submit_button_tab1 = ttk.Button(tab1, text="Подобрать вид спорта", command=onSubmitClick)
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

		delete_button_tab2 = ttk.Button(tab2, text="Удалить", command=partial(onDeleteClick, 1))
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

		delete_button_tab3 = ttk.Button(tab3, text="Удалить", command=partial(onDeleteClick, 2))
		delete_button_tab3.grid(row=2, column=0)

		rules = self.loadXml('rules.xml')

		for i in range (0, len(rules)-1):
			treeview2.insert(parent='',index='end',iid=i,text='',values=(rules[i].attrib['if'],rules[i].attrib['else']))

		sport_types = self.loadXml('types_of_sports.xml')

		for i in range (0, len(sport_types)-1):
			treeview3.insert(parent='',index='end',iid=i,text='',values=(
			sport_types[i].attrib['name'],
			sport_types[i].find('stamina').text,
			sport_types[i].find('flexibility').text,
			sport_types[i].find('power').text))


	def loadXml(self, file_name: str):
		tree = ET.parse(file_name)
		return tree.getroot()

    #Добавление элементов
    
	def onAdd(self, id_tab):
		add_window = Toplevel(self)
		if id_tab == 0:
			add_window.title = "Добавить необходимое свойство"
			text_box = Entry(add_window, width=50)
			text_box.grid(row=0, column=0, padx=20, pady=20)
   
			result = None
			def callback():
				nonlocal result
				if len(text_box.get()) == 0:
					messagebox.showerror(message="Поле должно быть заполнено")
					return
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
				if len(text_box_if.get()) == 0 or len(text_box_else.get()) == 0:
					messagebox.showerror(message="Поля должны быть заполнены")
					return
				nonlocal result
				tree = ET.parse('rules.xml')
				root = tree.getroot()
				attrib = { 
              		'if': text_box_if.get().upper(),
					'else': text_box_else.get().upper()
              	}
				element = root.makeelement('rule', attrib)
				root.append(element)
				tree.write('rules.xml', encoding="utf-8")
				result = element
				add_window.destroy()
    
			button = Button(add_window, text="Добавить", command=callback)
			button.grid(row=2, column=0, padx=20, pady=20)

			add_window.grab_set()
			add_window.wait_window()
			return result
		elif id_tab == 2:
			add_window.title = "Добавить вид спорта"
			text_box_name = Entry(add_window, width=50)
			text_box_name.grid(row=0, column=0, padx=20, pady=20)
   
			values = [ "Лёгкое", "Среднее", "Большое"]
      
			label_stamina = Label(add_window, text="На выносливость")
			label_stamina.grid(row=1, column=0, padx=20, pady=20)

			combo_box_stamina = ttk.Combobox(add_window, values=values, width=50, state="readonly")
			combo_box_stamina.grid(row=2, column=0, padx=20, pady=20)
			combo_box_stamina.current(0)

			label_flexibility = Label(add_window, text="На гибкость")
			label_flexibility.grid(row=3, column=0, padx=20, pady=20)

			combo_box_flexibility = ttk.Combobox(add_window, values=values, width=50, state="readonly")
			combo_box_flexibility.grid(row=4, column=0, padx=20, pady=20)
			combo_box_flexibility.current(0)
			
			label_power = Label(add_window, text="На силу")
			label_power.grid(row=5, column=0, padx=20, pady=20)
   
			combo_box_power = ttk.Combobox(add_window, values=values, width=50, state="readonly")
			combo_box_power.grid(row=6, column=0, padx=20, pady=20)
			combo_box_power.current(0)
   
			result = None
			def callback():
				if len(text_box_name.get()) == 0:
					messagebox.showerror(message="Поле должно быть заполнено")
					return
				nonlocal result
				tree = ET.parse('types_of_sports.xml')
				root = tree.getroot()
				attrib = { 
						'name': text_box_name.get()
						}
				element = root.makeelement('type', attrib)
				root.append(element)
				ET.SubElement(root[-1], 'stamina')
				root[-1][0].text = label_stamina.cget('text') + ' ' + combo_box_stamina.get()
				ET.SubElement(root[-1], 'flexibility')
				root[-1][1].text = label_flexibility.cget('text') + ' ' + combo_box_flexibility.get()
				ET.SubElement(root[-1], 'power')
				root[-1][2].text = label_power.cget('text') + ' ' + combo_box_power.get()
				tree.write('types_of_sports.xml', encoding="utf-8")						
				result = element
				add_window.destroy()
    
			button = Button(add_window, text="Добавить", command=callback)
			button.grid(row=7, column=0, padx=20, pady=20)

			add_window.grab_set()
			add_window.wait_window()
			return result
   
	def onDelete(self, id_tab, value):
		if id_tab == 1:
			tree = ET.parse('rules.xml')
			root = tree.getroot()
			for rule in root:
				if(rule.attrib['if'] == value[0] and rule.attrib['else'] == value[1]):
					root.remove(rule)
			tree.write('rules.xml', encoding="utf-8")
		elif id_tab == 2:
			tree = ET.parse('types_of_sports.xml')
			root = tree.getroot()
			for type in root:
				if type.attrib['name'] == value[0]:
					print(type.attrib['name'])
					root.remove(type)
			tree.write('types_of_sports.xml', encoding="utf-8")


	def onSubmit(self, treeview: ttk.Treeview):
		rules = self.loadXml('rules.xml')
		sport_types = self.loadXml('types_of_sports.xml')
		advices = []
		for line in treeview.get_children():
			for sign in treeview.item(line)['values']:
				for rule in rules:
					if rule.attrib['if'].lower() in sign.lower():
						advices.append(rule.attrib['else'].lower())

		suitable_sport = []
		print(advices)
		for sport_type in sport_types:
			suit = 1
			for advice in advices:
				if "выносливость" in advice:
					if sport_type.find('stamina').text.lower() not in advice:
						suit -= 1
						continue
				if "гибкость" in advice:
					if sport_type.find('flexibility').text.lower() not in advice:
						suit -= 1
						continue
				if "силу" in advice:
					if sport_type.find('power').text.lower() not in advice:
						suit -= 1
						continue
			if suit > 0:
				suitable_sport.append(sport_type.attrib['name'])

		self.windowResult(suitable_sport)


	def windowResult(self, suitable_sport):
		add_window = Toplevel(self)
		add_window.title = "Подходящие виды спорта"
		treeview = ttk.Treeview(add_window, columns=('name'))
		treeview.column("#0", width=0)
		treeview.column("name",anchor=CENTER, width=700)
		treeview.grid(column=0, row=0) 

		for sport_type in suitable_sport:
			treeview.insert(parent='',index='end',text='',values=(sport_type,))

		add_window.grab_set()
		add_window.wait_window()


if __name__ == "__main__":
	main_app = MainApp()
	main_app.mainloop()