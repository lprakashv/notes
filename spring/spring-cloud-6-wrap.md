# Wrap - Big Picture

## System components

!!! info "AI-generated"

~{Cloud-native system components}(<spring-cloud-system.json> "Gateway, discovery, configuration, and application-service components in the legacy Spring Cloud example.")

## Startup sequence

### Fetch configuration

!!! info "AI-generated"

~{Startup configuration phase}(<spring-cloud-startup-config.json> "Gateway and application services fetch external configuration from the Config Server.")

### Register instances

!!! info "AI-generated"

~{Startup registration phase}(<spring-cloud-startup-registration.json> "Gateway and service instances register their locations and health with the discovery server.")

## Request flow

Example request to service A:

1. Request starts with the gateway (Zuul)
2. Gateway utilises already cached location of services A <> or asks Discovery server for Service A’s location.
3. Makes “hystrix-protected” call to service A.
4. Service A’s Response depends upon Service B, then same (if location cached then use it otherwise ask Discovery Server for it).
5. Makes “hystrix-protected” call to Service B.
6. Service B responds -> Service A responds -> Gateway Responds.

> There are other Spring Cloud projects as well (apart from the Netflix projects) e.g., Spring Cloud Bus, etc
