"""
Purpose: Make a list of aips to request from ARCHive for format migration.
"""

import csv
import re
import sys

import PySimpleGUI as sg

# PART ONE: GET LIST CRITERIA FROM USER WITH A GUI

# Color scheme for the GUI.
sg.theme('BlueMono')

# Components of the GUI (label text, input boxes, and buttons).
layout = [[sg.Text('Your group'), sg.Combo(['bmac', 'dlg', 'dlg-harg', 'dlg-magil', 'hargrett', 'russell'], key='GROUP')],
          [sg.Text('Path to ARCHive format report'), sg.Input(key='REPORT'), sg.FileBrowse()],
          [sg.Text('-'*300)],
          [sg.Text('Format Name'), sg.Input(key='NAME1'), sg.Text('Version'), sg.Input(key='V1'), sg.Text('Identifier'), sg.Input(key='ID1')],
          [sg.Text('Format Name'), sg.Input(key='NAME2'), sg.Text('Version'), sg.Input(key='V2'), sg.Text('Identifier'), sg.Input(key='ID2')],
          [sg.Text('Format Name'), sg.Input(key='NAME3'), sg.Text('Version'), sg.Input(key='V3'), sg.Text('Identifier'), sg.Input(key='ID3')],
          [sg.Submit(), sg.Cancel()]]

# Make the GUI appear on the screen and gets the user input for use by the script.
window = sg.Window('Make a batch AIP request list', layout)
event, values = window.read()
window.close()

# Get the filepath to the format report from the user input.
format_report = values['REPORT']

# Get the ARCHive group from the user input.
archive_group = values['GROUP']

# Get the format criteria from the user input. Can be up to three combinations of format name, version, and id.
filters = [(values['NAME1'], values['V1'], values['ID1']), (values['NAME2'], values['V2'], values['ID2']), (values['NAME3'], values['V3'], values['ID3'])]


# PART TWO: GENERATE AIP REQUEST LIST BASED ON USER CRITERIA

# Increase size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize/10)

# List for results, since could get aips from more than one row.
aip_list = []

# Read the format report (ARCHive export), a tab-delimited text file.
with open(format_report) as report:
    read_report = csv.reader(report, delimiter='\t')

    # Find rows with the relevant format values.
    for row in read_report:

        # Tests information from each of the three format rows in the GUI.
        for format_info in filters:

            # If the user entered information in at least one of the three cells, matches against the format report
            # csv, extracts the data from the aip id cell, converts it to a list with split, and adds them to end of
            # aip_list. 0 is the format name, 1 is the version, and 2 is the identifier(s).

            # Matches are case insensitive and when a format has multiple ids it matches if any of the ids are the
            # filter. Does assume the ids do not contain spaces and are separated by spaces. Otherwise,
            # the match must be exact, for instance 7.0 is not the same 7 or seven.
            if format_info[0] or format_info[1] or format_info[2]:

                # Only has a name.
                if format_info[0] and not (format_info[1] or format_info[2]):
                    if row[2].lower() == format_info[0].lower():
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

                # Has a name and version.
                elif format_info[0] and format_info[1] and not (format_info[2]):
                    if row[2].lower() == format_info[0].lower() and row[3].lower() == format_info[1].lower():
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

                # Has a name and id.
                elif format_info[0] and not (format_info[1]) and (format_info[2]):
                    if row[2].lower() == format_info[0].lower() and format_info[2].lower() in row[5].lower().split(' '):
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

                # Has a name, version, and id.
                elif format_info[0] and format_info[1] and format_info[2]:
                    if row[2].lower() == format_info[0].lower() and row[3].lower() == format_info[1].lower() and format_info[2].lower() in row[5].lower().split(' '):
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

                # Only has a version.
                elif format_info[1] and not (format_info[2]):
                    if row[3].lower() == format_info[1].lower():
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

                # Has a version and id.
                elif format_info[1] and format_info[2]:
                    if row[3].lower() == format_info[1].lower() and format_info[2].lower() in row[5].lower().split(' '):
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

                # Only has an id.
                else:
                    if format_info[2].lower() in row[5].lower().split(' '):
                        aips = row[7]
                        aip_list.extend(aips.split('|'))

# Final sorted list of aip ids, with duplicates removed using set().
aip_list = list(set(aip_list))
aip_list.sort()

# Save to a new file in the format needed for an ARCHive batch copy request.
with open(f'aip_request.csv', 'w', newline='') as result:
    write_result = csv.writer(result)
    for aip in aip_list:
        write_result.writerow([f'http://archive.libs.uga.edu/{archive_group}/{aip}',1,'Performing preservation migration.'])