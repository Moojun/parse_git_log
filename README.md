# GitHub 프로젝트에서 commit message 내용 추출

### git_logs directory

alluxio, ballerina-lang, crate, elasticsearch, hazelcast, neo4j, react-native,
sakai, vespa, wildfly 총 10개의 git log 파일이 저장되어 있음

각 프로젝트 별로 git log 파일 추출 방법은 다음과 같다.

1. 프로젝트 clone
2. `git log > [project_name].git.log` 커맨드를 사용하여 .git.log 형식으로 저장한다.



### parse_log.py

각 프로젝트 별로, log 파일 형식은 아래와 같다. 

```
commit 73b4d67c8b39a6358897ec349370e7037a6fea7f
Author: maobaolong <307499405@qq.com>
Date:   Fri Mar 17 13:16:28 2023 +0800

    Add metric for cached block location
    
    Finish the todo task after https://github.com/Alluxio/alluxio/pull/16953
    
    pr-link: Alluxio/alluxio#17056
    change-id: cid-e6ddc03b08e7a8a18cd53d77fa9a2f0edf4e1f57
```



위 파일들을 읽어와서 추출된 결과물의 예시는`Target-project-commits.csv` 에 저장되며, 아래 표는 해당 파일의 예시이다. 

old_commit과 new_commit의 차이는 1개의 커밋 내역이 존재하고, new_commit이 새로운 변경 내용을 추가한 커밋이니 new_commit의 해시값을 기준으로 git log를 확인.

merged_commit_status의 값이 'T'인 경우는 해당 로그 메시지가 `Merge branch` 혹은 `Merge pull request` 를 포함하는 경우이다.

|      project      |                old_commit                |                new_commit                | merged_commit_status |
| :---------------: | :--------------------------------------: | :--------------------------------------: | -------------------- |
| **elasticsearch** | cbc73a7665ff3f262cbcd40c623bab2f69b7c2a9 | 12ab625c6f1d590b12794bc6246e53cbb9f19154 | F                    |
| **elasticsearch** | b068ab2ee2876d37caf7a7d24d26cffea7003720 | cbc73a7665ff3f262cbcd40c623bab2f69b7c2a9 | F                    |
| **elasticsearch** | 6da721eddab2d9f7c1b51ff5aba7da25634ab5ac | b068ab2ee2876d37caf7a7d24d26cffea7003720 | F                    |



### execute_db

parse_log.py의 결과로 저장되는 Target-project-commits.csv 파일을 읽어서, 기존의 commits table의 값을 Update 하는 코드.