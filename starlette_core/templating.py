import typing

from starlette import templating
from starlette.datastructures import QueryParams

from .config import config

try:
    import jinja2
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore


class Jinja2Templates(templating.Jinja2Templates):
    def __init__(self, loader: "jinja2.BaseLoader") -> None:
        assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
        self.env = self.get_environment(loader)

    def get_environment(self, loader: "jinja2.BaseLoader") -> "jinja2.Environment":
        def url_params_update(init: QueryParams, **new: typing.Any) -> QueryParams:
            values = dict(init)
            values.update(new)
            return QueryParams(**values)

        @jinja2.contextfunction
        def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
            request = context["request"]
            return request.url_for(name, **path_params)

        env = jinja2.Environment(
            extensions=config.jinja2_extensions, loader=loader, autoescape=True
        )
        env.globals["url_params_update"] = url_params_update
        env.globals["url_for"] = url_for

        return env
