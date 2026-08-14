# Spring Cloud Fundamentals

Netflix OSS + Spring + Spring Boot = Spring Cloud!

## Spring cloud stack

1. [Service Discovery](./spring-cloud-2-service-discovery.md)
2. [Distributed Configuration](./spring-cloud-1-distributed-config.md)
3. Client-side Load balancing (CSLB)
4. [Intelligent routing](./spring-cloud-3-intelligent-routing.md)
5. Fault tolerance

Spring Cloud projects:

- __Spring Cloud Config__
- Spring Cloud Cluster
- Spring Cloud Consul
- Spring Cloud Stream
- __Spring Cloud Netflix__
- Spring Cloud Sleuth
- More...

Spring Cloud Fundamentals ==> __Spring Cloud Config__ + __Spring Cloud Netflix__

### Spring Cloud Netflix

- Spring Cloud Netflix Eureka Server
- Spring Cloud Netflix Eureka Client
- Other Spring Cloud Netflix projects...

## Version scope and current equivalents

!!! info "AI-generated"

!!! warning "Manual review"
    This Spring Cloud series uses the Camden-era stack. Its Config, Eureka,
    Ribbon, Zuul, Hystrix, and Turbine examples should not be copied into a new
    project without checking the selected Spring Boot/Spring Cloud release train.
    Ribbon, Zuul 1, Hystrix, and Turbine moved to maintenance mode and are absent
    from current Spring Cloud Netflix documentation.

For a new system, start with the current release-train documentation and consider:

| Legacy topic in these notes | Current starting point |
|---|---|
| Ribbon | Spring Cloud LoadBalancer |
| Zuul 1 | Spring Cloud Gateway |
| Hystrix | Spring Cloud CircuitBreaker with a supported implementation |
| Hystrix Dashboard/Turbine | Micrometer metrics, traces, and an observability backend |
| `bootstrap.yml` Config client | `spring.config.import=configserver:` |

Eureka client and server remain available in Spring Cloud Netflix. The warning
is about version scope, not about every concept in the series being obsolete.

Further reading: [Spring Cloud projects](https://spring.io/projects/spring-cloud)
and [Spring Cloud Netflix](https://docs.spring.io/spring-cloud-netflix/reference/).
