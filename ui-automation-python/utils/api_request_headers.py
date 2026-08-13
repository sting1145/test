from utils.config import Config


def api_referer_for(path: str) -> str:
  normalized = path.split("?", 1)[0]
  user_path = Config.API_CURRENT_USER_PATH.split("?", 1)[0]
  list_path = Config.API_LIST_PATH.split("?", 1)[0]

  if user_path and normalized == user_path:
    return Config.API_USER_REFERER
  if list_path and normalized == list_path:
    return Config.API_LIST_REFERER
  return Config.API_REFERER
