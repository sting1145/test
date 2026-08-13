# UI Automation Cashier 鈥?鐔婄尗鎺屾煖鏀堕摱鍙?
鍩轰簬 **Python + Playwright** 鐨勬敹閾跺彴 UI 鑷姩鍖栭」鐩紝閽堝鏈湴鏀堕摱鍙扮▼搴忥紙`http://127.0.0.1:9981`锛夎璁°€?
## 鐜瑕佹眰

- Python 3.10+
- 鏀堕摱鍙扮▼搴忓凡鍚姩锛堢獥鍙ｆ爣棰橈細鏀堕摱鍙帮級

## 蹇€熷紑濮?
```bash
cd ui-automation-cashier
setup.bat
.venv\Scripts\activate
pytest
```

鎴栨墜鍔ㄥ畨瑁咃細

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chrome
copy .env.example .env
pytest
```

鏈」鐩粯璁や娇鐢?**鏈満宸插畨瑁呯殑 Google Chrome**锛坄BROWSER_CHANNEL=chrome`锛夛紝涓€鑸笉闇€瑕佷笅杞?Playwright 鑷甫鐨?Chromium銆?
鑻ユ湰鏈烘病鏈?Chrome锛屽彲鏀逛负 Edge锛歚BROWSER_CHANNEL=msedge`锛屽苟鎵ц `python -m playwright install msedge`銆?
鑻ヤ粛鎶ユ祻瑙堝櫒涓嶅瓨鍦紝鍐嶆墽琛岋細

```bash
python -m playwright install chromium
```

## 閰嶇疆

鍦?`.env` 涓厤缃祴璇曡处鍙凤細

```env
CASHIER_BASE_URL=http://127.0.0.1:9981
CASHIER_SERVER_IP=172.16.99.70
CASHIER_ACCOUNT=xmzg_yjb001
CASHIER_PASSWORD=123456
HEADLESS=true
```

## 椤圭洰缁撴瀯

```
pages/
  cashier_login_page.py   # 鏀堕摱鍙扮櫥褰曢〉 Page Object
utils/
  cashier_auth.py         # WebSocket 鎻℃墜銆佺櫥褰?API銆佽矾鐢辨嫤鎴?tests/
  test_cashier_login.py   # 鐧诲綍鐢ㄤ緥锛? 鏉★級
```

## 娴嬭瘯鐢ㄤ緥

| 鍒嗙被 | 鐢ㄤ緥 |
|------|------|
| 椤甸潰鍔犺浇 | 搴旀纭姞杞界櫥褰曢〉骞跺睍绀烘牳蹇冨厓绱?|
| 琛ㄥ崟鏍￠獙 | IP/璐﹀彿/瀵嗙爜涓虹┖绛?3 鏉℃牎楠?|
| 姝ｅ悜鐧诲綍 | 浣跨敤鏈夋晥 IP銆佽处鍙枫€佸瘑鐮佺櫥褰曟垚鍔?|

## 涓€閿繍琛岋紙鎺ㄨ崘锛?
**鍙屽嚮**椤圭洰鏍圭洰褰曚笅鐨勶細

```
run_tests_and_report.bat
```

浼氳嚜鍔細杩愯娴嬭瘯 鈫?鐢熸垚 Allure 鎶ュ憡 鈫?鎵撳紑 HTML 鎶ュ憡銆?
棣栨浣跨敤鍓嶅弻鍑?`setup.bat` 瀹夎渚濊禆銆?
## 娴嬭瘯鐢ㄤ緥锛? 鏉★級

| 鍒嗙被 | 鐢ㄤ緥 |
|------|------|
| 椤甸潰鍔犺浇 | 搴旀纭姞杞界櫥褰曢〉骞跺睍绀烘牳蹇冨厓绱?|
| 琛ㄥ崟鏍￠獙 | IP/璐﹀彿/瀵嗙爜涓虹┖绛?3 鏉℃牎楠?|
| 姝ｅ悜鐧诲綍 | 瀵嗙爜 `123456` 鐧诲綍鎴愬姛 |
| 璐熷悜鐧诲綍 | 瀵嗙爜 `1234567` 鐧诲綍澶辫触 |

## 鎶ュ憡璇存槑

- 鏈€鏂版姤鍛婏細`reports/latest-report.html`锛堝弻鍑绘墦寮€锛?- 鍘嗗彶绱㈠紩锛歚reports/index.html`
- 澶辫触鐢ㄤ緥鑷姩鎴浘锛岄檮鍦?Allure 鎶ュ憡涓?
## 鎵嬪姩杩愯

```bash
# 杩愯鍏ㄩ儴鐢ㄤ緥
pytest

# 鍙窇姝ｅ悜鐧诲綍
pytest -m positive

# 鏈夌晫闈㈣皟璇?set HEADLESS=false
pytest -m positive

# 鍙窇鐧诲綍鐩稿叧
pytest -m login
```

## 鎶€鏈鏄?
鏀堕摱鍙版槸 CEF 鍐呭祵 Web 搴旂敤銆傜櫥褰曟祦绋嬩緷璧栵細

1. WebSocket 鑾峰彇 `token/nid`锛坄172.16.99.70:16510`锛?2. 浜戠鐧诲綍 API
3. 椤甸潰鍐?`to_browser` 鎻℃墜

娴嬭瘯閫氳繃 Playwright 鎷︽埅鐧诲綍 API銆佹ā鎷熸彙鎵嬶紝骞舵牎楠?`localStorage.userinfo` 鍐欏叆鎴愬姛銆?
## 涓轰粈涔堢敤 Playwright 鑰屼笉鏄?Selenium

鏈」鐩€夌敤 **Playwright**锛屽洜涓猴細

- 鍘熺敓鏀寔 `page.route()` 鎷︽埅璇锋眰锛堢粫杩囨祻瑙堝櫒 CORS锛?- 涓庣幇鏈?TypeScript 鐗堟敹閾跺彴鑷姩鍖栨柟妗堜竴鑷?- 瀵规湰鍦?`127.0.0.1:9981` 椤甸潰鏀寔鏇村ソ

濡傞渶 Selenium 鐗堟湰锛屽彲灏?Page Object 涓殑瀹氫綅鍣ㄨ縼绉诲埌 `selenium.webdriver`锛屼絾鐧诲綍 API 鎷︽埅闇€鏀圭敤鍏朵粬鏂瑰紡锛堝浠ｇ悊鎴栫洿鎺ュ湪椤甸潰娉ㄥ叆鍝嶅簲锛夈€?
