# tvbox-config

把 `hafrey1/LunaTV-config` 和 `饭太硬` 的接口自动转换成 TVBox / OK影视 可订阅的配置，每 6 小时自动更新一次。

## 订阅地址

| 设备 | 文件 | 地址 |
|---|---|---|
| 电视 / 手机 | `oktv-alive.json`（实测可用） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/oktv-alive.json` |
| 电视 / 手机 | `oktv.json`（全量） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/oktv.json` |
| 电脑 | `tvbox-desktop-alive.json`（实测可用） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/tvbox-desktop-alive.json` |
| 电脑 | `tvbox-desktop.json`（全量） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/tvbox-desktop.json` |
| 电视 / 手机 | `fty.json`（饭太硬，纯 spider 源） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/fty.json` |

镜像：把域名换成 `https://fastly.jsdelivr.net` 或 `https://testingcf.jsdelivr.net` 即可，路径不变。

> 电脑端别用 `cdn.jsdelivr.net` / `raw.githubusercontent.com`：装了 Steam++ / Watt Toolkit 时这两个域名会被写进 hosts 指向 127.0.0.1，桌面端 fetch 不认它的证书会报 `fetch failed`。

## 说明

- 电视/手机（FongMi 内核）的 CMS 站点写 `type: 1`；电脑端 TVBox Desktop 要用 `type: "cms"`。写反会出现「站点有、点进去空白」或订阅直接报错。
- `fty.json` 是饭太硬那张「图片 + 尾部 base64」的接口解码出来的，50 个站全是 spider 源，依赖伪装成 jpg 的 jar，只能在电视/手机上跑。
- 更新状态看 `version.json` 的 `updated_utc / total / alive / fty_sites`。

## 自动更新

`.github/workflows/update.yml`：每 6 小时跑 `python convert.py --include-adult`，有变化才提交，提交后自动刷 jsDelivr 缓存。也可以在 Actions 里手动 Run workflow。

本地跑：`python convert.py --include-adult`（加 `--no-probe` 跳过实测）。
