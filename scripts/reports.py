# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 16:06:09 2020

@author: hansona
"""

"""
Calculate various subtotal reports of the collection, aip, and file counts for format types, format standard names, and groups. The reports are saved as csv files.
"""

import pandas as pd

#formats is the data to analyze
#results is the folder to save reports to
formats = 'H:/ARCHive-formats/archive_formats_2020-03.csv'
results = 'H:/ARCHive-formats/2020-02-25-reports'

#Read the data from the csv.
df = pd.read_csv(formats)

#Format type.
type_totals = df.groupby('Format_Type').sum()
type_totals.to_csv(f'{results}/type_totals.csv')

#Format standard name.
name_totals = df.groupby('Format_Standard_Name').sum()
name_totals.to_csv(f'{results}/name_totals.csv')

#Group.
group_totals = df.groupby('Group').sum()
group_totals.to_csv(f'{results}/group_totals.csv')

# Format type subdivided by group.
type_group = df.groupby(['Format_Type', 'Group']).sum()
type_group.to_csv(f'{results}/type_group.csv')

# Format type subdivided by format standardized name.
type_name = df.groupby(['Format_Type', 'Format_Standard_Name']).sum()
type_name.to_csv(f'{results}/type_name.csv')

# Format standardized name subdivided by group.
name_group = df.groupby(['Format_Standard_Name', 'Group']).sum()
name_group.to_csv(f'{results}/name_group.csv')

