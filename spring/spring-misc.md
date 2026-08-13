# Spring Miscellaneous

## Spring AOP

ProxyFactory:

```java
// class IntImpl implements Int { … }

ProxyFactory pf = new ProxyFactory(new IntImpl());
Int eye = (Int) pf.getProxy();
```

MethodAdvice:

```java
pf.addAdvice(new MethodBeforeAdvice() {
 @Override
 public void before(Method m, Object[] args, Object target) {
  …
 }
});
```

Pointcut:

```java
@Pointcut("execution(* adviseMe(..))")
private void anyMethodCalledAdviseMe() {
 
}
```

## Spring JPA Id Generation

Use sequences for `@Id` columns:

```java
@Id
@SequenceGenerator(name "gen_name", sequenceName = "…", schema = "…")
@GeneratedValue(generator = "gen_name")
```

Use default for non-primary key columns

```sql
ALTER TABLE pimcatalog.BUNDLE_MASTER_INFO add constraint df_bundle_cin default next value for pimcatalog.bundle_id_seq for CONSUMER_ITEM_NUMBER;
```

Use `saveAndFlush` to get the updated entities having some column values as default.
