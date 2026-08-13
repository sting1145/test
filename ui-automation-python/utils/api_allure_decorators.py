import functools
import inspect

import allure

from utils.allure_report_content import (
  API_METHOD_RUNTIME_BUILDERS,
  API_RUNTIME_DATA_RESOLVERS,
  build_allure_description,
  inject_bound_test_constants,
  resolve_runtime_data,
)
from utils.api_test_case_meta import API_CASE_BY_ID, api_allure_display_title

_SEVERITY_MAP = {
  "P0": allure.severity_level.CRITICAL,
  "P1": allure.severity_level.NORMAL,
  "P2": allure.severity_level.MINOR,
}


def _bind_call_args(func, args, kwargs):
  signature = inspect.signature(func)
  bound = signature.bind_partial(*args, **kwargs)
  bound.apply_defaults()
  return bound.arguments


def api_testcase(case_id: str):
  matched = API_CASE_BY_ID.get(case_id)
  if not matched:
    raise ValueError(f"Unknown API testcase id: {case_id}")

  def decorator(func):
    if func.__name__ != matched["method"]:
      raise ValueError(
        f"{case_id} is mapped to {matched['method']}, not {func.__name__}"
      )

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      bound_args = _bind_call_args(func, args, kwargs)
      test_instance = bound_args.get("self")
      runtime_data = resolve_runtime_data(
        case_id=case_id,
        method_name=func.__name__,
        bound_args=inject_bound_test_constants(bound_args, test_instance),
        resolvers=API_RUNTIME_DATA_RESOLVERS,
        method_builders=API_METHOD_RUNTIME_BUILDERS,
      )
      allure.dynamic.description(
        build_allure_description(matched, runtime_data=runtime_data)
      )
      if "payload" in bound_args:
        allure.dynamic.parameter("payload", bound_args["payload"])
      return func(*args, **kwargs)

    wrapper = allure.title(api_allure_display_title(matched))(wrapper)
    wrapper = allure.severity(
      _SEVERITY_MAP.get(matched["priority"], allure.severity_level.NORMAL)
    )(wrapper)
    return wrapper

  return decorator
