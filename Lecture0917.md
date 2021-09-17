# Lecture2 (0917)
## Git and Github 
---
### 사용 목적
```
1. 내가 코딩하고 있는 부분에 대해, 다른 사람이 동시에 코딩하고 있을 경우
2. 현재 상태를 저장(Snapshot)하기 위한 목적
3. 알아차리지 못한 상태에서 중요한 코드를 망가뜨리는 것 방지
4. 다른 팀원이 어떠한 변화를 주었는지 확인하는 목적
```

### Git
오픈소스 버전 컨트롤 시스템
### Github
웹 기반 Git Repository 호스팅 서비스

---
### Usecase
```bash
# Repository Clone
git clone http://khuhub.khu.ac.kr/2021-2-big-data-programming/assignment.git

# Initialize Current Folder
# 이 폴더를 추적함을 알린다
git init

# vim을 이용해서 Readme.md 파일 하나를 생성한다
# 저장하고 나올 때는 !wq를 사용하면 된다
vim Readme.md

# Readme.md파일을 추적에 추가한다
git add Readme.md

# 현 상태를 저장한다(Commit)
git commit -m "[Init] Readme added"

# log를 확인 가능하다
git log

# 현재 위치를 외부에 있는 서비스에 연동한다
git remote add origin https://github.com/HAMA2007/2021-SchoolH2-Bigdata.git

# github와 같은 곳에 실제로 업/다운로드한다
git push
git pull

# branch를 만든다
git branch develop

# branch 이동
git checkout develop
git checkout main

# merge (현재 branch를 합병한다)
git merge

# 여러개의 커밋 내용을 수정하여 하나의 커밋으로 합칠 때 사용
Git rebase -I HEAD~4
```
