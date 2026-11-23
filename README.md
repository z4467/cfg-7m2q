# LunaTV-config → TVBox 订阅配置

把 [hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config) 里的 LunaTV 配置（明文 JSON）转换成通用 TVBox / TVBox Desktop 可直接订阅的配置，自动更新自上游仓库。

## 文件说明

| 文件 | 内容 | 站点数 |
| --- | --- | --- |
| `tvbox.json` | 全部配置合并去重（推荐用这个） | 64 |
| `oktv.json` | OK影视 / 影视仓电视端专用，字段精简、只留点播 | 64 |
| `LunaTV-config.json` | 仅上游 `LunaTV-config.json` | 64 |
| `jin18.json` | 仅上游 `jin18.json` | 28 |
| `jingjian.json` | 仅上游 `jingjian.json` | 47 |

## 怎么用

TVBox / TVBox Desktop 里添加订阅时，填下面任意一个地址（推荐第 1 个，打不开就用第 2、3 个）：

| 线路 | 地址 |
| --- | --- |
| 1. GitHub raw（直连） | `https://raw.githubusercontent.com/z4467/tvbox-config/main/tvbox.json` |
| 2. jsDelivr 镜像（国内一般更快） | `https://cdn.jsdelivr.net/gh/z4467/tvbox-config@main/tvbox.json` |
| 3. ghfast 代理 | `https://ghfast.top/https://raw.githubusercontent.com/z4467/tvbox-config/main/tvbox.json` |

- TVBox Desktop：设置 → 配置源 → 添加 → 粘贴上面的地址
- 手机 TVBox：设置 → 配置地址 → 填入同一地址
- OK影视 / 影视仓（电视端）：设置 → 点播 → 粘贴 `oktv.json` 的地址 → 确定 → 回首页刷新

OK影视用这条（和其他文件一样可换 jsDelivr / ghfast 前缀）：

```
https://raw.githubusercontent.com/z4467/tvbox-config/main/oktv.json
```

> jsDelivr 走 CDN 缓存，通常 12 小时左右同步一次；刚更新完内容想马上生效，先用第 1 条 raw 地址，或者把 `@main` 换成 `@<commit 哈希>`。

其他文件同理，把末尾的 `tvbox.json` 换成 `LunaTV-config.json`、`jin18.json`、`jingjian.json` 即可。

## 说明

- 站点类型统一为苹果 CMS（`type: 3`），带搜索、快速搜索、筛选开关。
- 上游有 5 个条目不是标准苹果 CMS 接口（`优质资源`、`-美少女-`、`-黄AVZY`、`白嫖资源`、`大地资源`），TVBox 无法直接使用，已跳过。
- 配置只包含站点列表，不含直播源与解析接口（上游本身也没有）。
- 站点是否可用取决于对方接口状态，配置文件保留全部条目，可在软件「影视源」页自行禁用失效站点。

## 数据来源与更新

上游仓库：[https://github.com/hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config)

上游更新后重新跑一次转换脚本即可再生成，脚本见 [tvbox_convert.py](https://github.com/hafrey1/LunaTV-config)。

