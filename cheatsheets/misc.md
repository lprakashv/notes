# Miscellaneous HowTos

Commands used in personal/professional Experience

## Java

### JShell

Multiple dependencies using maven local repos, use JAR files `:` (colon) separated

```bash
jshell --class-path ./jackson-databind-2.12.4.jar:./jackson-core-2.12.4.jar:./jackson-annotations-2.12.4.jar
```

### JVM Arguments

Hibernate enable SQL generation/logging

```bash
-Dspring.jpa.show-sql=true \
-Dspring.jpa.properties.hibernate.format_sql=true \
-Dlogging.level.org.hibernate.SQL=DEBUG \
-Dlogging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
```

## Golang

### Tests

Test Coverage display on UI

```bash
go tool cover -html=cover.out
```

### `go get`

To add a dependency for a package or upgrade it to its latest version:

```bash
go get example.com/pkg
```

To upgrade or downgrade a package to a specific version:

```bash
go get example.com/pkg@v1.2.3
```

To remove a dependency on a module and downgrade modules that require it:

```bash
go get example.com/mod@none
```

### Go - Misc

!!! info "AI-generated"

```bash
# Format and vet every package in the module.
go fmt ./...
go vet ./...

# Explain why a package is in the module graph.
go mod why example.com/module

# Remove unused requirements and add missing ones.
go mod tidy

# List available updates without changing go.mod.
go list -m -u all
```

## Makefile

!!! info "AI-generated"

Keep targets small, declare non-file targets as phony, and use the same commands
locally and in CI.

```make
.PHONY: fmt lint test build

fmt:
	go fmt ./...

lint:
	go vet ./...

test:
	go test -race ./...

build:
	go build ./...
```

Recipe lines must begin with a tab unless the Makefile changes `.RECIPEPREFIX`.

## Databases / SQL

### MS SQL Server

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

### PostgreSQL

random number b/w a and b (inclusive):

```sql
select floor(random()*(b-a+1)) + a;
```

## Git

Remove files from remote after adding in `.gitignore`:

```bash
git rm -r --cached .
```

Then git add, commit and push

Delete all untracked files:

```bash
git ls-files -z -o --exclude-standard | xargs -0 rm
```

Removing staged files:

```bash
git reset file
```

## Unix Commands

Process stats

```bash
top -p <pid>
top -i
```

Run a shell as another user:

```bash
sudo -u <username> -s
```

Filesystem and directory disk usage:

```bash
df -h
du -sh <directory>
```

### Networking

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

### AWK

```bash
less image-processing.log | sed -E -e "s/Img//g" | awk '{print $6".jpeg"}' | xargs -I '{}' sudo mv ./tmp/{} ./temp-images/


less nginx_access.log | sed -E -e "s/(\?|\&)([^=]+)\=([^&]+)//g" | awk '{print $2 "\t" $10}' | sort -k1n


less nginx_access.log | grep status=502 | sed -E -e "s/(\?|\&)([^=]+)\=([^&]+)//g" | awk '{arr[$10]++}END{for(a in arr) print arr[a], "\t" a}' | sort -k1n
```

#### Command fragments explained

!!! info "AI-generated"

- `sort -k1,1n` sorts numerically by only the first field. `-k1n` starts at the
  first field but does not explicitly end there.
- `xargs -I '{}' command '{}'` replaces each `{}` in `command` with one input
  line. Quote the placeholder when filenames may contain spaces.
- `sed -E -e 'expression'` enables extended regular expressions and supplies one
  editing expression.
- In `awk`, `arr[key]++` counts occurrences. An `END { ... }` block runs once
  after all input has been consumed and is a convenient place to print totals.

Prefer null-delimited filenames (`find ... -print0 | xargs -0 ...`) when names can
contain spaces or newlines.

## Nginx

```bash
nginx -s reload|reopen|quit|stop
```

conf files with server specifications: `/etc/nginx/sites-available/*.conf`

`/etc/nginx/sites-enabled/<---->`

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

## Scala

Scala reading from a file:

```scala
val source: String = Source.fromFile("/Users/lpv/Desktop/categoryHierarchy.json")(Codec.UTF8).getLines.mkString
```

## Sonatype

### Reliability note

!!! info "AI-generated"

!!! warning "Manual review"
    The publishing steps below describe the legacy OSSRH/Jira/staging workflow.
    Maven Central ended support for the legacy deployment protocol on June 30,
    2025. Keep this section only as historical context; verify any real release
    against the current Central Publisher Portal documentation.

### Current publishing direction

!!! info "AI-generated"

1. Create an account at the Central Publisher Portal.
2. Verify the namespace used by the artifact coordinates.
3. Sign release artifacts and provide the required POM metadata.
4. Use a current Maven- or Gradle-compatible Central publishing plugin.
5. Upload, validate, and publish a deployment through the portal or its API.

Source: [Maven Central publishing guide](https://central.sonatype.org/publish/publish-portal-guide/).

### Create sonatype account

1. Same passwords for `issues.sonatype.org` (JIRA), `oss.sonatype.org`, `central.sonatype.org`
2. Raise a jira request to open a repository.
3. They will ask you to verify a domain/groupid.

### Signing

1. Create key using “gpg” and save passphrase.
    1. `gpg --list-secret-keys`
2. Set short code (last 8 chars of key), passphrase, secret ring file path in gradle’s global properties (set in maven is using maven)
3. Distribute it to “central keystores” (ubuntu, etc.)
    1. `gpg --keyserver hkp://pool.sks-keyservers.net --send-keys <key last 8 chars are fine>`
    2. `gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys <key>`
4. Generate a secret key
    1. `gpg --export-secret-keys >~/.gnupg/secring.gpg`

### Publish

1. Use gradle’s `maven-publish` or some other plugin for maven if using maven.
2. Don’t forget to add credentials to `buildscript` (`publishscript`)

### Sonatype release

1. “close” published sonatype `"staging"` repo, you can check the content.
2. Release it.
3. If first release (promote), comment on the jira ticket.
