


import json





# turns out the real way is to connect to the SQL database, not try to load up a second copy in python!

# https://www.geeksforgeeks.org/how-to-connect-python-with-sql-database/#

# # Importing module 
# import mysql.connector
 
# # Creating connection object
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "yourusername",
#     password = "your_password"
# )
 
# # Printing the connection object 
# print(mydb)



# but... right now I don't have database access





# funky way that seems to have a lot of issues

# import sqlite3

# connection_object = sqlite3.connect("database_name.db")

# cursor_object = connection_object.cursor()

# cursor_object.executescript(“script”)




# sqlparse docs didn't really make sense

# import sqlparse
# import collections
# import pandas as pd

# def load_sql_file(filename):

#     # cp850 is the language codec for Western Europe
#     # https://docs.python.org/2.4/lib/standard-encodings.html

#     with open(filename, "r", encoding="cp850") as sqldump:

#         statements = sqlparse.parsestream(sqldump)
#         headers = {}
#         contents = collections.defaultdict(list)

#         for statement in statements:

#             if statement.get_type() == "INSERT":

#                 sublists = statement.get_sublists()
#                 table_info = next(sublists)
#                 table_name = table_info.get_name()

#                 print(table_info)
#                 print(type(table_info))
#                 print(table_info.tokens)

#                 headers[table_name] = [
#                     col.get_name()
#                     for col in table_info.get_parameters()
#                 ]

#                 contents[table_name].extend(
#                     tuple(
#                         s.value.strip("\"'")
#                         for s in next(rec.get_sublists()).get_identifiers()
#                     )
#                     for rec in next(sublists).get_sublists()
#                 )

#     data = {
#         name: pd.DataFrame.from_records(table, columns = headers[name])
#         for name, table in contents.items()
#     }

#     return data




import re

def sql_dump_to_dict(file_path):

    # cp850 is the language codec for Western Europe
    # https://docs.python.org/2.4/lib/standard-encodings.html

    with open(file_path, "r", encoding="cp850") as file:
        sql_content = file.readlines()

    data_pattern = re.compile(r"INSERT INTO `(\w+)` \((.+?)\) VALUES (.+?);", re.DOTALL)
    data = []

    for line in sql_content:
        print(line)
        input()
        match = data_pattern.search(line)
        if match:
            table_name = match.group(1)
            columns = match.group(2).split(', ')
            values = match.group(3).strip("()").split("), (")
            data.append({
                'table': table_name,
                'columns': columns,
                'values': [tuple(map(lambda x: x.strip("'"), value.split(','))) for value in values]
            })

    db_dict = {}
    for entry in data:
        table = entry['table']
        db_dict[table] = []
        for row in entry['values']:
            row_dict = dict(zip(entry['columns'], row))
            db_dict[table].append(row_dict)

    return db_dict

# # Example usage
# db_dict = sql_dump_to_dict('dump.sql')
# print(db_dict)

def load_sql_file(filename):
    return sql_dump_to_dict(filename)





with open("dump.json", "w") as f:
    print(json.dumps(load_sql_file("OneDrive_1_7-24-2024/wp_rocksolidtruth_com.sql"), indent=2), file=f)




