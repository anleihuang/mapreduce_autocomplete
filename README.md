## Introduction
The goal of the repo is to build an architecture for Words Autocomplete Suggestion. Behind the scene, [N-Gram model](https://en.wikipedia.org/wiki/N-gram) is used to predict the next word(s).

This Hadoop MapReduce program is written in Python 3.7. Two MapReduce jobs are implemented and each of them consists of one mapper and one reducer.

## Architecture
### 1. MapReduce Job # 1
- Pre-process the input so content is read sentence-by-sentence instead of line-by-line
- Construct N-Gram Library through MapReduce framework (from 2-gram to N-gram models will be built)

<img src="https://github.com/anleihuang/mapreduce_autocomplete/blob/master/docs/nGram_MR2.png"  width="800" height="600">

### 2. MapReduce Job # 2
- Build Language Library based on probability. The output format is shown as "first phrase + following word + count" format which is constructed by the second MapReduce job
- Export the output to MySQL database which is ready to query by the front-end (web service). Here is an front-end template: [jQuery autocomplete tutorial](https://www.wowww.nl/2014/02/01/jquery-autocomplete-tutorial-php-mysql/)

<img src="https://github.com/anleihuang/mapreduce_autocomplete/blob/master/docs/nGram_MR2.png"  width="800" height="600">


## Implementation
1. Download the git repo
2. Copy or save the input files to ./inputs/ folder
3. Set up the environmental variables in ./bashrc
```
export HADOOP_HOME=//the path to where your hadoop is
export SQOOP_HOME=//the path to where your sqoop is
export MYSQL_USER=//mysql username
export MYSQL_PW=//mysql password
export MYSQL_HOST=//mysql host ip
export DB_NAME=//target schema name
export TABLE_NAME=//target table name
```
4. A database and table needed to be created before running the job
```
# log in to mysql through terminal
mysql -uroot -p
# create a database named test
CREATE DATABASE test; 
# grant all privileges to the root user
GRANT ALL PRIVILEGES ON test.* TO 'root'@'%'; 
# Use the test database
use test;
# create a table named ngram
CREATE TABLE ngram(first_phrase VARCHAR(100), following_words VARCHAR(100), count INT);
```
5. Execute `bash run.sh` on the terminal

## Result Snapshot
This is a query snapshot of the final MapReduce result.
```
SELECT * FROM ngram WHERE starting_phrase LIKE "%like%" ORDER BY count DESC LIMIT 10;
```
<img src="https://github.com/anleihuang/mapreduce_autocomplete/blob/master/docs/result.png"  width="400" height="400">


## Local Testing
A few commands are useful for debugging while developing the code

```
# make sure the python files have execution permission
chomd + x ./src/*

cat ./input/test1.txt | ./src/NGramLibBuildMapper.py 

cat ./outfile.txt | ./src/NGramLibBuildReducer.py

echo "foo foo quux labs foo bar quux" | ./src/NGramLibBuildMapper.py  | sort -k1,1 | ./src/NGramLibBuildReducer.py

echo "foo foo quux labs, foo bar quux. foo bar? foo foo quux labs foo! bar quux foo bar. foo foo quux labs foo bar quux foo bar" | ./src/NGramLibBuildMapper.py  | sort -k1,1 | ./src/NGramLibBuildReducer.py
```

## Environment Setup

### Hadoop Cluster
Set up a hadoop cluster with one name node and three data node in AWS
1. Hadoop Name Node: 1 x t2.large AWS EC2
2. Hadoop Data Node: 3 x t2.medium AWS EC2


### Sqoop + MySQL
- [Install Sqoop 1.4.7](https://programmer.help/blogs/5d805fb1ee5e9.html)
- Download MySQL JDBC connector( mysql-connector-java-5.1.39-bin.jar) and save the jar file to ${SQOOP_HOME}/lib/
```
mysql -h ${MYSQL_HOST} -P 3306
```

- Test MySQL connection through sqoop
```
sqoop list-databases --connect jdbc:mysql://${MYSQL_HOST}:3306
```


## Prerequisites
- java 8
- python 3.7
- Hadoop 3.2.1
- sqoop-1.4.7

## Challenges
One of the challenge confronted while building the MapReduce project in Python is that python does not support direct write to database. Unlike Java which has "DBOutputWritable" class to fulfill direct write, Python needs to first write data out to HDFS and then conduct Sqoop to transfer data from HDFS to database.
