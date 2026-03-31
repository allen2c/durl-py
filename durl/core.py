from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .parser import (
    DURLComponents,
    build_durl,
    decode_durl_data,
    parse_durl,
    serialize_durl,
)

_MISSING = object()


@dataclass(frozen=True, slots=True, init=False)
class DURL:
    _mime_type: str | None
    _parameters: Mapping[str, str]
    _is_base64: bool
    _raw_data: str

    def __init__(self, value: str) -> None:
        components = parse_durl(value)
        self._apply_components(components)

    @classmethod
    def build(
        cls,
        *,
        mime_type: str | None,
        data: bytes,
        parameters: Mapping[str, str] | None = None,
        is_base64: bool = True,
    ) -> DURL:
        components = build_durl(
            mime_type=mime_type,
            data=data,
            parameters=parameters,
            is_base64=is_base64,
        )
        return cls._from_components(components)

    @classmethod
    def _from_components(cls, components: DURLComponents) -> DURL:
        instance = cls.__new__(cls)
        instance._apply_components(components)
        return instance

    def _apply_components(self, components: DURLComponents) -> None:
        object.__setattr__(self, "_mime_type", components.mime_type)
        object.__setattr__(
            self,
            "_parameters",
            MappingProxyType(dict(components.parameters)),
        )
        object.__setattr__(self, "_is_base64", components.is_base64)
        object.__setattr__(self, "_raw_data", components.raw_data)

    @property
    def mime_type(self) -> str | None:
        return self._mime_type

    @property
    def parameters(self) -> Mapping[str, str]:
        return self._parameters

    @property
    def is_base64(self) -> bool:
        return self._is_base64

    @property
    def raw_data(self) -> str:
        return self._raw_data

    @property
    def parsed_data(self) -> str | bytes:
        return decode_durl_data(self._components)

    @property
    def value(self) -> str:
        return serialize_durl(self._components)

    def with_mime_type(self, mime_type: str | None) -> DURL:
        return self._replace(mime_type=mime_type)

    def with_parameters(self, parameters: Mapping[str, str] | None) -> DURL:
        return self._replace(parameters=parameters)

    def with_raw_data(self, raw_data: str) -> DURL:
        return self._replace(raw_data=raw_data)

    def with_data(self, data: bytes) -> DURL:
        return self.build(
            mime_type=self.mime_type,
            data=data,
            parameters=self.parameters,
            is_base64=self.is_base64,
        )

    def _replace(
        self,
        *,
        mime_type: str | None | object = _MISSING,
        parameters: Mapping[str, str] | None | object = _MISSING,
        is_base64: bool | object = _MISSING,
        raw_data: str | object = _MISSING,
    ) -> DURL:
        components = DURLComponents(
            mime_type=self.mime_type if mime_type is _MISSING else mime_type,
            parameters=tuple(
                (
                    self.parameters if parameters is _MISSING else parameters or {}
                ).items()
            ),
            is_base64=self.is_base64 if is_base64 is _MISSING else is_base64,
            raw_data=self.raw_data if raw_data is _MISSING else raw_data,
        )
        return self._from_components(components)

    @property
    def _components(self) -> DURLComponents:
        return DURLComponents(
            mime_type=self.mime_type,
            parameters=tuple(self.parameters.items()),
            is_base64=self.is_base64,
            raw_data=self.raw_data,
        )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"DURL({self.value!r})"
