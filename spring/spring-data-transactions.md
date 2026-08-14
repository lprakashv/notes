# Data Transactions with Spring

## Transaction

Multiple actions performed as a single group

### ACID Transactions

!!! info "AI-generated"

- __Atomicity:__ a transaction commits as one unit or has no effect.
- __Consistency:__ a committed transaction preserves declared invariants such as
  constraints; the application still has to encode the correct business rules.
- __Isolation:__ concurrent transactions interact according to the configured
  isolation level. Weaker levels allow specific anomalies.
- __Durability:__ an acknowledged commit survives the failures covered by the
  database's persistence and replication configuration.

### Transaction Types

!!! info "AI-generated"

- __Local:__ one transactional resource, such as a JDBC connection.
- __Global/distributed:__ one unit of work coordinates multiple transactional
  resources, commonly through JTA/XA. This adds failure modes and should not be
  confused with an ordinary transaction inside one database.

## Spring Framework

Consistent programming model across global and local transactions.

### Spring Transaction management types

#### Programmatic

- Custom code for transaction management.

Example:

```java
public void saveTicket(Ticket ticket) {
  Session session = sessionFactory.getCurrentSession();
  session.getTransaction().begin();   //--
  session.save(ticket);               //  | <=== transaction
  session.getTransaction().commit();  //--
}
```

#### Declarative

- Manages transaction using Spring-specific annotations.
- Separates transaction management from business code.

Example:

```java
@Transactional
public void scheduleRelease(Ticket ticket, Release release) {
  ticketDao.saveTicket(ticket);
  assignToRelease(ticket, release);
  doOtherStuff(ticket);
}
```

Manages everything:

1. Begin
2. Suspend
3. Commit
4. Rollback
5. Transactional parameters

### Transaction Managers

__Programmatic Transaction Management:__

1. __Transaction template:__ Similar to Spring templates like `JdbcTemplate` and other available templates.
2. __Platform transaction manager:__ Handles transactions across Hibernate, JDBC, JPA, JMS, etc.

__Spring Transaction Managers:__

1. Platform transaction manager
2. JTA
3. Hibernate
4. DataSource
5. __JPA__

### `@Transactional` annotation

- Proxy is created to hold transaction management code.
- Annotation used at the class, interface or method level.
- Transaction propagation is handled automatically.

__NOTE:__ In Spring boot, it works without configuration.

### Spring Configuration

- JPA Transaction Manager: Registers a transaction manager for us.
- Additional configuration: Datasource, entity manager, repositories.
- Spring Data Repositories.

### Lifecycle and Scope

#### Database Transaction

__`@Transactional`__ defines a single transaction, in the scope of a __persistence context__.

#### Persistence Context

- Defined in __JPA__
- Handles a set of entities that contain data to be persisted.

### How `@Transactional` works?

Via proxies!

#### Transactional call path

!!! info "AI-generated"

~{Direct call versus transaction proxy}(<spring-transaction-proxy.json> "A direct invocation bypasses transaction advice; a call through the proxy begins, invokes, and completes the transaction.")

#### Proxy

- __Transaction Interceptor:__ Intercepts method calls.
- __Platform transaction manager:__ Handles transactions.

Difference proxies in Spring (JPA?) transaction handling:

1. __Persistence context proxy__
2. __Entity manager proxy__
3. __Transaction aspect__
4. __Transaction manager__

### Rollbacks

!!! info "AI-generated"

By default, Spring marks a transaction for rollback when an unchecked
`RuntimeException` or an `Error` escapes the transactional boundary. Checked
exceptions do not trigger rollback unless configured.

- Use __`@Transactional(rollbackFor=Exception.class)`__ to state otherwise.
- Use __`@Transactional(noRollbackFor=SpecificException.class)`__ to avoid rollback on a specific exception.

The usual proxy-based flow is:

1. Application code throws out of the proxied transactional method.
2. The transaction interceptor applies rollback rules.
3. The transaction manager commits or rolls back the resource transaction.

Self-invocation normally bypasses the proxy, and catching an exception inside the
method prevents the interceptor from seeing it unless the transaction is marked
rollback-only explicitly.

__NOTE:__

To enable the transaction logging from Spring, set: `logging.level.org.springframework.transaction.interceptor=TRACE`

### Transaction management code

Configuration:

```java
private final TransactionTemplate transactionTemplate;

// constructor
public ReleaseService(PlatformTransactionManager transactionManager) {
  this.transactionTemplate = new TransactionTemplate(transactionManager);
  this.transactionTemplate.setPropagationBehaviorName("PROPAGATION_REQUIRES_NEW");
  this.transactionTemplate.setReadOnly(true);
}
```

A simple 2 step transaction with the above configuration:

```java
transactionTemplate.execute(new TransactionCallbackWithoutResult() {
  public void doInTransactionWithoutResult(TransactionStatus status) {
    try {

    } catch (NoSuchElementException exception) {
      exception.printStackTrace();
      status.setRollbackOnly();
    }
  }
});
```

Fine-grained control in programmatic transaction management, using platform transaction manager directly.

```java
public Release scheduleRelease(Release release) {
  TransactionDefinition transactionDefinition = new DefaultTransactionDefinition();
  TransactionStatus transactionStatus = transactionManager.getTransaction(transactionDefinition);

  try {
    createTickets(release);
    assignTicketsToRelease(release.getId(), release.getTickets());

    transactionManager.commit(transactionStatus);
  } catch (RuntimeException e) {
    transactionManager.rollback(transactionStatus);
    throw e;
  }

  return release;
}
```

#### Declarative transaction management (vs Programmatic)

- Manage transaction via configuration.
- Separate transaction logic from business logic.
- Easy to maintain.
- Preferred when a lot of transaction logic.
