# CSLB

Outine:

- Load Balancing
  - server side
  - client side
- Netflix Ribbon
  - With and without Service discovery
    - `@LoadBalanced`
    - `@RibbonClient`
  - Custom Ribbon configuration

In cloud world:

From __multiple instances with a single LB ( manageable )__ to __multiple service and multiple instances with multiple LBs__

## Server-side vs Client-side LB

| Server-side                          | Client-side                          |
|--------------------------------------|--------------------------------------|
| Server distributes requests          | Client distributes load              |
| Hardware or software based           | Software based                       |
| Extra hop                            | No extra hops                        |
| Various balancing algorithms support | Various balancing algorithms support |
| Occurs outside the request process   | Occurs within the request process    |
| Centralized or distributed           | Typically distributed                |

## Netflix Ribbon

Ribbon is an inter-process communication (IPC) / remote procedure calls (RPC) library with built in software load balancers.

### Spring + Netflix Ribbon

- Full integration with Spring's `RestTemplate`
- Customize configuration for different:
  - Balancing algorithms
  - Availability checks

Two new Annottations:

1. `@LoadBalanced` : Marks a `RestTemplate` to support load balancing
2. `@RibbonClient` : Used for custom configurations and when service discovery is absent.

### Creating a `@LoadBalanced` `RestTemplate`

`MyConfiguration.java`

```java
@Configuration
public class MyConfiguration {
    @Bean
    @LoadBalanced // <-----
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

__NOTEs:__

- @LoadBalanced creates a RestTemplate interceptor which utilises the Ribbon load balancer client to distribute load b/w multiple instances.
- By default -> Round-Robin algorithm.

#### With service discovery

__Suppose ...__
> `my-service` is the name of a service running on port `9000` at `mycompany.com` and is discoverable via Service Discovery. There are 2 instances running.

__Instead of ...__

```java
restTemplate.getForEntity("http:/mycompany.com:9000/u/1", ...);
```

__User `RestTemplate` like this instead ...__

```java
restTemplate.getForEntity("http:/my-service/u/1", ...);
```

#### Without service discovery

`MyConfiguration.java`

```java
@Configuration
@RibbonClient(name = "someservice")
public class MyConfiguration {
    // ...
}
```

`application.properties`:

```properties
<ribbon-client-name>.ribbon.eureka.enabled=false
<ribbon-client-name>.ribbon.listOfServers=http://host:9090, http://host:9091
```

OR `application.yml`:

```yaml
<ribbon-client-name>:
  ribbon:
    eureka:
      enabled: false
    listOfServers: http://host:9090, http://host:9091
```

__NOTEs:__

- replace the `<ribbon-client-name>` with the `name` field value of `@RibbonClient`.

Use it like:

```java
restTemplate.getForEntity("http://someservice/", ...);
```

### Custom Configuration of Ribbon Clients

`MyConfiguration.java`

```java
@Configuration
@RibbonClient(
    name = "otherservice",
    configuration = OtherServiceConfig.class)
public class MyConfiguration {
    // ...
}
```

`OtherServiceConfig.java`

```java
@Configuration
public class OtherServiceConfig {
    // ...
}
```

Benefits:

- Can have different package so that it is not picked up by `@ComponentScan`
- Standard `@Configuration` class
- Can define `@Bean`s for customization

Spring Cloud Netflix provides the following beans by default for ribbon (`BeanType` beanName: `ClassName` ):

- `IClientConfig` ribbonClientConfig: `DefaultClientConfigImpl`
- `IRule` ribbonRule: `ZoneAvoidanceRule`
- `IPing` ribbonPing: `NoOpPing`
- `ServerList<Server>` ribbonServerList: `ConfigurationBasedServerList`
- `ServerListFilter<Server>` ribbonServerListFilter: `ZonePreferenceServerListFilter`
- `ILoadBalancer` ribbonLoadBalancer: `ZoneAwareLoadBalancer`

Creating a bean of one of those type and placing it in a `@RibbonClient` configuration (such as FooConfiguration above) allows you to override each one of the beans described. Example:

```java
@Configuration
public class FooConfiguration {
    @Bean
    public IPing ribbonPing(IClientConfig config) {
        return new PingUrl();
    }
}
```

2 Key beans:

- `IRule` : load balancing algorithm.
- `IPing` : availability checks.

#### `IRule`

`IRule` implementations:

1. `RoundRobinRule`
2. `ResponseTimeWeightedRule`
3. `RandomRule`
4. `ZoneAvoidanceRule`

__NOTEs:__

- `ResponseTimeWeightedRule` and `ZoneAvoidanceRule` are both “round-robin” they just re-order based on different strategies.
- `ZoneAvoidanceRule` is AWS specific.

Example LB strategy `IRule` Bean:

```java
@Configuration
public class OtherServiceConfig {
    @Bean
    public IRule ribbonRule() {
        return new RoundRobinRule();
    }
}
```

#### `IPing`

Checks the liveliness of the services being load-balanced.

Default implementations:

1. `DummyPing` : Always returns true, route requests to all the services regardless of their liveliness.
2. `PingUrl` : Typically a health check URL, validate an expected response.
3. `NIWSDiscoveryPing` : Automatically setup when we are using SD / Eureka.

Example Liveness check `IPing` bean:

```java
@Configuration
public class OtherServiceConfig {
    @Bean
    public IPing ribbonPing() {
        PingUrl pingUrl = new PingUrl();
        pingUrl.setExpectedContent("true");
        return pingUrl;
    }
}
```
