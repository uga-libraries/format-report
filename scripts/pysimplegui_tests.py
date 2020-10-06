import PySimpleGUI as sg

# Pattern 2B

layout = [[sg.Input(key='-IN-')],
          [sg.Text('Formats requested so far:'), sg.Text(size=(12,1), key='-OUTPUT-')],
          [sg.Button('Add Another'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

format_info = [] #I added this to save all the input received, not just the last one

while True:  # Event Loop
    event, values = window.read()       # can also be written as event, values = window()
    print(event, values)
    format_info.append(values) #I added this
    if event is None or event == 'Exit':
        break
    if event == 'Add Another':
        # change the "output" element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])
        # above line can also be written without the update specified
        window['-OUTPUT-'](values['-IN-'])

window.close()

#I added this: has every value input into the field PLUS the last one twice.
print('Total input: ', format_info)
