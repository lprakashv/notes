# Basic Syntax

## Variables

```go
// Define and assign
var someInt int
someInt = 42

// combines define and assign => type inference
someOtherInt := 42

// Multiple variables declaration
var a, b, c, d int
var e, f, g, h string

// Multiple variables with assignment
var (
  x = 42
  y = 54
  z = "some string"
  caps = map[string]string{
    "a" : "A",
    "b" : "B",
    "c" : "C",
  }
)


// Capital case to make it visible outside current package
SomeIntPublic := 42
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
  fmt.Print("At %v -> %v\n", index, element)
}

// Looping over maps
someMap := map[string]string{
  "a" : "A",
  "b" : "B",
  "c" : "C",
}
for key, val := range someMap {
  fmt.Print("For key: %v, value is: %v\n", key, val)
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

Interface as a "God" type:

```go
```

Type assertions:

```go
```

Type assertions with type-switch (runtime):

```go
```

Compile time type contract:

```go
```

Composing types using `interface{ interface{ SomeFunc any } }` or with named one `interface{ Contract1, Contract2 }`:

```go
```

```go
type Animal interface {
  Speak() string
  Legs() int
}

// Any struct implementing/having an interface's all the methods
// it automatically implements that interface
type Dog struct {

}
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
