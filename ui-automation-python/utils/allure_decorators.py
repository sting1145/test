import functools
import inspect

import allure

from utils.allure_report_content import (
  API_METHOD_RUNTIME_BUILDERS,
  API_RUNTIME_DATA_RESOLVERS,
  UI_METHOD_RUNTIME_BUILDERS,
  build_allure_description,
  inject_bound_test_constants,
  resolve_runtime_data,
)
from utils.test_case_meta import CASE_BY_ID, allure_display_title

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


def testcase(case_id: str):
  """按用例编号为测试方法绑定 Allure 中文标题与描述。"""

  matched = CASE_BY_ID.get(case_id)
  if not matched:
    raise ValueError(f"Unknown testcase id: {case_id}")

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
        resolvers={},
        method_builders=UI_METHOD_RUNTIME_BUILDERS,
      )
      allure.dynamic.description(
        build_allure_description(matched, runtime_data=runtime_data)
      )
      if "payload" in bound_args:
        allure.dynamic.parameter("payload", bound_args["payload"])
      return func(*args, **kwargs)

    wrapper = allure.title(allure_display_title(matched))(wrapper)
    wrapper = allure.severity(
      _SEVERITY_MAP.get(matched["priority"], allure.severity_level.NORMAL)
    )(wrapper)
    return wrapper

  return decorator
