# Assignment3 (1001) - WordCount Test

## Hadoop 3.3.1 + mac 10.15.7
### input.txt is from https://en.wikipedia.org/wiki/Intel

## 1. WordCount.java 컴파일하기
-> 아래 명령어 입력해서 JAVA_HOME 값 알기
```bash
/usr/libexec/java_home
```
fish shell 말고 zshell로 이동해서 수행(iTerm2)
```zsh
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home # 맞게 수정
echo ${JAVA_HOME} # 적용 확인
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
```
컴파일 시작
```zsh
cd /usr/local/cellar/hadoop/3.3.1
hadoop com.sun.tools.javac.Main WordCount.java # -> class파일이 총 3개 나옴(WordCount, WordCount$IntSumReducer, WordCount$TokenizerMapper)
jar cf wc.jar WordCount*.class # wc.jar파일로 합침
```
## 2. WordCount 시작
파일 복사
```
1. user/hama2007/input.txt 형태로 폴더안에 파일 집어넣기
2. hadoop fs -put ./user  /
```
WordCount 시작
```zsh
jps # 6개 모두 동작중인지 확인
hadoop jar wc.jar WordCount ./input.txt output
```
Output file hdfs에서 local로 복사
```zsh
hadoop fs -get /user/hama2007/output ./
```

## log
```zsh
2021-10-02 02:59:01,391 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
2021-10-02 02:59:01,899 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at /0.0.0.0:8032
2021-10-02 02:59:02,241 WARN mapreduce.JobResourceUploader: Hadoop command-line option parsing not performed. Implement the Tool interface and execute your application with ToolRunner to remedy this.
2021-10-02 02:59:02,251 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/hama2007/.staging/job_1633109339670_0003
2021-10-02 02:59:02,405 INFO input.FileInputFormat: Total input files to process : 1
2021-10-02 02:59:02,440 INFO mapreduce.JobSubmitter: number of splits:1
2021-10-02 02:59:02,518 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1633109339670_0003
2021-10-02 02:59:02,518 INFO mapreduce.JobSubmitter: Executing with tokens: []
2021-10-02 02:59:02,641 INFO conf.Configuration: resource-types.xml not found
2021-10-02 02:59:02,641 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2021-10-02 02:59:02,684 INFO impl.YarnClientImpl: Submitted application application_1633109339670_0003
2021-10-02 02:59:02,710 INFO mapreduce.Job: The url to track the job: http://hyungsucbookpro:8088/proxy/application_1633109339670_0003/
2021-10-02 02:59:02,710 INFO mapreduce.Job: Running job: job_1633109339670_0003
2021-10-02 02:59:07,774 INFO mapreduce.Job: Job job_1633109339670_0003 running in uber mode : false
2021-10-02 02:59:07,776 INFO mapreduce.Job:  map 0% reduce 0%
2021-10-02 02:59:11,828 INFO mapreduce.Job:  map 100% reduce 0%
2021-10-02 02:59:15,850 INFO mapreduce.Job:  map 100% reduce 100%
2021-10-02 02:59:15,857 INFO mapreduce.Job: Job job_1633109339670_0003 completed successfully
2021-10-02 02:59:15,926 INFO mapreduce.Job: Counters: 50
	File System Counters
		FILE: Number of bytes read=166300
		FILE: Number of bytes written=878089
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=87325
		HDFS: Number of bytes written=45379
		HDFS: Number of read operations=8
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters
		Launched map tasks=1
		Launched reduce tasks=1
		Data-local map tasks=1
		Total time spent by all maps in occupied slots (ms)=1716
		Total time spent by all reduces in occupied slots (ms)=1715
		Total time spent by all map tasks (ms)=1716
		Total time spent by all reduce tasks (ms)=1715
		Total vcore-milliseconds taken by all map tasks=1716
		Total vcore-milliseconds taken by all reduce tasks=1715
		Total megabyte-milliseconds taken by all map tasks=1757184
		Total megabyte-milliseconds taken by all reduce tasks=1756160
	Map-Reduce Framework
		Map input records=637
		Map output records=13218
		Map output bytes=139858
		Map output materialized bytes=166300
		Input split bytes=111
		Combine input records=0
		Combine output records=0
		Reduce input groups=4315
		Reduce shuffle bytes=166300
		Reduce input records=13218
		Reduce output records=4315
		Spilled Records=26436
		Shuffled Maps =1
		Failed Shuffles=0
		Merged Map outputs=1
		GC time elapsed (ms)=99
		CPU time spent (ms)=0
		Physical memory (bytes) snapshot=0
		Virtual memory (bytes) snapshot=0
		Total committed heap usage (bytes)=1253048320
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters
		Bytes Read=87214
	File Output Format Counters
		Bytes Written=45379
```