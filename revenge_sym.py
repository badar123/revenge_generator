import PySimpleGUI as sg
import xml.etree.ElementTree as ET

SUBMIT_TEXT = 'Ezt csinálom!'
ENTER_KEY_PRESSED = 'Return:36'
CLOSE_BUTTON_PRESSED = 'Close'

tree = ET.parse('story_template.xml')
root = tree.getroot()
title = root.attrib['title']
player = root[0]
scene = root[1]
situation = [s for s in scene.findall('situation')
             if s.attrib['name'] == scene.attrib['current_situation']][0]
options = [f for f in situation[1]]

### GUI ###
sg.theme('DarkAmber')
img = sg.Image(scene.attrib['img'], size=(500, 500))
img_txt = sg.Multiline(situation[0].text, size=(30, 35), disabled=True, do_not_clear=False)
listbox = sg.Listbox(values=[o.text for o in options], size=(70, 5))
button = sg.Submit(SUBMIT_TEXT)
window = sg.Window(title, [[img, img_txt], [listbox, button]], resizable=False, return_keyboard_events=True)

### MAIN LOOP ###
while True:
    event, values = window.read()
    if event in (None, CLOSE_BUTTON_PRESSED):
        break
    if event in (SUBMIT_TEXT, ENTER_KEY_PRESSED):
        selected = listbox.get()
        if len(selected) == 0:
            continue
        if selected[0] == 'ok':
            listbox.update([o.text for o in options])
            img_txt.update(situation[0].text)
            continue

        selected_option = [o for o in options if o.text == selected[0]][0]
        if 'result' in selected_option.attrib:
            img_txt.update(selected_option.attrib['result'])
            listbox.update(['ok'])

        if 'to_situation' in selected_option.attrib:
            situation = [s for s in scene.findall('situation')
                         if s.attrib['name'] == selected_option.attrib['to_situation']][0]
            scene.attrib['current_situation'] = situation.text
            options = [f for f in situation[1]]

            if 'item_gained' in situation.attrib:
                new_item = ET.Element('item')
                new_item.text = situation.attrib['item_gained']
                ET.SubElement(player[1], new_item)

            if 'img' in situation.attrib:
                scene.attrib['img'] = situation.attrib['img']
                img.update(scene.attrib['img'])

            img_txt.update(situation[0].text)
            listbox.update([o.text for o in options])

window.close()
