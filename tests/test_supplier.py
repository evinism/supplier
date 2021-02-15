import pytest
from supplier import Supplier, supply


def test_supplier_supplies():
    blah_supplier = Supplier("blah")
    with blah_supplier.use("hello"):
        assert blah_supplier.get() == "hello"


def test_supplier_resets():
    blah_supplier = Supplier("blah")

    with blah_supplier.use("hello"):
        pass
    with pytest.raises(Exception):
        blah_supplier.get()


def test_supplier_can_be_used_multiple_times():
    foo_supplier = Supplier("foo")

    with foo_supplier.use("hello"):
        assert foo_supplier.get() == "hello"

    with foo_supplier.use("hi"):
        assert foo_supplier.get() == "hi"


def test_supply_decorator():
    foo_supplier = Supplier("foo")

    @supply(foo_supplier)
    def has_arg(hello):
        assert hello == "hello"

    with foo_supplier.use("hello"):
        has_arg()


def test_supply_decorator_with_arg():
    foo_supplier = Supplier("foo")

    @supply(foo_supplier)
    def has_arg(hello, there):
        assert hello == "hello"
        assert there == "there"

    with foo_supplier.use("hello"):
        has_arg("there")


def test_supply_decorator_multiple_suppliers():
    foo_supplier = Supplier("foo")
    bar_supplier = Supplier("bar")

    @supply(foo_supplier, bar_supplier)
    def has_arg(hello, there, friend):
        assert hello == "hello"
        assert there == "there"
        assert friend == "friend"

    with foo_supplier.use("hello"), bar_supplier.use("there"):
        has_arg("friend")


def test_supply_decorator_optional_args():
    foo_supplier = Supplier("foo")

    @supply(foo_supplier)
    def has_arg(hello, there, pal="pal"):
        assert hello == "hello"
        assert there == "there"
        assert pal == "pal"

    with foo_supplier.use("hello"):
        has_arg("there")
        has_arg("there", "pal")


def test_supply_decorator_in_classes():
    foo_supplier = Supplier("foo")
    bar_supplier = Supplier("bar")

    class Baz:
        name = "baz"

        @supply(foo_supplier, bar_supplier)
        def bound_method(self, hello, there, cool, house):
            assert hello == "hello"
            assert there == "there"
            assert self.name == "baz"
            assert cool == "cool"
            assert house == "house"

    baz = Baz()

    with foo_supplier.use("hello"), bar_supplier.use("there"):
        baz.bound_method("cool", "house")
