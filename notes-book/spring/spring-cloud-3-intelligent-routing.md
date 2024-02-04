# Intelligent Routing

## Challenges with Individual Services

- Different ports
- Different addresses
- Different APIs and paths

Solution: __"Intelligent Routing"__

## Routing Service

- Via Gateway service (or API Gateway)
- Single point of entry for all clients

## Gateway Service

Provides:

- Dynamic routing and delivery
- Security and Filtering
- Auditing and Logging
- Request Enhancement
- Load balancing
- Different APIs for different clients

## Netflix Zuul

Zuul is a gateway service that provides dynamic routing, monitoring, resiliency, security and more.

- Proxy server
- Setting up routes
- Setting up filters

### Using Spring Cloud + Netflix Zuul Reverse Proxy

`Application.java`

```java
@SpringBootApplication
@EnableZuulProxy
public class Application {

  public static void main(String[] args) {
    SpringBootApplication.run(Application.class, args);
  }
}
```

### Using Spring Cloud + Netflix Zuul

#### With Service Discovery

`application.properties`

```properties
spring.application.name=gateway-service
eureka.client.service-url.defaultZone=http://localhost:8761/eureka
```

OR `application.yml`

```yaml
spring:
  application:
    name: gateway-service
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka
```

#### Without Service Discovery

`application.properties`

```properties
spring.application.name=gateway-service
ribbon.eureka.enabled=false
```

OR `application.yml`

```yaml
spring:
  application:
    name: gateway-service
ribbon:
  eureka:
    enabled: false
```

Default Route to Service Resolution with Service Discovery

| Request          | maps to Service                      |
|------------------|--------------------------------------|
| `/foo`           | spring.application.name=foo          |
| `/categories/1`  | spring.application.name=categories   |

__NOTEs:__

- *Prefix is stripped by default. Use `zuul.stripPrefixes=false` to disable.*
- *All services are added by default. Use `zuul.ignoredServices=<pattern>` to ignore services.*

#### With Service Discovery: Precise Routing

`application.properties`

```properties
spring.application.name=gateway-service
zuul.routes.<route_name>.path=/somepath/**
zuul.routes.<route_name>.serviceld=some_service_id
zuul.ignored-services=some_service_id
```

OR `application.yml`

```yaml
spring:
  application:
    name: gateway-service
  zuul:
    routes:
      ‹route_name>:
        path: / somepath/**
        serviceld: some_service_id
    ignored-services: some_service_id
```

#### Without Service Discovery: Precise Routing

`application.properties`

```properties
spring.application.name=gateway-service
zuul.routes.<route_name>.path=/somepath/**
zuul.routes.<route_name>.url=http://some_url_address/
```

OR `application.yml`

```yaml
spring:
  application:
    name: gateway-service
  zuul:
    routes:
      ‹route_name>:
        path: / somepath/**
        url: http://some_path_url/
```

### Zuul Filters

Filter types:

1. Pre -> before request
2. Route -> any kind of routing
    1. In fact @EnableZuulProxy sets up some default ‘route’ filters.
3. Post -> After request is executed.
4. Error -> Any of pre/route/post filter failed.

#### Creating a Zuul Filter

Extend & Implement ZuulFilter

`MyFilter.java`

```java
public class MyFilter extends ZuulFilter {
    // implement methods

    // Filter logic goes here
    // **Current implementation ignores return value**
    @Override
    public Object run() {
        // ...
    }

    // Whether or not the `run()` method should execute
    @Override
    public boolean shouldFilter() {
        // ...
    }

    // The type of filter: `pre`, `route`, `post`, `error`
    @Override
    public String filterType() {
        // ...
    }

    // The order of execution with respect to the other filters of the same type
    @Override
    public int filterOrder() {
        // ...
    }
}
```

Define a `@Bean` which returns the Filter

`MyConfig.java`

```java
@Configuration
public class MyConfig {

    @Bean
    public ZuulFilter myFilter() {
        return new MyFilter();
    }
}
```

#### Sharing between Filters: `RequestContext`

- Holds request, response, state and data information
- Only available for the duration of the request

```java
RequestContext ctx = RequestContext.getCurrentContext();

// Get the servlet request
HttpServletRequest req = ctx.getRequest();

// Get the servlet response
HttpServletResponse = res = ctx.getResponse();

// Set a variable
ctx.set("foobar", "PRE_FILTER_EXECUTED");

// Get a variable
String foobar = (String) ctx.get("foobar");
```

Example of setting the header using Filter:

```java
public class AbstractRequestHeaderFilter extends ZuulFilter {
    @Override
    public boolean shouldFilter() {
        return true;
    }

    @Override
    public String filterType() {
        return "pre";
    }

    @Override
    public Object run() {
        RequestContext ctx = RequestContext.getCurrentContext();
        ctx.addZuulRequestHeader("x-location", "INDIA");
        return null;
    }
}
```
