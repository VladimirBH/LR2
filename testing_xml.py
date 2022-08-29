import xml.etree.ElementTree as ET

def main():
    tree = ET.parse('rules.xml')
    rules = tree.getroot()
    for rule in rules:
        print(rule.attrib['else'])
   

    
    #################################################################
    #                                                               #
    #                    Добавление элемента в XML                  #
    #                                                               #
    #################################################################
    
def add_element():
    tree = ET.parse('types_of_sports.xml')
    root = tree.getroot()
    attrib = { 
              'name': "Легкая атлетика" 
              }
    element = root.makeelement('type', attrib)
    root.append(element)
    ET.SubElement(root[-1], 'stamina')
    root[-1][0].text = "На выносливость Большое"
    ET.SubElement(root[-1], 'flexibility')
    root[-1][1].text = "На гибкость Среднее"
    ET.SubElement(root[-1], 'power')
    root[-1][2].text = "На силу Среднее"
    tree.write('types_of_sports1.xml', encoding="utf-8")
    
    #################################################################
    
    
    #################################################################
    #                                                               #
    #                    Удаление элемента в XML                    #
    #                                                               #
    #################################################################
    
    
def delete_element():
    tree = ET.parse('types_of_sports.xml')
    root = tree.getroot()
    for type in root:
        if(type.attrib['name'] == "Легкая атлетика"):
            type.remove()
    tree.write('types_of_sports1.xml', encoding="utf-8")
    
    
    #################################################################
    


    #################################################################
    #                                                               #
    #                    Изменение элемента в XML                   #
    #                                                               #
    #################################################################
    
def update_element():
    tree = ET.parse('types_of_sports.xml')
    root = tree.getroot()
    for type in root.iter('value'):
        if(type.attrib['name'] == 'Плавание'):
            print(type.attrib['name'])
            type.set('name', 'Бех')
    tree.write('types_of_sports1.xml', encoding="utf-8")    
    
    
    #################################################################

if __name__ == "__main__":
    main()
