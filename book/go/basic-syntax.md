# Basic Syntax

## Variables

!!! info "AI-generated"

```go
// Declare, then assign.
var someInt int
someInt = 42

// Short declaration with type inference. This form is valid inside functions.
someOtherInt := 42

// Grouped declarations are valid at package or function scope.
var (
    SomeIntPublic = 42 // Exported because the name starts with an uppercase letter.
    privateText   = "visible only inside this package"
)

caps := map[string]string{
    "a": "A",
    "b": "B",
    "c": "C",
}
```

## If-Else

```go
if condition {
    //
} else {
    //
}
```

## Loops

```go
for i := 0; i < 42; i++ {
    //
}

// Infinite loop, similar to `while(true)`
for {
    //
}

// Similar to `while(i < 10)`
i := 0
for i < 10 {
    //
    i++
}

// Looping over lists/arrays/slices
someList := []string{ "Apple", "Banana", "Carrot" }
for index, element := range someList {
  fmt.Printf("At %v -> %v\n", index, element)
}

// Looping over maps
someMap := map[string]string{
  "a" : "A",
  "b" : "B",
  "c" : "C",
}
for key, val := range someMap {
  fmt.Printf("For key: %v, value is: %v\n", key, val)
}
```

## Functions

```go
// returning function
func PublicSum(a int, b int) int {
  return a + b
}

// void function
func PrintHello() {
  fmt.Print("Hello")
}

// not visible outside current package
func privateSum(a int, b int) int {
  return a + b
}
```

## Structs and Objects

```go
type Person struct {
  Name  string
  Age   int
}

// usage
person := Person{
  Name: "John",
  Age:  42,
}
```

## Methods and Receivers

```go
type Person struct {
  Name string
  Age int
}

// this 'p' is called a receiver
func (p *Person) PrintName() {
  fmt.Print(p.Name)
}

func (p *Person) DoubleTheAge() int {
  return p.Age * 2
}
```

## Passing By Reference and By Value

```go
type Light struct {
  Color string
}

func ChangeLightColorByVal(light Light, newColor string) {
  light.Color = newColor
}


func ChangeLightColorByRef(light *Light, newColor string) {
  light.Color = newColor
}

func main() {
  light := Light{Color: "green"}
  ChangeLightColorByVal(light, "red")
  fmt.Println(light.Color)

  ChangeLightColorByRef(&light, "red")
  fmt.Println(light.Color)
}
```

## Interfaces

!!! info "AI-generated"

Interfaces describe behavior. A concrete type implements an interface implicitly
by providing its methods; there is no `implements` declaration.

Keep interfaces small and define them near the code that consumes them. The empty
interface `any` accepts a value of any type, but using it gives up compile-time
knowledge and should not be a default abstraction.

### Type assertions

!!! info "AI-generated"

```go
value, ok := input.(string)
if !ok {
    return fmt.Errorf("expected string, got %T", input)
}
```

Use the two-result form when a different dynamic type is expected; a failed
single-result assertion panics.

### Type switches

!!! info "AI-generated"

```go
switch value := input.(type) {
case string:
    fmt.Println("string:", value)
case int:
    fmt.Println("int:", value)
default:
    fmt.Printf("unsupported: %T\n", value)
}
```

### Compile-time contract check

!!! info "AI-generated"

```go
var _ Animal = Dog{}
```

The blank identifier turns an accidental missing method into a compile-time error.

### Composing interfaces

!!! info "AI-generated"

```go
type ReaderWriter interface {
    io.Reader
    io.Writer
}
```

### Implicit implementation

!!! info "AI-generated"

```go
type Animal interface {
  Speak() string
  Legs() int
}

// Any struct implementing/having an interface's all the methods
// it automatically implements that interface
type Dog struct{}

func (d Dog) Speak() string {
  return "Bark"
}

func (d Dog) Legs() int {
  return 4
}

var animal Animal
animal = Dog{}
fmt.Print(animal.Speak())
```
