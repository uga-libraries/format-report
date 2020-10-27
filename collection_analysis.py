# Calculate the number of unique collections and AIPs per format type and format standardized name. Because of how
# the data is normalized, the same collection or AIP is counted multiple times if the counts in the archive formats
# csv are used, resulting in very inflated numbers. Numbers can be 2x-10x bigger.

import csv

formats_report = "C:/users/amhan/Documents/GitHub/format-report/testing/2020-10-26_prod/archive_formats_2020-10.csv"

type_count = {}
name_count = {}

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

        # Adds each collection to a dictionary with format type as the key and a list of collection ids as the value.
        # Adds each collection to a dictionary with format name as the key and a list of collection ids as the value.
        for collection in collection_list:
            try:
                type_count[row[4]].append(collection)
                name_count[row[5]].append(collection)
            except KeyError:
                type_count[row[4]] = [collection]
                name_count[row[5]] = [collection]

    # Convert the list of collections in each dictionary to the count of unique collections.
    # Making a set removes duplicates.
    for key, value in type_count.items():
        type_count[key] = len(set(value))

    for key, value in name_count.items():
        name_count[key] = len(set(value))

    # Prints the results.
    print("\nAll Format Types")
    for key, value in type_count.items():
        print(key, value)

    print("\nStandardized Format Names if over 40 collections")
    for key, value in name_count.items():
        if value > 40:
            print(key, value)
