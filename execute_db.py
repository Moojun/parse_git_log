import pymysql

# Execute sql to revise db in server.
db = pymysql.connect(host='', port=3306, user='', password='',
                     db='', charset='utf8')

project = ""
old_commit = ""
new_commit = ""
merged_commit_status = ""
count = 0

f = open("commits_info/Target-project-commits.csv", 'r')
lines = f.readlines()

cursor = db.cursor()

# Case 1. Use executemany()
data_list = []
for line in lines:
    line_split = line.strip('\n').split(',')
    project = line_split[0]
    old_commit = line_split[1]
    new_commit = line_split[2]
    merged_commit_status = line_split[3]

    data = [merged_commit_status, project, old_commit, new_commit]
    data_list.append(data)
    print("count: ", count)  # test

    count += 1

    if count % 10000 == 0:
        query = """UPDATE commits SET merged_commit_status = %s 
                   WHERE project_name = %s and old_commit = %s and new_commit = %s """
        cursor.executemany(query, data_list)
        db.commit()
        data_list = []

# 나머지 데이터 Update
query = """UPDATE commits SET merged_commit_status = %s
                   WHERE project_name = %s and old_commit = %s and new_commit = %s """
cursor.executemany(query, data_list)
db.commit()

# Case 2. use execute()
# for line in lines:
#     line_split = line.strip('\n').split(',')
#     project = "'" + line_split[0] + "'"
#     old_commit = "'" + line_split[1] + "'"
#     new_commit = "'" + line_split[2] + "'"
#     merged_commit_status = "'" + line_split[3] + "'"
#
#     print("count: ", count)  # test
#     count += 1
#
#     query = """UPDATE commits SET merged_commit_status = {}
#                    WHERE project_name = {} and old_commit = {} and new_commit = {}
#         """.format(merged_commit_status, project, old_commit, new_commit)
#     cursor.execute(query)
#     db.commit()

db.close()
