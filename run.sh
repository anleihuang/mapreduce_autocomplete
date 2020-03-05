#!/bin/bash

set -e

## create an input directory named /nGram/input/ on HDFS
hdfs dfs -mkdir /nGram
hdfs dfs -mkdir /nGram/input/

## copy the input files to this newly created HDFS directory
hdfs dfs -put ./${YOUR_INPUT_DIR}/* /nGram/input/

## Since the results of the mapreduce job is saved to "/nGram/output"
## We need to make sure this directory is removed before moving forward
# hdfs dfs -rm -r /nGram/output

## Execute MapReduce Job # 1
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
            -D mapreduce.job.name='job1-buildNGramModel' \
            -mapper "NGramLibBuildMapper.py 2" \
            -reducer NGramLibBuildReducer.py \
            -input hdfs:///nGram/input/* \
            -output hdfs:///nGram/output \
            -file /home/ubuntu/autoCom/NGram/src/NGramLibBuildReducer.py \
            -file /home/ubuntu/autoCom/NGram/src/NGramLibBuildMapper.py

## Execute MapReduce Job # 2
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
            -D mapreduce.job.name='job2-buildLanguageModel' \
            -mapper "LanguageModelMapper.py 3" \
            -reducer "LanguageModelReducer.py 4" \
            -input hdfs:///nGram/output \
            -output hdfs:///nGram/db  \
            -file /home/ubuntu/autoCom/NGram/src/LanguageModelReducer.py \
            -file /home/ubuntu/autoCom/NGram/src/LanguageModelMapper.py

## Export the final results on HDFS to MySQL through SQOOP
$SQOOP_HOME/bin/sqoop export \
            --connect jdbc:mysql://${MYSQL_HOST}:3306/${DB_NAME} \
            --username ${MYSQL_USER} \
            --table ${TABLE_NAME} \
            --export-dir /nGram/db \
            --input-fields-terminated-by ":"

