# Chorus Standalone

1. Download and install `chorus` standalone and `chorctl`
```
wget https://s3.clyso.com/chorus-artefacts/chorctl/latest/chorctl_Linux_x86_64.tar.gz
tar xf chorctl_Linux_x86_64.tar.gz
mv chorctl /usr/local/bin

wget https://s3.clyso.com/chorus-artefacts/standalone/latest/chorus_Linux_x86_64.tar.gz
tar xf chorus_Linux_x86_64.tar.gz
mv chorus /usr/local/bin

rm chorctl_Linux_x86_64.tar.gz chorus_Linux_x86_64.tar.gz
```

2. Perform the configuration and start Chorus standalone
Ensure the configuration file is located at `~/.config/chorus/config.yaml` or pass the configuration file with `-c` option to the command `chorus`
```
chorus
```
```
_________ .__                               
\_   ___ \|  |__   ___________ __ __  ______
/    \  \/|  |  \ /  _ \_  __ \  |  \/  ___/
\     \___|   Y  (  <_> )  | \/  |  /\___ \ 
 \______  /___|  /\____/|__|  |____//____  >
        \/     \/                        \/


Mgmt UI URL:	http://127.0.0.1:9672

S3 Proxy URL: 	http://127.0.0.1:9669
S3 Proxy Credentials (AccessKey|SecretKey): 		
 - user1: [access|secret]

GRPC mgmt API:	127.0.0.1:9670
HTTP mgmt API:	http://127.0.0.1:9671
Redis URL:	127.0.0.1:45917

Storage list:
 - ceph--1: http://172.19.1.200 < MAIN
 - ceph--2: http://172.19.1.160
```

3. Check lag between two buckets
```
chorctl check ceph--1 ceph--2 -b buk -u user1
```
```
Checking files in bucket buk ...
🪣 BUCKET | Match	 | MissSrc	 | MissDst	 | Differ	 | Error
✅ buk... | 4      	 | 0      	 | 0      	 | 0      	 | 0  
```

4. Add a specific bucket to the replication job
```
chorctl repl add -f ceph--1 -t ceph--2 -b buk -u user1
```

5. Check if the job has been added and the progress. This should do the initial replication
```
chorctl repl
```
```
NAME                           PROGRESS                 SIZE                    OBJECTS     EVENTS     PAUSED     LAG             AGE
user1:buk:ceph--1->ceph--2     [##########] 100.0 %     268.2 MiB/268.2 MiB     4/4         0/0        false      17.155266ms     9m
```

6. Observe the same on the interactive dashboard
```
chorctl dash
```

7. Going forward, all the S3 interaction must go via Chorus proxy so the events can be tracked. You still have a choice to either use Chorus proxy or the Chorus agent which uses bucket notifications instead
```
s3cmd -c proxy-cfg put 10M s3://buk
```
This should give an increase in the events which Chorus worker will eventually apply on the destination.

<img width="864" alt="image" src="https://github.com/zap51/chorus-examples/assets/45934027/b8afede1-de89-4b0d-a301-c2b17c5a80d5">

Checking the same on the destination should show that both are in sync.
```
chorctl check ceph--1 ceph--2 -b buk -u user1
```
```
Checking files in bucket buk ...
🪣 BUCKET | Match	 | MissSrc	 | MissDst	 | Differ	 | Error
✅ buk... | 5      	 | 0      	 | 0      	 | 0      	 | 0    
```
