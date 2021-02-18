# Supplier: Python library for passing values deeply, easily!

Have you ever had a piece of configuration that you want access to deeply in a function, but you don't want to always have to pass it, and you don't want to have a singleton?

This is for you!

### Example

Here's a basic before/after for passing variables deeply.

Before:
```py
def outer_function(config):
  middle_function(config)

def middle_function(config):
  inner_function(config)
  
def inner_function(config):
  # To supply config here, we have to manually pass the config through 2 layers of function calls!
  do_something_based_on(config)
  
outer_function(Config())
```

After:
```py
from supplier import Supplier, supply
config_supplier = Supplier('config')

def outer_function():
  middle_function()

def middle_function()
  inner_function()
  
@supply(config_supplier)
def inner_function(config):
  # No longer have to manually pass the config through 2 layers!
  do_something_based_on(config)

with config_supplier.use(Config()):
  outer_function()
```

This is essentially python contextvars + contextlib in one convenient package

## @supply allows multiple function arguments

Supplier prepends the function's arguments with the supplied value.

```py
@supply(foo_supplier)
def func_with_args(foo, arg1, arg2):
  print(foo, arg1, arg2)

with foo_supplier.use("foo"):
  func_with_args("arg1", "arg2")
```

## @supply works with multiple suppliers

You can supply multiple variables simultaneously.

```py
@supply(foo_supplier, bar_supplier)
def doubly_provided_func(foo, bar, arg):
  print(foo, bar, arg)

with foo_supplier.use("foo"), bar_supplier.use("bar"):
  doubly_provided_func("arg")
```

## @supply keeps `self` argument in the same place.

When using supply to decorate class method, supply keeps the `self` argument in the same place, for ease of use.

```py
class A(Printer):
  @supply(foo_supplier):
  def print_foo(self, foo):
    self.print(foo)
```

