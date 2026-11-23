# tvbox-config

把 [`hafrey1/LunaTV-config`](https://github.com/hafrey1/LunaTV-config) 自动转换成
**OK影视 / FongMi 内核 / TVBox** 可直接订阅的配置，每 6 小时自动同步一次。

## 订阅地址

| 文件 | 说明 | 地址 |
|---|---|---|
| `tvbox-alive.json` | **电脑端 TVBox Desktop**，实测可用站（type=3） | `https://raw.githubusercontent.com/z4467/tvbox-config/main/tvbox-alive.json` |
| `tvbox.json` | 电脑端 TVBox Desktop，全量（type=3） | `https://raw.githubusercontent.com/z4467/tvbox-config/main/tvbox.json` |
| `oktv-alive.json` | **电视/手机（OK影视·影视仓）**，实测可用站（type=1） | `https://raw.githubusercontent.com/z4467/tvbox-config/main/oktv-alive.json` |
| `oktv.json` | 电视/手机，全量 | `https://raw.githubusercontent.com/z4467/tvbox-config/main/oktv.json` |
| `oktv-safe-alive.json` | 不含成人源，实测可用 | `https://raw.githubusercontent.com/z4467/tvbox-config/main/oktv-safe-alive.json` |
| `oktv-safe.json` | 不含成人源，全量 | `https://raw.githubusercontent.com/z4467/tvbox-config/main/oktv-safe.json` |
| jsDelivr 镜像 | raw 打不开时用 | `https://cdn.jsdelivr.net/gh/z4467/tvbox-config@main/oktv-alive.json` |
| ghfast 镜像 | 备选 | `https://ghfast.top/https://raw.githubusercontent.com/z4467/tvbox-config/main/oktv-alive.json` |

> **`type` 在两类 App 里含义不一样**：FongMi 内核（OK影视/影视仓）把 CMS 采集接口定为 `1`，
> 写成 `3` 会被当成 spider 源 → 站点能列出但内容空白；电脑端 TVBox Desktop 反过来，
> CMS 必须写 `3`，写 `1` 会被当成 HTML 规则站 → 订阅直接报错。所以两类设备要用不同的文件。

> jsDelivr 对 `@main` 有缓存。刚更新完想立刻看到新内容，可以用固定 commit 链接，
> 或者等几分钟（工作流会自动请求 jsDelivr 刷新缓存）。

## 自动更新

`.github/workflows/update.yml`：

- 每 6 小时（UTC `17 */6 * * *`）自动运行，拉取上游三个源重新转换；
- 有变化才提交（commit message 带 `[skip ci]`，不会形成循环）；
- 提交后自动调用 `purge.jsdelivr.net` 刷新 CDN 缓存；
- 也可以在仓库 **Actions → Auto Update TV Config → Run workflow** 手动触发。

状态看板：`version.json` 里有 `updated_utc / total / alive`，用来确认是否真的更新过。

## 转换规则（`convert.py`）

1. 读取上游 `LunaTV-config.json`、`jin18.json`、`jingjian.json`，兼容 `api_site` 与 `sites` 两种格式；
2. 按 `api` 去重，跳过 `csp_` 这类需要 spider 的源（只保留 http/https 采集接口）；
3. **`type` 一律写 1**：CMS JSON 采集接口。写成 3 会被当成 spider 源，症状是"站点有、点进去空白、搜不出东西"；
4. 自动更新默认**保留**成人源（`--include-adult`）；同时额外生成一份不含 🔞 的 `oktv-safe*.json`；
5. 上游 `_comment` 里写"无法搜索/403"等，自动关闭该站的 `searchable`；
6. 逐个实测 `?ac=detail&pg=1` 是否能返回片单，能返回的才进 `*-alive.json`；
7. 输出统一带 `flags`、`doh`（阿里/腾讯 DoH，电视端解析更稳）。

## 本地手动跑

```bash
python convert.py --include-adult   # 与自动更新一致：含成人源 + 实测存活
python convert.py                   # 不含成人源
python convert.py --no-probe        # 不实测，速度快
```

产物：`oktv.json`、`oktv-alive.json`、`tvbox.json`、`oktv-safe.json`、`oktv-safe-alive.json`、`version.json`。
