# AWS Essentials

## Account

!!! info "AI-generated"

The email address used to create an AWS account controls its root user. Treat the
root user as break-glass access:

1. register a hardware-backed or other phishing-resistant MFA method where
   available;
2. do not create root access keys;
3. configure alternate security and billing contacts;
4. use AWS Organizations and IAM Identity Center for workforce access when the
   environment has more than one person or account;
5. grant roles with short-lived credentials and least privilege;
6. monitor root-user activity and keep a tested recovery procedure.

Avoid long-lived access keys for routine administration. When a workload runs on
AWS, give the compute service an IAM role instead of storing a key in code or on
disk.

## Billing

!!! info "AI-generated"

Use AWS Budgets for cost or usage thresholds and Cost Anomaly Detection for
unexpected patterns. Send notifications through configured contacts or SNS, and
tag resources so a cost can be traced to an owner and environment.

## CloudWatch

!!! info "AI-generated"

CloudWatch provides metrics, logs, alarms, dashboards, and related observability
features. Billing alarms use estimated-charge metrics; Budgets is usually the
clearer starting point for budget notifications.

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

!!! info "AI-generated"

A Region is a separate geographic area. An Availability Zone is one or more
discrete data centers with independent power, networking, and connectivity inside
a Region. Design across multiple AZs when the service must tolerate an AZ failure.
Service availability, price, and feature rollout vary by Region; do not assume a
particular Region always receives features first.

## IaaS Compute

### EC2 VM remote

!!! info "AI-generated"

- Prefer AWS Systems Manager Session Manager when it meets the access requirement;
  it avoids exposing SSH and managing shared private keys.
- For SSH, put the public key on the instance and protect the downloaded private
  key. A lost private key cannot be downloaded again.
- Security groups are stateful virtual firewalls. Allow only the required sources,
  protocols, and ports.
- T-family instances earn and spend CPU credits for burstable performance.
- Savings Plans and Reserved Instances can reduce eligible compute cost for
  predictable usage; they do not make an instance more reliable.
- Stopping an EBS-backed instance stops most instance compute charges, but EBS,
  Elastic IP, and other attached resources can still incur cost.
- A stop/start may move the instance to different physical hardware but keeps it
  in the same Availability Zone. A reboot normally stays on the same host.
- An AMI captures launch metadata and block-device snapshots; test restoration
  instead of treating image creation alone as a backup plan.

## IaaS Storage

### EBS

!!! info "AI-generated"

Elastic Block Store provides block volumes for EC2. Volumes can generally be
expanded, but shrinking requires creating and copying to a smaller filesystem and
volume. Most volumes attach to one instance at a time; Multi-Attach is limited to
specific volume types, instance types, and same-AZ use cases and still requires a
cluster-aware filesystem or application.

### EFS

!!! info "AI-generated"

Elastic File System is a managed NFS file service that can be mounted by multiple
clients. Mount targets live in VPC subnets and use security groups to control NFS
traffic. Choose its performance and throughput modes from the workload; its
shared filesystem semantics solve a different problem from EBS block storage.

### S3

!!! info "AI-generated"

S3 is regional object storage, not a mounted block or network filesystem. Clients
read and write objects by key through APIs. Design around object semantics rather
than comparing its latency directly with EBS or EFS.

- Block Public Access by default and grant access through IAM, bucket policies, or
  access points.
- Enable versioning when recovery from overwrite or deletion matters.
- Use lifecycle rules to transition or expire objects intentionally.
- Choose encryption and key policy from the data classification.
- Give workloads IAM roles; do not embed long-lived access keys in applications.
- Use separate buckets or access points when ownership, retention, policy, or
  blast-radius boundaries differ.

### S3 “Glacier”

!!! info "AI-generated"

S3 Glacier storage classes are S3 tiers for infrequently accessed archives, not
a separate service outside S3. Retrieval time and minimum-storage charges differ
by class: Instant Retrieval supports immediate access, while Flexible Retrieval
and Deep Archive use restore workflows that can take minutes to hours. Match the
class and lifecycle rule to the recovery objective.

### Cloudfront (not S3!)

!!! info "AI-generated"

CloudFront is a content-delivery network. It caches content at edge locations and
fetches misses from an origin such as S3, an Application Load Balancer, or an HTTP
server. It does not replicate the source S3 bucket across Regions.

## IaaS Networking

### VPC (Virtual Private Cloud)

!!! info "AI-generated"

A VPC is a logically isolated regional network. Subnets belong to one Availability
Zone and are classified by their routes, not by a “public/private” flag:

- a public subnet has a route to an internet gateway and workloads still need a
  public address and security policy to communicate through it;
- a private subnet has no direct internet-gateway route and may use NAT for
  outbound IPv4 access;
- isolated subnets have no internet route.

Security groups filter traffic at network interfaces; network ACLs filter at the
subnet boundary. Routes provide reachability but do not grant application access.

### NAT Gateway

!!! info "AI-generated"

A public NAT gateway lets resources in private subnets initiate outbound IPv4
connections through an Elastic IP. Return traffic is allowed, but unsolicited
inbound connections are not. It is an Availability-Zone resource; resilient
designs avoid routing several AZs through one NAT gateway.

### Internet Gateway

!!! info "AI-generated"

An internet gateway is a VPC attachment used by routes to and from the public
internet. A route alone does not make a workload reachable: it also needs a public
address and security-group/network-ACL rules that allow the traffic.

### Elastic IPs

!!! info "AI-generated"

An Elastic IP is a static public IPv4 address that can be remapped between
resources. AWS charges for public IPv4 addresses, including addresses in use, so
release unused addresses and prefer IPv6 or shared front doors where practical.

Connectivity examples include Client VPN for individual clients, Site-to-Site VPN
for encrypted IPsec tunnels from a customer network, Direct Connect for dedicated
connectivity, VPC peering for selected VPC pairs, and Transit Gateway for hub-and-
spoke routing.

### ELB (Elastic Load Balancer)

!!! info "AI-generated"

Elastic Load Balancing distributes traffic across healthy registered targets.
Application Load Balancers operate at HTTP/HTTPS, Network Load Balancers at
transport level, and Gateway Load Balancers integrate virtual network appliances.
Health checks control routing; they do not replace application monitoring.

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

!!! info "AI-generated"

Aurora is an RDS database engine compatible with MySQL or PostgreSQL. It separates
compute instances from a distributed cluster storage layer. Choose provisioned or
supported Serverless configurations from workload shape, connection behavior,
scaling limits, availability, and cost—not from the word “serverless” alone.
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

!!! info "AI-generated"

- **Kinesis Data Streams:** partitioned event streaming with ordered records per
  shard and configurable retention; it is not simply a queue.
- **SQS:** managed standard or FIFO message queues with polling-based consumers.
- **SNS:** publish/subscribe fan-out to endpoints such as SQS, Lambda, HTTP, or
  mobile notifications.

Compare ordering, replay, retention, fan-out, throughput, and total request/data
cost for the actual traffic pattern.

## PaaS

When things just works ==> giving the codebase, clicking a button and everything is performed under the hood, software updates etc.

### Elastic Beanstalk

!!! info "AI-generated"

Deploys supported application platforms onto managed AWS resources. It provisions
and coordinates components such as EC2, load balancing, health reporting, and
deployment policies while still exposing the underlying resources for inspection.

### ECS (Elastic Container Service)

!!! info "AI-generated"

Runs containerized tasks and services on EC2 capacity or AWS Fargate. A task
definition is the versioned runtime contract; a service maintains the desired
task count and can integrate with load balancing and deployment controls.

### FaaS / AWS Lambda

!!! info "AI-generated"

Lambda runs event-driven functions without managing servers. Configure memory,
timeout, concurrency, retries, dead-letter or failure destinations, and
idempotency from the event source's delivery semantics.

## Managed Application Services

### Cognito

- User Authentication service

### API Gateway

!!! info "AI-generated"

API Gateway publishes HTTP, REST, and WebSocket APIs with features such as routing,
authorization integration, throttling, validation, and usage controls. It is an
API front door, not a general replacement for every load balancer.

### AppSync

- GraphQL

### Amplify

!!! info "AI-generated"

- Tools and managed services for building and hosting web and mobile applications

### AWS SageMaker

- Machine Learning

### Lex

- Chatbots

….many more!!
