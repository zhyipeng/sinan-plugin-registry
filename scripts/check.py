"""资料登记校验；正式版本分发协议尚未实现。"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
seen = set()
for path in sorted((root / "plugins").glob("*/plugin.json")):
    item = json.loads(path.read_text())
    assert item["schemaVersion"] == 1
    assert item["id"] == path.parent.name and item["id"] not in seen
    seen.add(item["id"])
    assert item["name"] and item["summary"]
    assert item["publisher"]["kind"] in ("official", "community")
    assert item["status"] == "pending-release"
    assert item["releases"] == [], "正式版本协议尚未实现，不能登记可安装版本"
    source = item["source"]
    assert source["repository"] is None or source["repository"].startswith("https://github.com/")
    assert source["path"] and not source["path"].startswith("/") and ".." not in source["path"].split("/")
assert seen, "目录不能为空"
print(f"资料校验通过：{len(seen)} 个插件，0 个可安装版本")
