"""资料与待审核发布记录校验；不生成可安装索引。"""
import json
import re
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
submissions = list((root / "submissions").glob("*/*.json"))
for path in submissions:
    item = json.loads(path.read_text())
    assert set(item) == {"schemaVersion", "pluginId", "name", "version", "repository", "tag", "commit", "compatibility", "assets", "releaseId"}
    assert item["schemaVersion"] == 1
    assert re.fullmatch(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+", item["pluginId"])
    assert len(item["pluginId"]) <= 128 and not item["pluginId"].startswith("system.")
    assert path.parent.name == item["pluginId"] and path.stem == item["version"]
    assert re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", item["version"])
    assert isinstance(item["name"], str) and 0 < len(item["name"].strip()) <= 64
    assert re.fullmatch(r"[\w.-]+/[\w.-]+", item["repository"])
    assert item["tag"] == "v" + item["version"] and re.fullmatch(r"[a-f0-9]{40}", item["commit"])
    assert type(item["releaseId"]) is int and item["releaseId"] > 0
    assert item["compatibility"] == {"apiVersion": "1", "uiBridgeVersion": "2"}
    assert item["assets"]
    targets = set()
    for asset in item["assets"]:
        assert set(asset) == {"os", "arch", "file", "sha256", "size", "assetId", "downloadUrl"}
        target = (asset["os"], asset["arch"])
        assert target not in targets and asset["os"] in ("darwin", "linux", "windows") and asset["arch"] in ("arm64", "amd64")
        targets.add(target)
        expected = f"{item['pluginId']}-{item['version']}-{asset['os']}-{asset['arch']}.zip"
        assert asset["file"] == expected and re.fullmatch(r"[a-f0-9]{64}", asset["sha256"])
        assert type(asset["size"]) is int and 0 < asset["size"] <= 64 * 1024 * 1024
        assert type(asset["assetId"]) is int and asset["assetId"] > 0
        assert asset["downloadUrl"] == f"https://github.com/{item['repository']}/releases/download/{item['tag']}/{expected}"
print(f"资料校验通过：{len(seen)} 个插件，{len(submissions)} 个待审核发布，0 个可安装版本")
