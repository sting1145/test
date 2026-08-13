"""登录表单 SQL 注入探测 payload（UI 黑盒测试用）。"""

# 经典永真 / 注释绕过
ACCOUNT_PAYLOADS = [
  "' OR '1'='1",
  "' OR 1=1--",
  "admin'--",
  "' OR 'a'='a",
  "') OR ('1'='1",
]

# 联合查询 / 堆叠（探测是否被原样拼接进 SQL）
ACCOUNT_ADVANCED_PAYLOADS = [
  "' UNION SELECT NULL,NULL--",
  "1' AND '1'='2",
]

PASSWORD_PAYLOADS = [
  "' OR '1'='1",
  "' OR 1=1#",
  "') OR ('1'='1",
]

ALL_ACCOUNT_PAYLOADS = ACCOUNT_PAYLOADS + ACCOUNT_ADVANCED_PAYLOADS
