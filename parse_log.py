import csv

'''
class Commits:
    def __init__(self, project_name, old_commit, new_commit, merged_commit):
        self.project_name = project_name
        self.old_commit = old_commit
        self.new_commit = new_commit
        self.merged_commit = merged_commit

    def __str__(self):
        return '%s,%s,%s,%s' % (self.project_name, self.old_commit, self.new_commit, self.merged_commit)
'''


def create_project_csv():
    file_name = "commits_info/Target-project-commits.csv"
    with open(file_name, 'w', newline='') as csv_file:
        write_csv = csv.writer(csv_file, delimiter=',')
        write_csv.writerow(['project', 'old_commit', 'new_commit', 'merged_commit_status', 'commit_message'])
    return file_name


projects = ['elasticsearch', 'ballerina-lang', 'crate', 'alluxio', 'hazelcast',
            'neo4j', 'react-native', 'sakai', 'vespa', 'wildfly']
# projects = ['crate']
ofile_name = create_project_csv()
for project in projects:
    ifile_name = "git_logs/" + project + ".git.log"
    ifile = open(ifile_name, "r")

    new_commit_id = ""
    old_commit_id = ""
    merged_commit_status = ""
    commit_message = ""
    commit_flag = False
    message_flag = True

    while True:
        line = ifile.readline()
        if not line:
            break
        if line.startswith("commit "):
            line = line.strip("commit").lstrip().strip('\n')
            if not commit_flag:  # 첫 번째 line의 경우, new_commit_id 를 따로 설정해 줘야함
                new_commit_id = line

            old_commit_id = line
            if commit_flag:  # old_commit 과 new_commit 이 같은 경우(첫 번째 line의 경우)는 pass
                with open(ofile_name, 'a', newline='') as csvfile:
                    write_to_csv = csv.writer(csvfile, delimiter=',')
                    write_to_csv.writerow([project, old_commit_id, new_commit_id, merged_commit_status, commit_message])
            commit_flag = True
            message_flag = True

        elif line.startswith("Author"):
            continue
        elif line.startswith("Date"):
            continue
        elif line.startswith("    "):   # commit message 의 경우 여러 줄로 구성되어 있기 때문에, 이 코드를 그대로 사용하면 맨 마지막 커밋 메시지가 등록된다.
            if message_flag:
                line = line.lstrip().strip('\n')
                if line.startswith("Merge branch") or line.startswith("Merge pull request"):
                    commit_message = line
                    merged_commit_status = 'T'
                else:
                    commit_message = line
                    merged_commit_status = 'F'
                message_flag = False    # False 로 설정함으로 인해, 이후 커밋 메시지들을 무시한다.
            else:
                continue

            new_commit_id = old_commit_id  # 여기서 new_commit 값을 old_commit 값으로 넣은 뒤, 위에서 old_commit 새로 설정

    ifile.close()
