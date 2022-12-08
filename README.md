# DSL Parser

A simple proof-of-concept parser that parses, transforms and then parses the transformed value. Useful for implementing custom
[DSL](https://en.wikipedia.org/wiki/Domain-specific_language)s for configurations etc.

Uses [**Lark**](https://github.com/lark-parser/lark) for the implementation.

## Examples
> 
> Format of examples
> ```
> # input -> parsed output
> # Tree representation of the parsed input.
> ```
> See [custom_function.py](./custom_function.py) for custom function implementations.

```
${ env(SHELL) } -> /bin/zsh
function
  function_name env
  args  SHELL

${env(SHELL, SHOULD_NOT_PRINT)} -> /bin/zsh
function
  function_name env
  args
    SHELL
    SHOULD_NOT_PRINT

${env(NOTHING, DEFAULT_VALUE_1)} -> DEFAULT_VALUE_1
function
  function_name env
  args
    NOTHING
    DEFAULT_VALUE_1

${ env(NOTHING,DEFAULT_VALUE_2 )} -> DEFAULT_VALUE_2
function
  function_name env
  args
    NOTHING
    DEFAULT_VALUE_2

${ ref(disk/created/properties) } -> disk.created.properties
function
  function_name ref
  args  disk/created/properties

${ref(disk/created/properties/name)} -> disk.created.properties.name
function
  function_name ref
  args  disk/created/properties/name

${ref(disk/created/properties/size )} -> disk.created.properties.size
function
  function_name ref
  args  disk/created/properties/size

${ ref( disk/created/properties/type ) } -> disk.created.properties.type
function
  function_name ref
  args  disk/created/properties/type

disk/created/properties -> disk.created.properties
reference
  module_name   disk
  resource_name created
  properties    properties

disk/created/properties/name -> disk.created.properties.name
reference
  module_name   disk
  resource_name created
  properties
    properties
    name

disk/created/properties/size -> disk.created.properties.size
reference
  module_name   disk
  resource_name created
  properties
    properties
    size

disk / created/ properties/ type -> disk.created.properties.type
reference
  module_name   disk
  resource_name created
  properties
    properties
    type
```
