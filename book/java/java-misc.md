# Java - Misc

## Strings

!!! info "AI-generated"

- The interned string pool moved from PermGen to the regular heap in Java 7.
- String concatenation with `+` is compiled to an implementation chosen by the
  compiler/runtime. Modern JDKs may use `invokedynamic`; do not rely on a specific
  `StringBuilder` translation.
- `String.concat` accepts one `String`; `+` converts operands using string
  conversion rules.
- Since Java 7u6, `substring` copies the requested range instead of retaining the
  original backing array.
- `String` is immutable. Use `StringBuilder` for repeated single-threaded mutation
  when profiling shows concatenation is a hot path.

## Stream

- The data comes from elsewhere (a collection, array, generator function, or I/O channel) and is processed through a pipeline of computational steps to produce a result or side effect, at which point the stream is finished.
- Stream's __focus is on computation__, __not data__.
- Streams provide __no storage for the elements that they process__*, and the lifecycle of a stream is more like a point in time — the invocation of the terminal operation.
- For streams, __only the terminal operation is eager, all the others are lazy__.
- Stream operations represent a functional transformation on their input (also a stream), rather than a mutative operation on a data set (filtering a stream produces a new stream whose elements are a subset of the input stream but doesn't remove any elements from the source).

Example of non-stream vs stream operation:

```java
//Ad-hoc query over a collection

Set<Seller> sellers = new HashSet<>();
for (Txn t : txns) {
  if (t.getBuyer().getAge() >= 65)
    sellers.add(t.getSeller());
}

List<Seller> sorted = new ArrayList<>(sellers);

Collections.sort(sorted, new Comparator<Seller>() {
  public int compare(Seller a, Seller b) {
    return a.getName().compareTo(b.getName());
  }
});

for (Seller s : sorted)
  System.out.println(s.getName());
```

```java
txns.stream()
  .filter(t -> t.getBuyer().getAge() >= 65)
  .map(Txn::getSeller)
  .distinct()
  .sorted(comparing(Seller::getName))
  .map(Seller::getName)
  .forEach(System.out::println);
```

Key Advantages:

1. No distraction of garbage variable (sellers, sorted in the above example)
2. Don't have to keep track of context which leads to code understanding on one glance, less error prone.

## Class Loaders

!!! info "AI-generated"

`javac` compiles source into class files. At runtime, class loaders locate class
definitions and define `Class<?>` objects. Current JDKs have three built-in loader
roles:

1. **Bootstrap loader:** built into the VM; loads foundational runtime classes and
   is commonly represented by `null` from `Class.getClassLoader()`.
2. **Platform loader:** loads Java SE platform and JDK runtime classes.
3. **System/application loader:** normally loads application classes from the
   class path or module path.

The pre-Java-9 extension mechanism, `rt.jar`, `lib/ext`, and `java.ext.dirs` no
longer describe the current runtime image.

### Parent delegation

!!! info "AI-generated"

The usual `ClassLoader.loadClass` implementation asks its parent first and calls
`findClass` only if the parent cannot load the class. This prevents an application
loader from casually replacing platform classes. Custom plugin and container
loaders may use different delegation rules.

~{Java class-loader parent delegation}(<java-classloader-delegation.json> "Application and platform loaders delegate upward before a not-found request falls back toward findClass.")

Class identity includes both the binary name and the defining loader. Two loaders
can define classes with the same name that are not assignment-compatible.

Further reading: [`ClassLoader`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ClassLoader.html).
