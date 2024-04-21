# Creating bucket notifications:

## To HTTP Endpoint:
This section mostly defines about sending the bucket notifications to a HTTP endpoint. This is of type "persistent" or "asynchronous".

1. Make sure `python3` is installed on your machine.
2. Clone this repo and run `$ python3 http_server.py` under protected environments. This is a very basic HTTP Server that accepts POST method and displays on stdout.
3. Install `awscli` package by referring to your OS distribution's preferred methods.
4. Configure `awscli`
```
# aws configure
AWS Access Key ID [None]: access
AWS Secret Access Key [None]: secret
Default region name [None]: 
Default output format [None]: 
```
5. Try creating a bucket to see if that works by specifying an endpoint in addition
```
# aws s3 --endpoint http://172.19.1.200 mb s3://jayanth
make_bucket: jayanth
```
6. Create the topic
```
# aws --endpoint http://172.19.1.200 sns create-topic --name bucketevents --attributes=file://topic.json --region=default
{
    "TopicArn": "arn:aws:sns:default::bucketevents"
}
```
7. List the created topic
```
# aws --endpoint http://172.19.1.200 sns list-topics --region=default
{
    "Topics": [
        {
            "TopicArn": "arn:aws:sns:default::bucketevents"
        }
    ]
}
```
8. Create a notification configuration. This doesn't provide any output
```
# aws --endpoint=http://172.19.1.200 s3api put-bucket-notification-configuration --bucket jayanth --notification-configuration file://notification.json
```
9. Now try creating an object
```
s3cmd put notification.json s3://jayanth/
```
10. See the HTTP Server logs
```
Received POST request:
{"Records":[{"eventVersion":"2.2","eventSource":"ceph:s3","awsRegion":"default","eventTime":"2024-04-21T10:03:18.419013Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"user"},"requestParameters":{"sourceIPAddress":""},"responseElements":{"x-amz-request-id":"89759221-f520-4594-a8af-8633d52181bd.14369.13245020851017049375","x-amz-id-2":"3821-default-default"},"s3":{"s3SchemaVersion":"1.0","configurationId":"HTTPNotification","bucket":{"name":"jayanth","ownerIdentity":{"principalId":"user"},"arn":"arn:aws:s3:default::jayanth","id":"89759221-f520-4594-a8af-8633d52181bd.14371.2"},"object":{"key":"notification.json","size":177,"eTag":"a60023221945e53a31f07df71f37f032","versionId":"","sequencer":"66E42466712CA919","metadata":[{"key":"x-amz-meta-s3cmd-attrs","val":"atime:1713693750/ctime:1713693688/gid:0/gname:root/md5:a60023221945e53a31f07df71f37f032/mode:33188/mtime:1713693688/uid:0/uname:root"}],"tags":[]}},"eventId":"1713693798.430517.a60023221945e53a31f07df71f37f032","opaqueData":""}]}
172.19.1.200 - - [21/Apr/2024 10:03:18] "POST / HTTP/1.1" 200 -
```
11. Additionally, topics on RGW can also be viewed
```
# radosgw-admin topic list
{
    "topics": [
        {
            "user": "",
            "name": "bucketevents",
            "dest": {
                "push_endpoint": "http://172.19.1.171:8000",
                "push_endpoint_args": "Version=2010-03-31&persistent=true&push-endpoint=http://172.19.1.171:8000&verify-ssl=False",
                "push_endpoint_topic": "bucketevents",
                "stored_secret": false,
                "persistent": true
            },
            "arn": "arn:aws:sns:default::bucketevents",
            "opaqueData": ""
        }
    ]
}
```

You may try exploring to capture a wide variety of events.

## Read more:
- https://docs.ceph.com/en/latest/radosgw/notifications/
- https://www.ibm.com/docs/en/storage-ceph/7?topic=management-creating-bucket-notifications
- https://www.redbooks.ibm.com/redpieces/pdfs/redp5715.pdf
