import xml.etree.ElementTree as ET

def loadXml(file_name: str):
    tree = ET.parse(file_name)
    return tree.getroot()

def add_element_in_xml(file_name: str, element: dict):
    tree = ET.parse(file_name)
    root = tree.getroot()
    tree_element = root.makeelement(element['tag'], element['attrib'])
    root.append(tree_element)
    length = len(element['subelements'])
    if length != 0:
        for i in range(0, length):
            ET.SubElement(root[-1], element['subelements'][i]['name'])
            root[-1][i].text = element['subelements'][i]['text']
    tree.write(file_name, encoding="utf-8")

def delete_element_in_xml(file_name: str, value):
    tree = ET.parse(file_name)
    root = tree.getroot()
    if 'rules.xml' == file_name:
        for element in root:
            if element.attrib['if'] == value[0] and element.attrib['else'] == value[1]:
                root.remove(element) 
    elif 'types_of_sports.xml' == file_name:
        for element in root:
            if element.attrib['name'] == value[0]:
                root.remove(element)    
    tree.write(file_name, encoding="utf-8")