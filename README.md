# tvbox-config

LunaTV 接口 + 饭太硬接口 → TVBox / OK影视 订阅配置，每 6 小时自动更新。

## 订阅地址

| 设备 | 文件 | 地址 |
|---|---|---|
| 电视 / 手机 | `tv-all.json`（合并版，38 CMS 站 + 饭太硬 50 站 + 5 直播） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/tv-all.json` |
| 电脑 | `tvbox-desktop-alive.json`（实测可用） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/tvbox-desktop-alive.json` |
| 电脑 | `tvbox-desktop.json`（全量） | `https://gcore.jsdelivr.net/gh/z4467/tvbox-config@main/tvbox-desktop.json` |

单看某一家的：`oktv-alive.json`（LunaTV 38 站）、`oktv.json`（69 站）、`fty.json`（饭太硬 50 站）。
镜像：域名换成 `fastly.jsdelivr.net` 或 `testingcf.jsdelivr.net`，路径不变。

> 电脑端别用 `cdn.jsdelivr.net` / `raw.githubusercontent.com`：装了 Steam++ / Watt Toolkit 时这两个域名会被写进 hosts 指向 127.0.0.1，桌面端 fetch 不认它的证书会报 `fetch failed`。

## 说明

- 电视/手机（FongMi 内核）CMS 站点写 `type: 1`，spider 站点写 `type: 3`；电脑端 TVBox Desktop 只认 `type: "cms"`，且不能跑 spider，所以 `tv-all.json` 只在电视/手机用。
- 饭太硬的接口是一张图片 + 尾部 base64，脚本自动解码。
- 更新状态看 `version.json` 的 `updated_utc / alive / fty_sites / tv_all`。

## 自动更新

`.github/workflows/update.yml`：每 6 小时跑 `python convert.py --include-adult`，有变化才提交，提交后自动刷 jsDelivr 缓存。也可在 Actions 里手动 Run workflow。
