"""Compatibility shim: import web automation helpers from behave_zap."""

from behave_zap import (
    BaseElement,
    Button,
    ConfigAdapter,
    InputText,
    PageObject,
    Text,
    create_driver,
    get_current_context,
    set_current_context,
)

__all__ = [
    "ConfigAdapter",
    "create_driver",
    "set_current_context",
    "get_current_context",
    "BaseElement",
    "Button",
    "InputText",
    "Text",
    "PageObject",
]
