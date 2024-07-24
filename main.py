


import csv
import json
import os





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

    # data_pattern = re.compile(r"INSERT INTO `(\w+)` \((.+?)\) VALUES (.+?);", re.DOTALL)
    # data_pattern = re.compile(r"INSERT INTO `(\w+)` VALUES (.+?);", re.DOTALL)
    data = []

    for line in sql_content:
        # match = data_pattern.search(line)
        # if match:

        # print(line)
        if line.startswith("INSERT INTO "):
            # print(line.find("`"))
            name_start = 13
            assert line[name_start-1] == "`"
            name_end = line.find("`", name_start)
            values_start = name_end+9
            assert line[name_end:values_start] == "` VALUES "
            values_end = len(line)-2
            assert line[values_end:] == ";\n"

            name = line[name_start:name_end]
            values = line[values_start:values_end]

            # print(name_end)
            print(name)
            # print(line.find("(", name_end))
            # assert 
            # input()

            # table_name = match.group(1)
            # columns = match.group(2).split(', ')
            # values = match.group(3).strip("()").split("), (")
            # values = match.group(2).strip("()").split("), (")
            # values = match.group(2)
            data.append({
                # 'table': table_name,
                'table': name,
                # 'columns': columns,
                # 'values': [tuple(map(lambda x: x.strip("'"), value.split(','))) for value in values]
                'values': values
            })

    db_dict = {}
    for entry in data:
        table = entry['table']
        db_dict[table] = []
        # for row in entry['values']:
        #     row_dict = dict(zip(entry['columns'], row))
        #     db_dict[table].append(row_dict)
        # db_dict[table].extend(entry["values"])
        db_dict[table] = entry["values"]

    return db_dict

# # Example usage
# db_dict = sql_dump_to_dict('dump.sql')
# print(db_dict)

def load_sql_file(filename):
    return sql_dump_to_dict(filename)





# with open("dump.json", "w") as f:
#     database = load_sql_file("OneDrive_1_7-24-2024/wp_rocksolidtruth_com.sql")
#     print(json.dumps(database, indent=2), file=f)

# active_plugins = None
# # for row in database["aajjez_options"]:
# #     print(json.dumps(row, indent=2))
# #     if row[1] == "active_plugins":
# #         active_plugins = row[2]


# print(database["aajjez_options"].find("active_plugins"))
# input()

# x = database["aajjez_options"]
# # print(json.dumps(x, indent=2))
# # input()

# x = x.strip("()")
# # print(json.dumps(x, indent=2))
# # input()

# x = x.split("), (")
# print(json.dumps(x, indent=2))
# input()

# print(json.dumps(active_plugins, indent=2))



def get_active_plugins(filename):
    with open(filename, "r", encoding="cp850") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if not line.startswith("INSERT"):
            continue

        j = line.find("_options")
        if j == -1:
            continue

        j = line.find("active_plugins")
        if j == -1:
            continue

        start = j
        assert line[j-5:j] == "(33,'"
        start -= 5

        j = line.find("category_base")
        if j == -1:
            continue

        end = j
        assert line[j-6:j] == ",(34,'"
        end -= 6



        # print(line[start:end])
        # print(f"{i+1},{j-1}")
        # print(json.dumps(line[start:end].split("\\\""), indent=2))


        blocks = line[start:end].split("\\\"")

        out = []
        for i in range(1, len(blocks), 2):
            out.append(blocks[i])
    
        return out
    



if __name__ == "__main__":
    active_plugins_by_dump = {}
    for file in os.listdir("dumps/"):
        plugins = get_active_plugins("dumps/" + file)
        active_plugins_by_dump[file] = set(plugins)
        # print(plugins)

    # print(json.dumps(active_plugins_by_dump, indent=2))

    all_plugins = set()
    for plugins in active_plugins_by_dump.values():
        for plugin in plugins:
            all_plugins.add(plugin)
    all_plugins = sorted(list(all_plugins))

    # print(json.dumps(all_plugins, indent=2))

    export_table = [["sql dump", *all_plugins]]
    for dump in sorted(active_plugins_by_dump.keys()):
        export_table.append([dump])
        for plugin in all_plugins:
            if plugin in active_plugins_by_dump[dump]:
                export_table[-1].append("present")
            else:
                export_table[-1].append("missing")

    with open("plugin_report.csv", "w") as f:
        csv.writer(f, lineterminator="\n").writerows(export_table)
