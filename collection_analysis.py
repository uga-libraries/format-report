# Subtotal for collections counts the same collection many times.
# What do the numbers look like for format types if calculated by collection?

"""
Duplication makes a big difference. Counts below are before and after deduplication with 10/26 data:

video [476, 160]
image [1174, 538]
audio [154, 69]
application [266, 53]
structured_text [131, 26]
text [557, 63]
spreadsheet [124, 27]
archive [65, 27]
presentation [48, 24]
executable [155, 21]
web_archive [18, 17]
database [65, 14]
message [50, 14]
design [70, 17]
model [2, 2]
multipart [2, 2]
geographic_data [7, 1]

"""

import csv

formats_report = "C:/users/amhan/Documents/GitHub/format-report/testing/2020-10-26_prod/archive_formats_2020-10.csv"

type_coll_id = {}
type_coll_count = {}

# Gets the data from the merged ARCHive formats report.
with open(formats_report, 'r') as formats:
    formats_read = csv.reader(formats)

    # Skips the header row.
    next(formats_read)

    # Gets the data from each row in the report, which has information about a single format for that group.
    # row[0] is group.
    # row[4] is format type.
    # row[11] is collection ids (a comma separated string).
    for row in formats_read:

        # Format the collections as a list.
        collection_list = row[11].split(', ')

        # For Russell, remove the dash from collection identifiers, since there can be two id formats for the same
        # collection, rbrl-### and rbrl###. If both variations are present, just want to count it once.
        if row[0] == 'russell':
            collection_list = [collection.replace('-', '') for collection in collection_list]

        # Change to a set, which removes duplicates from Russell reformatting.
        collection_list = list(set(collection_list))

        # Adds each collection to a dictionary with format type as the key and a list of collection ids as the value.
        for collection in collection_list:
            try:
                type_coll_id[row[4]].append(collection)
            except KeyError:
                type_coll_id[row[4]] = [collection]

    # Add pre-deduplication count to count dictionary.
    for key, value in type_coll_id.items():
        type_coll_count[key] = [len(value)]

    # Changes each list in the dictionary to a set to remove duplicates.
    for key, value in type_coll_id.items():
        type_coll_id[key] = set(value)

    # Add the post-deduplication count to count dictionary
    for key, value in type_coll_id.items():
        type_coll_count[key].append(len(value))

    # Prints the results:
    for key, value in type_coll_count.items():
        print(key, value)
