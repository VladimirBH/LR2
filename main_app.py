from math import e
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from functools import partial
from turtle import width
import for_xml
import xml.etree.ElementTree as ET

class MainApp(Tk):
        
    def __init__(self):
        super().__init__()
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        self.resizable(0,0)
        self.option_add("*Font", default_font)
        self.title("") 
        self.iconbitmap(default='transparent.ico')
        style = ttk.Style()
        style.theme_use('clam')
        tab_control = ttk.Notebook(self)
        style.configure('My.TFrame', background='#f4f4f4', borderwidth=0)
        style.configure('W.TButton', background='#e3e3e3', relief=RIDGE, borderwidth=1, width=20, height=2)
        
        tab1 = ttk.Frame(tab_control, style="My.TFrame")  
        tab2 = ttk.Frame(tab_control, style="My.TFrame") 
        tab3 = ttk.Frame(tab_control, style="My.TFrame")
        tab_control.add(tab1, text='Признаки')  
        tab_control.add(tab2, text='Правила')  
        tab_control.add(tab3, text='Виды спорта')
        tab_control.grid(row=0)
        style.configure("Treeview.Heading", background="grey", font=("TkDefaultFont", 10))

        treeview1 = ttk.Treeview(tab1, selectmode='browse', columns='name', show="")

        treeview1.column('name',anchor='w', width=700)
        treeview1.anchor = CENTER
        treeview1.grid(row=0)


        def onAddClick(id_tab):
            res = self.onAdd(id_tab)
            if res != None:
                if id_tab == 0:
                    treeview1.insert(parent='',index='end', text='', values=(res,))
                elif id_tab == 1:
                    treeview2.insert(parent='',index='end',text='',values=(res['attrib']['if'],res['attrib']['else']))
                elif id_tab == 2:
                    treeview3.insert(parent='',index='end',text='',values=(res['attrib']['name'], res['subelements'][0]['text'], 
                                                                        res['subelements'][1]['text'], 
                                                                        res['subelements'][2]['text']))


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
        
           
        add_button_tab1 = ttk.Button(tab1, text="Добавить", command=partial(onAddClick, 0), style='W.TButton')
        add_button_tab1.grid(row=1, pady=5)

        delete_button_tab1 = ttk.Button(tab1, text="Удалить", command=partial(onDeleteClick, 0), style='W.TButton')
        delete_button_tab1.grid(row=2, pady=5)

        submit_button_tab1 = ttk.Button(tab1, text="Подобрать вид спорта", command=onSubmitClick, style='W.TButton')
        submit_button_tab1.grid(row=3, pady=5)

        tab2.grid_columnconfigure(0, weight=1)
        treeview2 = ttk.Treeview(tab2, selectmode='browse', show='headings')

        treeview2['columns'] = ('if', 'else')

        treeview2.column("if",anchor=CENTER,width=250)
        treeview2.column("else",anchor=CENTER,width=250)

        treeview2.heading("if",text="ЕСЛИ",anchor=CENTER)
        treeview2.heading("else",text="ТО",anchor=CENTER)

        treeview2.grid(row=0)

        add_button_tab2 = ttk.Button(tab2, text="Добавить", command=partial(onAddClick, 1), style='W.TButton')
        add_button_tab2.grid(row=1, pady=5)
        
        delete_button_tab2 = ttk.Button(tab2, text="Удалить", command=partial(onDeleteClick, 1), style='W.TButton')
        delete_button_tab2.grid(row=2, pady=5)


        treeview3 = ttk.Treeview(tab3, selectmode='browse')

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
        treeview3.grid(row=0)

        add_button_tab3 = ttk.Button(tab3, text="Добавить", command=partial(onAddClick, 2), style='W.TButton')
        add_button_tab3.grid(row=1, pady=5)

        delete_button_tab3 = ttk.Button(tab3, text="Удалить", command=partial(onDeleteClick, 2), style='W.TButton')
        delete_button_tab3.grid(row=2, pady=5)

        rules = for_xml.loadXml('rules.xml')

        for i in range (0, len(rules)):
            treeview2.insert(parent='',index='end',iid=i,text='',values=(rules[i].attrib['if'],rules[i].attrib['else']))

        sport_types = for_xml.loadXml('types_of_sports.xml')

        for i in range (0, len(sport_types)):
            treeview3.insert(parent='',index='end',iid=i,text='',values=(
            sport_types[i].attrib['name'],
            sport_types[i].find('stamina').text,
            sport_types[i].find('flexibility').text,
            sport_types[i].find('power').text))



    #Добавление элементов

    def onAdd(self, id_tab):
        add_window = Toplevel(self)
        if id_tab == 0:
            add_window.title("Добавить необходимое свойство")
            text_box = Entry(add_window, width=50)
            text_box.grid(row=0, column=0, padx=20, pady=20)

            result = None
            def callback():
                nonlocal result
                if len(text_box.get()) == 0:
                    messagebox.showerror(message="Поле должно быть заполнено")
                    return
                result = text_box.get()
                add_window.destroy()

            button = Button(add_window, text="Подтвердить", command=callback)
            button.grid(row=0, column=1, padx=20, pady=20)

            add_window.grab_set()
            add_window.wait_window()
            return result
        elif id_tab == 1:
            add_window.title("Добавить правило")
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
                element = {
                    'tag': 'rule',
                    'attrib': 
                        {
                            'else': text_box_else.get().upper(),
                            'if': text_box_if.get().upper()
                        },
                    'subelements': []
                }
                for_xml.add_element_in_xml('rules.xml', element=element)
                result = element
                add_window.destroy()
            button = Button(add_window, text="Добавить", command=callback)
            button.grid(row=2, column=0, padx=20, pady=20)

            add_window.grab_set()
            add_window.wait_window()
            return result
        elif id_tab == 2:
            add_window.title("Добавить вид спорта")
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
                element = {
                    'tag': 'type',
                    'attrib': 
                        {
                            'name': text_box_name.get()
                        },
                    'subelements': [
                    {
                        'name': 'stamina',
                        'text': label_stamina.cget('text') + ' ' + combo_box_stamina.get()
                    },
                    {
                        'name': 'flexibility',
                        'text': label_flexibility.cget('text') + ' ' + combo_box_flexibility.get()
                    },
                    {
                        'name': 'power',
                        'text': label_power.cget('text') + ' ' + combo_box_power.get()
                    }
                    ]
                }
                for_xml.add_element_in_xml('types_of_sports.xml', element=element)					
                result = element
                add_window.destroy()

            button = Button(add_window, text="Добавить", command=callback)
            button.grid(row=7, column=0, padx=20, pady=20)

            add_window.grab_set()
            add_window.wait_window()
            return result

    def onDelete(self, id_tab, value):
        if id_tab == 1:
            for_xml.delete_element_in_xml('rules.xml', value)
        elif id_tab == 2:
            for_xml.delete_element_in_xml('types_of_sports.xml', value)


    def onSubmit(self, treeview: ttk.Treeview):
        if len(treeview.get_children()) == 0:
            messagebox.showerror("Ошибка", "Укажите признаки")
            return
        rules = for_xml.loadXml('rules.xml')
        sport_types = for_xml.loadXml('types_of_sports.xml')
        advices = []
        for line in treeview.get_children():
            for sign in treeview.item(line)['values']:
                for rule in rules:
                    if rule.attrib['if'].lower() in sign.lower():
                        advices.append(rule.attrib['else'].lower())

        suitable_sport = []
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
        add_window.title("Подходящие виды спорта")
        treeview = ttk.Treeview(add_window, columns=('name'), show="")
        treeview.column("name",anchor=CENTER,)
        treeview.grid(column=0, row=0) 

        for sport_type in suitable_sport:
            treeview.insert(parent='',index='end',text='',values=(sport_type,))

        add_window.grab_set()
        add_window.wait_window()
        