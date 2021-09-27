# Lecture3 (0924) - hadoop and MapReduce 

## 설치 방법 (mac 10.15.7 + fish shell)

## 1. 설치
```bash
brew install openjdk -> 만약 안될경우 홈페이지에서 수동 설치
brew install hadoop
```

## 2. 환경변수 수정
```bash
cd /usr/local/cellar/hadoop/3.3.1/libexec/etc/hadoop
```

### 2-1. hadoop-env.sh에 추가
-> 아래 명령어 입력해서 JAVA_HOME 값 알기
```bash
/usr/libexec/java_home
```
-> JAVA_HOME변경할 것
```sh
export HADOOP_OPTS="-Djava.net.preferIPv4Stack=true -Djava.security.krb5.realm= -Djava.security.krb5.kdc="
export JAVA_HOME="/Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home"
```

### 2-2. core-site.xml에 추가
```xml
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/usr/local/Cellar/hadoop/hdfs/tmp</value>
        <description>A base for other temporary directories.</description>
    </property>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

### 2-3. hdfs-site.xml에 추가
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <!-- 이 아래는 선택적으로 추가 -->
    <property>
        <name>dfs.namenode.http-address.[NameServiceID].[NameNodeID]</name>
        <value>localhost:50070</value>
    </property>
    <property>
        <name>dfs.datanode.http.address</name>
        <value>localhost:50075</value>
    </property>
</configuration>
```

### 2-4. mapred-site.xml에 추가
```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>   
        <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>

    <!-- 이 아래는 선택적으로 추가 -->
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>localhost:19888</value>
    </property>
</configuration>
```

### 2-5. yarn-site.xml에 추가
```xml
<configuration>
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
	<property>
		<name>yarn.nodemanager.env-whitelist</name>
		<value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
	</property>

    <!-- 이 아래는 선택적으로 추가 -->
    <property>
        <name>yarn.nodemanager.webapp.address</name>
        <value>localhost:8042</value>
    </property>
    <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>localhost:8088</value>
    </property>
</configuration>
```

## 3. 실행
### 3-1. ssh 설정
```bash
ssh localhost
```
-> Connection refused가 나올 경우
```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

### 3-2. hdfs 포맷
```bash
cd /usr/local/cellar/hadoop/3.3.1/libexec/bin
hdfs namenode -format
```

### 3-3. hadoop 실행
```bash
cd /usr/local/cellar/hadoop/3.3.1/libexec/sbin
./start-all.sh
```
-> 만약 "localhost: ssh: connect to host localhost port 22: Connection refused"오류 나오면
```
맥 환경설정 - 공유 - 원격 로그인 설정(Administrator만)
```

### 3-4. 실행 확인
```bash
jps
```
-> 결과값(숫자는 다를 수 있음)
```
77200 NodeManager
76775 DataNode
77101 ResourceManager
77324 Jps
76671 NameNode
76911 SecondaryNameNode
```

### 3-5. WebUI 확인
```
Cluster status : http://localhost:8088
HDFS status : http://localhost:9870
Secondary NameNode status : http://localhost:9868
DataNode status : http://localhost:50075
Node Manager : http://localhost:8042
```

## 4. hadoop 종료
```bash
cd /usr/local/cellar/hadoop/3.3.1/libexec/sbin
./stop-all.sh
```
<br><br><br>

# MapReduce 테스트해보기
## 1. input.txt파일 생성
```txt
a b c d e a b c d e a b b c c c d d d d e e e e e
```

## 2. hdfs에 경로 생성 및 파일 복사
```
1. user/hama2007/input.txt 형태로 폴더안에 파일 집어넣기
2. hadoop fs -put ./user  /
```

## 3. MapReduce실행
```bash
cd /usr/local/cellar/hadoop/3.3.1/libexec/bin

./hadoop jar /usr/local/Cellar/hadoop/3.3.1/libexec/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount ./input.txt output
```

## 4. output파일 다시 로컬로 옮기기
```bash
hadoop fs -ls hdfs://localhost:9000/user/hama2007 -> 파일이 있는지 확인
hadoop fs -get /user/hama2007/output ./
```

## 5. output
```
a	3
b	4
c	5
d	6
e	7
```

---
### 참고자료

[블로그](https://key4920.github.io/p/mac-os%EC%97%90-%ED%95%98%EB%91%A1hadoop-%EC%84%A4%EC%B9%98/)
<br>
[공식문서](https://hadoop.apache.org/docs/r3.3.1/hadoop-project-dist/hadoop-common/SingleCluster.html)
