# Gradle

## Incremental Builds

!!! info "AI-generated"

Gradle skips a task as `UP-TO-DATE` when its declared inputs and outputs match the
previous local execution. Custom tasks must declare every input and output;
otherwise Gradle cannot decide safely whether the work can be skipped.

```bash
./gradlew build --console=verbose
```

Incremental execution is local to the current workspace and previous task state.

## Build Cache

!!! info "AI-generated"

The build cache reuses task outputs produced by an earlier build when the task
implementation and inputs have the same cache key. Unlike an up-to-date check,
the output may come from another workspace or a shared remote cache.

```bash
./gradlew build --build-cache
```

Enable it persistently with `org.gradle.caching=true` in `gradle.properties`.
Only cache deterministic tasks whose outputs depend completely on declared inputs.

## Daemon

!!! info "AI-generated"

The Gradle Daemon is a long-lived JVM that runs builds, retains in-memory caches,
and benefits from JVM warm-up. It is enabled by default. Useful commands are:

```bash
./gradlew --status
./gradlew --stop
./gradlew build --no-daemon
```

## Scopes

!!! info "AI-generated"

Dependency configurations describe where a dependency is needed:

| Configuration | Meaning |
|---|---|
| `implementation` | Compile and runtime dependency hidden from consumers |
| `api` | Dependency exposed in a Java library's public API |
| `compileOnly` | Needed to compile but not placed on the runtime classpath |
| `runtimeOnly` | Needed only at runtime |
| `testImplementation` | Needed to compile and run tests |
| `testRuntimeOnly` | Needed only while running tests |

Prefer the narrowest configuration; it reduces accidental coupling and improves
compile avoidance.

## Configuration

!!! info "AI-generated"

Build logic is normally written in `build.gradle.kts` or `build.gradle`, while
project structure and plugin/dependency resolution policy live in
`settings.gradle.kts` or `settings.gradle`. Prefer the Gradle Wrapper (`./gradlew`)
so local and CI builds use the declared Gradle version.

### Plugins

!!! info "AI-generated"

```kotlin
plugins {
    java
    application
}
```

Plugins add tasks, conventions, and domain-specific configuration. Pin external
plugin versions in the `plugins` block or central plugin management.

### Repositories

!!! info "AI-generated"

```kotlin
repositories {
    mavenCentral()
    maven { url = uri("https://repo.example.com/releases") }
}
```

Repository order matters. Prefer authenticated HTTPS repositories with known
provenance. Avoid `mavenLocal()` in repeatable builds unless local publication is
the explicit workflow. The `jcenter()` API was deprecated in Gradle 7 and removed
in Gradle 9; use `mavenCentral()` or the repository that actually owns the
artifact.

### Dependencies

!!! info "AI-generated"

```kotlin
dependencies {
    implementation("com.google.guava:guava:33.5.0-jre")
    testImplementation(platform("org.junit:junit-bom:6.0.3"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}
```

Use dependency constraints or platforms to keep related versions aligned. Avoid
dynamic versions such as `1.+` in reproducible builds.

### Sub Projects

!!! info "AI-generated"

```kotlin
// settings.gradle.kts
rootProject.name = "shop"
include("app", "catalog", "payments")
```

Each subproject has its own tasks and dependencies. Share real build conventions
through a convention plugin; avoid a large root `allprojects` block that silently
couples unrelated modules.

## Tasks

!!! info "AI-generated"

```kotlin
tasks.register<Copy>("copyDocs") {
    from(layout.projectDirectory.dir("docs"))
    into(layout.buildDirectory.dir("docs"))
}
```

Register tasks lazily with `tasks.register`. A task should declare inputs and
outputs and should not perform work during configuration.

## Phases

!!! info "AI-generated"

Every build moves through initialization, configuration, and execution. Knowing
the boundary explains why printing or doing I/O at the top level of a build script
happens even when its tasks are not selected.

### Initialization

!!! info "AI-generated"

Gradle evaluates settings, discovers included builds and projects, and creates
the project structure.

### Configuration phase

!!! info "AI-generated"

Gradle evaluates build scripts, configures projects and tasks, and constructs the
task graph. The configuration cache can reuse this work when the build logic is
compatible.

### Execution

!!! info "AI-generated"

Gradle runs the selected task graph, honoring dependencies, ordering rules,
up-to-date checks, and cache hits.

Further reading: [Gradle build lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html)
and [performance optimizations](https://docs.gradle.org/current/userguide/gradle_optimizations.html).
