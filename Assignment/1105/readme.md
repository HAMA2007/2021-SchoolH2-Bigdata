# Assignment4(1105) - Hadoop cluster 연습
목표 - 3개의 node를 이용하여 cluster로 만든 뒤, wordcount돌려보기
환경 - ubuntu 16.04 LTS 3nodes

## 1. host내용 수정
```bash
sudo vim /etc/hosts
```
파일에 내용 추가(당연히 ip는 조정 필요)
<br>127.0.1.1관련된 것들이 있을 수 있는데, 삭제하면 좋음(간혹 문제 생김)
```vim
192.168.0.19    master
192.168.0.8     slave1
192.168.0.24    slave2
```

## 2. hostname내용 수정
```bash
sudo vim /etc/hostname
```
master의 경우 master이라고 적고, slave1, slave2는 각각 slave1, slave2라고 작성
```vim
master
```

장비 리부트
```bash
sudo shutdown -r now
```


## 3. ssh key 생성후 복사하기
```bash
# 키를 만든다
ssh-keygen -t rsa - P ""
# 키를 master와, slave1, slave2에 복사한다
# master노드에서 만든 것은 master, slave1, slave2에 모두 복사
# slave노드에서 만든 것은 자신slave, master 2군데만 복사
ssh-copy-id -i ~/.ssh/id_rsa.pub master
ssh-copy-id -i ~/.ssh/id_rsa.pub slave1
ssh-copy-id -i ~/.ssh/id_rsa.pub slave2
```

## 4. hadoop환경설정
vim을 써도 좋지만, vscode의 ssh로 연결해서 하면 훨씬 편하다
```bash
# codes폴더에 적힌대로 수정

# 1. hadoop-env.sh수정
# java_home 얻기
echo $JAVA_HOME
# hadoop home은 하둡 복사해제한 폴더
# 여기서는 /home/hadoop(유저명)/hadoop(이 폴더에 압축을 해제함)
# 알기 쉽게 하면 /home/hama2007/hadoop/bin,sbin폴더 있음
HADOOP_HOME="/home/hadoop/hadoop"

# 2. core-site.xml
# 메인폴더에 hdfs라는 폴더를 만들어서 그곳에 hdfs를 셋팅하게됨(자동-폴더 만들필요X)
<name>hadoop.tmp.dir</name>
<value>/home/hadoop/hdfs</value>

# 3. hdfs-site.xml
# core-site.xml과 마찬가지
<name>dfs.namenode.name.dir</name>
<value>/home/hadoop/hdfs/namenode</value>

# 4. master, slaves
master과 slave이름들을 적어줌
```

## 5. hdfs 포맷
```bash
# ~/hadoop경로로 이동 후
bin/hadoop namenode -format
```

## 6. hadoop cluster 시작
```bash
# ~/hadoop/sbin경로로 이동 후
bash start-all.sh
```

## 7. jps로 확인
```bash
ssh master jps; ssh slave1 jps; ssh slave2 jps;
```
순서대로 master에 4개, slave1에 3개, slave2에 3개 떠 있으면 성공
```bash
1347 ResourceManager
8294 Jps
5403 NameNode
5597 SecondaryNameNode

4661 DataNode
4120 NodeManager
5499 Jps

5687 DataNode
4521 NodeManager
6425 Jps
```

## 7-1. 문제해결
만약 Namenode가 안보일 경우
```bash
# ~/hadoop/sbin경로로 이동 후
bash stop-dfs.sh

# 4-2, 4-3에서 지정했던 hdfs폴더 제거(master, slave 전부 제거)
rm -r -f /home/hadoop/hdfs

# ~/hadoop/sbin경로로 이동 후 재실행
bash start-dfs.sh
```

## 8. hdfs에 파일 복사
```bash
# 하둡이 설치된 폴더 안(여기서는 ~/hadoop)에서 
# /user/hadoop/LICENSE.txt와 같이 파일 넣고
# hdfs의 /경로에 복사 수행
bin/hadoop fs -put ./user /
```

## 9. wordcount 예제 수행
```bash
# 하둡이 설치된 폴더 안(여기서는 ~/hadoop)에서 LICENSE.txt 분석 수행
bin/hadoop jar ./share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.6.jar wordcount ./LICENSE.txt output
```
실행 로그
```bash
21/11/05 14:43:13 INFO client.RMProxy: Connecting to ResourceManager at master/192.168.0.19:8032
21/11/05 14:43:15 INFO input.FileInputFormat: Total input paths to process : 1
21/11/05 14:43:15 INFO mapreduce.JobSubmitter: number of splits:1
21/11/05 14:43:15 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1636090032343_0001
21/11/05 14:43:16 INFO impl.YarnClientImpl: Submitted application application_1636090032343_0001
21/11/05 14:43:16 INFO mapreduce.Job: The url to track the job: http://master:8088/proxy/application_1636090032343_0001/
21/11/05 14:43:16 INFO mapreduce.Job: Running job: job_1636090032343_0001
21/11/05 14:43:27 INFO mapreduce.Job: Job job_1636090032343_0001 running in uber mode : false
21/11/05 14:43:27 INFO mapreduce.Job:  map 0% reduce 0%
21/11/05 14:43:35 INFO mapreduce.Job:  map 100% reduce 0%
21/11/05 14:43:42 INFO mapreduce.Job:  map 100% reduce 100%
21/11/05 14:43:42 INFO mapreduce.Job: Job job_1636090032343_0001 completed successfully
21/11/05 14:43:42 INFO mapreduce.Job: Counters: 49
	File System Counters
		FILE: Number of bytes read=29637
		FILE: Number of bytes written=305039
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=86531
		HDFS: Number of bytes written=22239
		HDFS: Number of read operations=6
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
	Job Counters
		Launched map tasks=1
		Launched reduce tasks=1
		Data-local map tasks=1
이하생략
```

## 10. 결과물 파일 빼오기
```bash
bin/hadoop fs -get /user/hadoop/output ./
```

## 11(번외). ssh tunneling으로 web UI접속해보기
```bash
# 1. local pc(맥북 등)에서 아래 명령어 수행(master:8088을 localhost:12345에 포워딩), ssh접속정보는(hadoop@125.6.37.80)
# 2. 명령어가 켜져 있는 상황에서 크롬브라우저 이용해 localhost:12345, localhost:12346접속

# cluster에서 수행되는 Application정보 볼 수 있음
ssh  -L 12345:master:8088 hadoop@125.6.37.80
# hdfs summary 등을 볼 수 있음
ssh  -L 12346:master:8088 hadoop@125.6.37.80
```




