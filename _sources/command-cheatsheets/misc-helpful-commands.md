# Miscellaneous Helpful Commands - WIP

Commands used in personal/professional Experience

## JShell

Multiple dependencies using maven local repos, use JAR files `:` (colon) separated

```bash
jshell --class-path ./jackson-databind-2.12.4.jar:./jackson-core-2.12.4.jar:./jackson-annotations-2.12.4.jar
```

## Docker

Remove old dangling images

```bash
docker rmi `docker images --filter dangling=true
```

Remove container after running it

```bash
docker run —rm image-id
```

Run an image in a container with its name

```bash
docker run --rm `docker images --filter reference='*/log-generator' --format '{{.ID}}'`
```

## JVM Arguments - WIP

Hibernate enable SQL generation/logging

```bash
-Dspring.jpa.show-sql=true \
-Dspring.jpa.properties.hibernate.format_sql=true \
-Dlogging.level.org.hibernate.SQL=DEBUG \
-Dlogging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
```

## MS SQL Server

Running procedure

```sql
SELECT
  object_name(st.objectid) as ProcName
FROM
  sys.dm_exec_connections as qs
CROSS APPLY sys.dm_exec_sql_text(qs.most_recent_sql_handle) st
WHERE
  object_name(st.objectid) is not null;
```

Currently Running queries

```sql
SELECT sqltext.TEXT,
req.session_id,
req.status,
req.start_time,
req.command,
req.cpu_time,
req.total_elapsed_time
FROM sys.dm_exec_requests req
CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS sqltext;
```

## Git - WIP

Remove files from remote after adding int .gitignore:

```bash
git rm -r --cached .
```

Then git add, commit and push

## General Unix Commands - WIP

Process stats

```bash
top -p <pid>
top -i
```

User taking superuser role - ?

```bash
sudo -su <username>
```

Disk space

```bash
df -hk | du
```

Get open ports where applications are listening

```bash
netstat -ap tcp | grep -i "listen"

lsof -Pn -i4
lsof -Pn -i4 | grep LISTEN
sudo lsof -PiTCP -sTCP:LISTEN
```

All services listening on ports

```bash
netstat -tunlp
```

Local DNS

```bash
/etc/hosts
```

## Nginx Basics - WIP

```bash
nginx -s reload|reopen|quit|stop
```

conf files with server specifications: `/etc/nginx/sites-available/*.conf`

`/etc/nginx/sites-enabled/<---->`

## AWK - WIP

```bash
less image-processing.log | sed -E -e "s/Img//g" | awk '{print $6".jpeg"}' | xargs -I '{}' sudo mv ./tmp/{} ./temp-images/


less nginx_access.log | sed -E -e "s/(\?|\&)([^=]+)\=([^&]+)//g" | awk '{print $2 "\t" $10}' | sort -k1n


less nginx_access.log | grep status=502 | sed -E -e "s/(\?|\&)([^=]+)\=([^&]+)//g" | awk '{arr[$10]++}END{for(a in arr) print arr[a], "\t" a}' | sort -k1n
```

- `sort -k1n` - ???
- `xargs -I '{}'` - ???
- `sed -E -e ""` - ???
- `awk` with multi-line expression and for-loop.

## HDFS

```bash
hadoop fs <command>
```

Grepping across multiple files in HDFS

Recursive LS on a directory

1. GREP files
2. capture/awk file names (after 8th char)
3. get 1 input
4. use caret to be replaced by input
5. 10 multiple processes
6. execute bash script for hadoop fs -cat

Impl:

```bash
hadoop fs -ls -R /user/asdacd_account/feedFiles/2019/08/ | grep .csv | awk '{print $8}' | \
xargs -n 1 -I ^ -P 10 bash -c \
"hadoop fs -cat ^ | grep -q 961412 && echo ^"
```

## Kafka Debugging

To find the last 10 records

```bash
kafkacat \
-b <bootstrap-servers> \
-G lpv-kafkacat-consumer \
-t asda-storeinventory \
-o -10 \
-C \
-f '\nKey (%K bytes): %k\t\nValue (%S bytes): %s\nTimestamp: %T\tPartition: %p\tOffset: %o\n--\n'
```

To find the latest offset in a topic

```bash
kafka-run-class kafka.tools.GetOffsetShell \
--broker-list <bootstrap-servers> \
--topic asda-recipes-etl --time -1 \
| awk -F  ":" '{sum += $3} END {print sum}'
```

To find earliest offset in a topic

```bash
kafka-run-class kafka.tools.GetOffsetShell \
--broker-list <bootstrap-servers> \
--topic asda-recipes-etl \
--time -2 \
| awk -F  ":" '{sum += $3} END {print sum}'
```

To find offset of topic at a particular epoch-time

```bash
kafka-run-class kafka.tools.GetOffsetShell \
--broker-list <bootstrap-servers> \
--topic ukgr-recipe-hearst-etl-prod \
--time 1583298000000
```