# Building a GUI to get in put for the reqeust_aips_list script. Will allow for more flexibility with what is
# requested than using script arguments.

import PySimpleGUI as sg

# There are many color schemes to pick from.
sg.theme('BlueMono')

# Text, buttons, and boxes for the window.
# Each list is its own row.
layout = [[sg.Text('Path to ARCHive format report'), sg.Input(key='REPORT'), sg.FileBrowse()],
          [sg.Text('Your group'), sg.Combo(['bmac', 'dlg', 'dlg-harg', 'dlg-magil', 'hargrett', 'russell'], key='GROUP')],
          [sg.Text('-'*300)],
          [sg.Text('Format Name'), sg.Input(key='NAME1'), sg.Text('Version'), sg.Input(key='V1'), sg.Text('Identifier'), sg.Input(key='ID1')],
          [sg.Text('Format Name'), sg.Input(key='NAME2'), sg.Text('Version'), sg.Input(key='V2'), sg.Text('Identifier'), sg.Input(key='ID2')],
          [sg.Text('Format Name'), sg.Input(key='NAME3'), sg.Text('Version'), sg.Input(key='V3'), sg.Text('Identifier'), sg.Input(key='ID3')],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Make a batch AIP request list', layout)

event, values = window.read()

window.close()

print('Results:', values)
print('First format:', values['NAME1'])
print('Second version:', values['V2'])
print('Third id:', values['ID3'])