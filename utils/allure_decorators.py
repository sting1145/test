import allure

from utils.test_case_meta import CASE_BY_METHOD

_SEVERITY_MAP = {
  "P0": allure.severity_level.CRITICAL,
  "P1": allure.severity_level.NORMAL,
  "P2": allure.severity_level.MINOR,
}


def _build_description(meta: dict) -> str:
  return (
    f"前置条件：\n{meta['precondition']}\n\n"
    f"测试数据：\n{meta['data']}\n\n"
    f"测试步骤：\n{meta['steps']}\n\n"
    f"预期结果：\n{meta['expected']}"
  )


def testcase(method_name: str | None = None):
  """为测试方法绑定 Allure 中文标题、前置条件与测试数据。"""

  def decorator(func):
    key = method_name or func.__name__
    meta = CASE_BY_METHOD.get(key)
    if not meta:
      return func

    if func.__name__ != meta["method"]:
      raise ValueError(f"{key} is mapped to {meta['method']}, not {func.__name__}")

    func = allure.title(meta["title"])(func)
    func = allure.description(_build_description(meta))(func)
    return func

  return decorator


def apply_chinese_title(func):
  return testcase()(func)
