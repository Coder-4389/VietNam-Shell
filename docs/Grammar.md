## **define functions**
```
func name_of_function(param_name1, param_name2) {
    ...
}
```

* **You only use return in a function.**

## **define spaces**
```
space name_of_space{
    ...
}
```
* **In the space you can't use object in parent space.**

## **define a struct**
```
struct name_of_struct{
    name: type_value,
    ...
}
```

* **shouldn't named it's like a space.**

## **assign a variable**
```
set name_of_variable = value_of_variable
```

or 

```
const name_of_const = value_of_const
```

## **branching code**
```
if condition {
    ...
} elif condition {
    ...
} else {
    ...
}
```

* **don't write code between 2 if's block**

## **loop code**
```
while condition {
    ...
}
```

or

```
for variable_name in iterable {
    ...
}
```

## **use file of code**
```
use name_of_file;
``` 

or 

```
use name_of_file as title_of_file;
```

* **The lang check file of code in 2 path are**
    * `{app}/Lib/{file_want_to_use}`
    * `{file_dir}/{file_want_to_use}`

* **This function in beta version.**
