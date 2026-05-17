from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from behave_zap import create_default_runner
from behave_zap import ConfigAdapter, create_driver, set_current_context


RUNNER = create_default_runner(
    config_path="conf/properties.cfg",
    config_adapter_cls=ConfigAdapter,
    create_driver_fn=create_driver,
    set_current_context_fn=set_current_context,
)


def before_all(context):
    RUNNER.before_all(context)


def before_feature(context, feature):
    RUNNER.before_feature(context, feature)


def before_scenario(context, scenario):
    RUNNER.before_scenario(context, scenario)


def after_scenario(context, scenario):
    RUNNER.after_scenario(context, scenario)


def after_feature(context, feature):
    RUNNER.after_feature(context, feature)


def after_all(context):
    RUNNER.after_all(context)
