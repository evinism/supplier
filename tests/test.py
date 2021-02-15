import pytest
from providers import Provider, provide


def test_provider_provides():
    blah_provider = Provider("blah")

    with blah_provider.use("hello"):
        assert blah_provider.get() == "hello"


def test_provider_resets():
    blah_provider = Provider("blah")

    with blah_provider.use("hello"):
        pass
    with pytest.raises(Exception):
        blah_provider.get()


def test_provider_can_be_used_multiple_times():
    foo_provider = Provider("foo")

    with foo_provider.use("hello"):
        assert foo_provider.get() == "hello"

    with foo_provider.use("hi"):
        assert foo_provider.get() == "hi"


def test_provide_decorator():
    foo_provider = Provider("foo")

    @provide(foo_provider)
    def has_arg(hello):
        assert hello == "hello"

    with foo_provider.use("hello"):
        has_arg()


def test_provide_decorator_with_arg():
    foo_provider = Provider("foo")

    @provide(foo_provider)
    def has_arg(hello, there):
        assert hello == "hello"
        assert there == "there"

    with foo_provider.use("hello"):
        has_arg("there")


def test_provide_decorator_multiple_providers():
    foo_provider = Provider("foo")
    bar_provider = Provider("bar")

    @provide(foo_provider, bar_provider)
    def has_arg(hello, there, friend):
        assert hello == "hello"
        assert there == "there"
        assert friend == "friend"

    with foo_provider.use("hello"), bar_provider.use("there"):
        has_arg("friend")


def test_provide_decorator_optional_args():
    foo_provider = Provider("foo")

    @provide(foo_provider)
    def has_arg(hello, there, pal="pal"):
        assert hello == "hello"
        assert there == "there"
        assert pal == "pal"

    with foo_provider.use("hello"):
        has_arg("there")
        has_arg("there", "pal")


def test_provide_decorator_in_classes():
    foo_provider = Provider("foo")
    bar_provider = Provider("bar")

    class Baz:
        name = "baz"

        @provide(foo_provider, bar_provider)
        def bound_method(self, hello, there, cool, house):
            assert hello == "hello"
            assert there == "there"
            assert self.name == "baz"
            assert cool == "cool"
            assert house == "house"

    baz = Baz()

    with foo_provider.use("hello"), bar_provider.use("there"):
        baz.bound_method("cool", "house")
