#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 hafrey1/LunaTV-config 的三个源（LunaTV-config.json / jin18.json / jingjian.json）
转换成 OK影视(FongMi 内核)/TVBox 可直接订阅的配置。

关键点：CMS 采集接口必须用 "type": 1（JSON 采集），写成 3 会被当成 spider 源，
表现为"站点有、进去空白、搜不出东西"。

输出：
  oktv.json        —— 全部正规站点（默认排除名字带 🔞 的成人源）
  oktv-alive.json  —— 只保留实测能返回片单的站点
  tvbox.json       —— 与 oktv.json 同内容（兼容 TVBox Desktop）
  version.json     —— 本次更新时间/数量，方便核对有没有真的更新

用法：
  python convert.py                 # 默认排除成人源、实测存活
  python convert.py --no-probe      # 不实测，速度快
  python convert.py --include-adult # 保留成人源（默认不保留）
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "okhttp/3.8.1"}
SOURCES = [
    "https://raw.githubusercontent.com/hafrey1/LunaTV-config/main/LunaTV-config.json",
    "https://raw.githubusercontent.com/hafrey1/LunaTV-config/main/jin18.json",
    "https://raw.githubusercontent.com/hafrey1/LunaTV-config/main/jingjian.json",
]
MIRRORS = [
    "https://cdn.jsdelivr.net/gh/hafrey1/LunaTV-config@main/{}",
    "https://ghfast.top/https://raw.githubusercontent.com/hafrey1/LunaTV-config/main/{}",
]
FLAGS = ["youku", "qq", "iqiyi", "qiyi", "letv", "sohu", "tudou", "pptv",
         "mgtv", "wasu", "bilibili", "renren", "xigua"]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def http_get(url, timeout=20, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # 网络抖动/镜像失败都重试
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"下载失败 {url}: {last}")


SEARCH_BLOCK = ["无法搜索", "暂不支持搜索", "无搜索结果", "污染搜索结果", "禁止搜索结果"]


def load_source(url):
    """返回 [(站点dict)]，兼容两种上游格式：
    1) LunaTV 原生：{"cache_time":..., "api_site": {"域名": {name, api, detail, _comment}}}
    2) TVBox 风格：{"name":..., "sites": [...]}
    """
    name = url.rsplit("/", 1)[-1]
    try:
        raw = http_get(url)
    except Exception as e:
        print(f"  ! 直链失败 {name}: {str(e)[:60]}，尝试镜像")
        for m in MIRRORS:
            try:
                raw = http_get(m.format(name))
                print(f"  ✓ 镜像成功 {name}")
                break
            except Exception:
                continue
        else:
            print(f"  × 放弃 {name}")
            return []
    i = raw.find("{")
    if i < 0:
        return []
    data = json.loads(raw[i:])

    api_site = data.get("api_site") or data.get("apiSite")
    if isinstance(api_site, dict) and api_site:
        out = []
        for domain, s in api_site.items():
            if not isinstance(s, dict):
                continue
            comment = str(s.get("_comment") or "")
            searchable = 0 if any(w in comment for w in SEARCH_BLOCK) else 1
            out.append({
                "key": "csp_" + str(domain).lower().replace(".", "_").replace("-", "_"),
                "name": s.get("name") or domain,
                "api": str(s.get("api") or "").strip(),
                "detail": s.get("detail"),
                "searchable": searchable,
                "quickSearch": searchable,
            })
        return out
    return data.get("sites") or []


def collect(include_adult):
    sites, seen = [], set()
    for url in SOURCES:
        print(f"读取 {url}")
        for s in load_source(url):
            api = str(s.get("api") or "").strip()
            name = s.get("name") or ""
            if not api.lower().startswith("http"):
                continue  # 跳过 csp_/spider 型
            if api in seen:
                continue
            if not include_adult and "🔞" in name:
                continue
            seen.add(api)
            item = {
                "key": s.get("key") or f"src{len(sites) + 1}",
                "name": name,
                "type": 1,                  # ← 必须 1，不能 3
                "api": api,
                "searchable": 1 if s.get("searchable") else 0,
                "quickSearch": 1 if s.get("quickSearch") else 0,
                "filterable": 1 if s.get("filterable") else 0,
            }
            if s.get("detail"):
                item["detail"] = s["detail"]
            sites.append(item)
    return sites


def probe(site, timeout=8):
    api, sep = site["api"], ("&" if "?" in site["api"] else "?")
    try:
        req = urllib.request.Request(api + sep + "ac=detail&pg=1", headers=UA)
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            body = r.read(300000).decode("utf-8", "replace")
        i = body.find("{")
        d = json.loads(body[i:]) if i >= 0 else {}
        return len(d.get("list") or []) > 0
    except Exception:
        return False


def build(sites):
    return {
        "wallpaper": "",
        "sites": sites,
        "lives": [],
        "parses": [],
        "flags": FLAGS,
        "spider": "",
        "doh": [
            {"name": "阿里DoH", "url": "https://dns.alidns.com/dns-query"},
            {"name": "腾讯DoH", "url": "https://doh.pub/dns-query"},
        ],
        "rules": [],
        "ads": [],
    }


def dump(obj, path):
    with open(os.path.join(REPO, path), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print(f"  → {path}  {len(obj.get('sites', []))} 站")


def for_desktop(sites):
    """电脑端 TVBox Desktop 的 type 语义不同：CMS 采集接口要写 3，写 1 会被当成
    需要 HTML 规则的站点，直接报错。这里单独产出一份桌面端配置。"""
    out = []
    for s in sites:
        d = dict(s)
        d["type"] = 3
        out.append(d)
    return out


def desktop_native(sites):
    """电脑端自家 B 方言（format=tvbox-desktop/1，type 用 "cms"），可读性更好。"""
    out = []
    for s in sites:
        out.append({
            "key": s["key"],
            "name": s["name"],
            "type": "cms",
            "api": s["api"],
            "searchable": bool(s.get("searchable")),
            "quickSearch": bool(s.get("quickSearch")),
            "filterable": bool(s.get("filterable")),
        })
    return {
        "format": "tvbox-desktop/1",
        "name": "TVBox Desktop 电脑端配置（LunaTV 转换）",
        "sites": out,
        "lives": [],
        "parses": [],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-probe", action="store_true", help="不实测站点存活")
    ap.add_argument("--include-adult", action="store_true", help="保留成人源")
    args = ap.parse_args()

    sites = collect(args.include_adult)
    print(f"合并去重后站点：{len(sites)}")
    if not sites:
        print("没有取到任何站点，保留旧文件不动")
        sys.exit(2)

    full = build(sites)
    dump(full, "oktv.json")
    dump(build(for_desktop(sites)), "tvbox.json")   # 电脑端专用：type=3

    if args.no_probe:
        alive = sites
    else:
        print("实测存活中…")
        with ThreadPoolExecutor(max_workers=12) as ex:
            ok = list(ex.map(probe, sites))
        alive = [s for s, o in zip(sites, ok) if o]
        print(f"存活：{len(alive)}/{len(sites)}")
    dump(build(alive), "oktv-alive.json")
    dump(build(for_desktop(alive)), "tvbox-alive.json")   # 电脑端精简版
    dump(desktop_native(sites), "tvbox-desktop.json")     # 电脑端 B 方言（type: cms）
    dump(desktop_native(alive), "tvbox-desktop-alive.json")

    # 额外再存一份不含成人源的版本，家里电视/给小孩看时用这两个
    safe = [s for s in sites if "🔞" not in s["name"]]
    safe_alive = [s for s in alive if "🔞" not in s["name"]]
    if len(safe) != len(sites):
        dump(build(safe), "oktv-safe.json")
        dump(build(safe_alive), "oktv-safe-alive.json")

    info = {
        "updated_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "total": len(sites),
        "alive": len(alive),
        "include_adult": args.include_adult,
        "safe_total": len(safe),
        "safe_alive": len(safe_alive),
        "sources": SOURCES,
    }
    with open(os.path.join(REPO, "version.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    print("  → version.json", info["updated_utc"])


if __name__ == "__main__":
    main()
