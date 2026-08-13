# AWS Essentials

## Account

AWS Account signup with email id ==> Root account (captain of the starship)

__NOTEs:__

- Do not use the Root account after the initial setup!
- Setup and Use MFA (multi factor authentication keys for your root account and IAM users)

First steps:

1. Create group using IAM with admin, developer, etc specific permissions/roles.
2. Delete the root user’s secret access key if it is present (should never leak in public).
3. Create an admin user and add it to the admin group. Use this for further admin actions.
4. Create secret access keys for the admin IAM user and store it securely somewhere. If the access key is ever leaked out, delete it immediately and generate a new one!

## Billing

- Add email alerts from the Billing service

## CloudWatch (logging and monitoring service)

- You can add “alarms” for billing, with SNS.

## Birth of Cloud

- initially there used to be physical servers
  - Self hosted
  - Colocation
  - Leased
- All are example of on-premise
- Not elastic and not able to scale well and need to be managed.
- Virtualisation technologies came which were able to split the machine resources and create a virtual machine out of it.
- Clouds took advantages of it to scale and provide elasticity
- There is a shared responsibility model for the cloud as they manage hardware and physical servers and users have to maintain the software and updates.
- Called now “IaaS” - infrastructure as a service. AWS provides an infrastructure as a service to us.
- EC2 and S3 are the oldest AWS services even before dropbox.

## Regions and Availability Zones (AZ)

- AZ is a data centre within a region.
- Ohio, Oregon and North Virginia (us-east) are the largest regions and AZs. First updates comes here.

## IaaS Compute

### EC2 VM remote

- You are asked to generate key-pair for the instance
- You can download the .pem file ==> it is the only private key there is, just don’t lose it!
- Public key is already present in the was instance.
- Save the .pem file securely somewhere on your machine.
- No you can SSH into the instance using the .pem file and the URL/endpoint provided.

Instance Types:

- Size ==> T-shirt sizes like model for size of machine.
- T instances use compute credits for later burst usage
- Reserved instances are great way to save money when you know what you workload is.

Connecting to internet:

- “Security groups” act as firewall/filter from the public internet.
- Outgoing traffic allows all ==> can connect to internet and install softwares etc.

EC2 actions:

- “Stop” and “start” ==> this might move the VM instance into a different AZ! Do this if you are facing trouble connecting to the machine (there might be a failure at that AZ).
- “Reboot” will do a software reboot of the VM on the same physical machine.
- Stopped instance won’t be changed with the compute cost but there will be data cost for hard drive (which will be minimal).
- You can create and AMI image from an existing EC2 instance to clone this VM (all the hard drive and software intact) ==> you can use the image in case the VM crash or corrupt to rest it to the default fresh configuration.

## IaaS Storage

### EBS

Elastic Block storage (grow and shrink in size)

- Once a EBS volume os plugged into the EC2 instance it cannot be shared across with another EC2 instance.
- Automatically attached to the EC2 and given OOTB

### EFS

Elastic File System

- AWS version of the NAS (Network attached storage)
- Allows you to mount and share drive across multiple EC2 instances.
- Isn’t as fast as EBS as it is not that closely attached to the raw hardware.
- You can create the EFS from the AWS services console
  - Install “nfs-common” (if using ubuntu) on each connected machine where EFS need to be accessed.
  - Create a mount point ==> instruction are given in the AWS Console.
- Security groups work exactly like EC2

### S3

- One of the first AWS services.
- Slower than both EBS and EFS.
- Can share all kinds of files directly with the users without having to configure any security polity and mounting etc.
- You don’t need a server to host your files (which is required in case of an EFS)
- Keep separate buckets for different kind of security sensitive files to keep different settings for each bucket.

__NOTEs:__

- You can use the AWS CLI and SDK to access and manage your AWS services.
- While working with SDK, avoid using and leaking the access key and secret into the server
- For this you can create a role with specific permission to a particular EC2 instance, then you won’t need a key to work with SDK.

### S3 “Glacier”

- For “colder” files (files not being used much), you can opt for a cheaper file storage than S3.
- Costs a fraction that S3.
- Ideal for backups.
- If you want to access some data from “Glacier” it is freezing cold and need to become hot ==> this can take several hours ==> only keep data not frequently used into “S3 Glacier”

### Cloudfront (not S3!)

- CDN
- We can “distribute” a bucket across multiple regions (or across the hold world)

## IaaS Networking

### VPC (Virtual Private Cloud)

- Local network between in the AWS services isolated from the public internet
- e.g., n computers connected to each other using a network switch without the internet.

NOTE : We can create multiple subnets to groups different networking privileges for different AWS services.

- Private subnet for db servers
- Public subnet for external facing services

### NAT Gateway

> door-knob only on the inside, outside traffic can’t get in (router without port-forwarding enabled).

### Internet Gateway

> door-knob on the both sides

### Elastic IPs

- static IP
- Ipv4 addresses are precious resources, hence, Amazon will charge a small fee to let you keep an Elastic IP without it being bound to some addresses/instance/EC2/server
- Make sure you release the Elastic IP when you shutdown a service.

2 main use cases of VPC:

1. Developer connecting to DB servers without it being open to public internet.
2. Site to Site VPC ==> ???

### ELB (Elastic Load Balancer)

- Checks health of the target

### Route 53

> AWS DNS

- Use this to point to your ALB (ELB)
- If we want to transfer domain to route 53, we can point the domain’s DNS server to route 53 servers.

## DBaaS

NOTE : You can still use database server inside a EC2 instance just like your on-premise environment.

### RDS

- Relational Database service
- Multiple vendor options

### AWS Aurora

- Mysql and Postgres compatible RBBMS managed service
- Serverless model
- A lot more managed by AWS

### DynamoDB

- AWS’s NoSQL offering
- Easier to scale up if you have partitioned your keys correctly
- They even provide global tables
  - Replicated tables for speed and redundancy

### DocumentDB

- Mongo like database

### ElastiCache

- Redis
- Memcache

### Redshift

- Big data store

NOTE : Datalake vs Data warehouse

- Datalake - box of books (unorganized)
- Data warehouse - labelled, organised data ==> optimized Postgres

## Messaging Services

- Kinesis ==> realtime large data queue
- SQS ==> Simple Queue service, can get really expensive on sending lots and lots of data.
- SNS ==> Simple Notification service

## PaaS

When things just works ==> giving the codebase, clicking a button and everything is performed under the hood, software updates etc.

### Elastic Beanstalk

### ECS (Elastic Container Service)

### FaaS / AWS Lambda

- Serverless Architecture

## SaaS

### Cognito

- User Authentication service

### API Gateway

- Similar to LB but very heavy on REST APIs

### AppSync

- GraphQL

### Amplify

- Apps boiletplate

### AWS SageMaker

- Machine Learning

### Lex

- Chatbots

….many more!!
