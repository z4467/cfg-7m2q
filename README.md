# LunaTV-config → TVBox 订阅配置

把 [hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config) 里的 LunaTV 配置（明文 JSON）转换成通用 TVBox / TVBox Desktop 可直接订阅的配置，自动更新自上游仓库。

## 文件说明

| 文件 | 内容 | 站点数 |
| --- | --- | --- |
| `tvbox.json` | 全部配置合并去重（推荐用这个） | 64 |
| `LunaTV-config.json` | 仅上游 `LunaTV-config.json` | 64 |
| `jin18.json` | 仅上游 `jin18.json` | 28 |
| `jingjian.json` | 仅上游 `jingjian.json` | 47 |

## 怎么用

TVBox / TVBox Desktop 里添加订阅时，直接填对应文件的 **raw 地址**：

```
https://raw.githubusercontent.com/z4467/tvbox-config/main/tvbox.json
```

- TVBox Desktop：设置 → 配置源 → 添加 → 粘贴上面的地址
- 手机 TVBox：设置 → 配置地址 → 填入同一地址

## 说明

- 站点类型统一为苹果 CMS（`type: 3`），带搜索、快速搜索、筛选开关。
- 上游有 5 个条目不是标准苹果 CMS 接口（`优质资源`、`-美少女-`、`-黄AVZY`、`白嫖资源`、`大地资源`），TVBox 无法直接使用，已跳过。
- 配置只包含站点列表，不含直播源与解析接口（上游本身也没有）。
- 站点是否可用取决于对方接口状态，配置文件保留全部条目，可在软件「影视源」页自行禁用失效站点。

## 数据来源与更新

上游仓库：[https://github.com/hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config)

上游更新后重新跑一次转换脚本即可再生成，脚本见 [tvbox_convert.py](https://github.com/hafrey1/LunaTV-config)。

