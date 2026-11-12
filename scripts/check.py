"""校验资料、已审核版本与待审核记录；不下载或执行插件。"""
import base64
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]


def version(value):
    assert isinstance(value, str) and len(value) <= 32
    assert re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value)
    assert all(int(part) < 2**53 for part in value.split("."))


def plugin_id(value):
    assert isinstance(value, str) and len(value) <= 128
    assert re.fullmatch(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+", value)
    assert not value.startswith("system.")


def repository(value):
    assert isinstance(value, str)
    assert re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*/[A-Za-z0-9_-][A-Za-z0-9_.-]*", value)


def release(item, reviewed=False):
    required = {"schemaVersion", "pluginId", "name", "version", "repository", "tag", "commit", "compatibility", "assets", "releaseId"}
    assert set(item) == required | {"minHostVersion"} if reviewed else set(item) in (required, required | {"minHostVersion"})
    assert item["schemaVersion"] == 1
    plugin_id(item["pluginId"])
    version(item["version"])
    if "minHostVersion" in item:
        version(item["minHostVersion"])
    assert isinstance(item["name"], str) and 0 < len(item["name"].strip()) <= 64
    repository(item["repository"])
    assert item["tag"] == "v" + item["version"] and re.fullmatch(r"[a-f0-9]{40}", item["commit"])
    assert type(item["releaseId"]) is int and item["releaseId"] > 0
    assert item["compatibility"] in ({"apiVersion": "1", "uiBridgeVersion": "1"}, {"apiVersion": "1", "uiBridgeVersion": "2"})
    assert isinstance(item["assets"], list) and 0 < len(item["assets"]) <= 8
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


seen = set()
installable = 0
for path in sorted((root / "plugins").glob("*/plugin.json")):
    item = json.loads(path.read_text())
    assert set(item) - {"icon"} == {"schemaVersion", "id", "name", "summary", "publisher", "source", "status", "releases"}
    if "icon" in item:
        icon = item["icon"]
        assert isinstance(icon, str) and len(icon) <= 128 * 1024
        assert icon.startswith(("data:image/svg+xml;base64,", "data:image/png;base64,", "data:image/jpeg;base64,"))
        assert len(base64.b64decode(icon.split(",", 1)[1], validate=True)) <= 64 * 1024
    assert item["schemaVersion"] == 1
    plugin_id(item["id"])
    assert item["id"] == path.parent.name and item["id"] not in seen
    seen.add(item["id"])
    assert isinstance(item["name"], str) and 0 < len(item["name"].strip()) <= 64
    assert isinstance(item["summary"], str) and len(item["summary"].encode()) <= 2048
    assert item["publisher"] in ({"kind": "official"}, {"kind": "community"})
    assert item["status"] in ("pending-release", "published", "withdrawn")
    assert isinstance(item["releases"], list) and len(item["releases"]) <= 64
    assert item["status"] != "pending-release" or not item["releases"]
    assert item["status"] != "published" or item["releases"]
    source = item["source"]
    assert set(source) == {"repository", "path"}
    if source["repository"] is not None:
        assert source["repository"].startswith("https://github.com/")
        repository(source["repository"].removeprefix("https://github.com/"))
    assert source["path"] and not source["path"].startswith("/") and ".." not in source["path"].split("/")
    assert not any(char in source["path"] for char in "\\:\0")
    versions = set()
    for record in item["releases"]:
        release(record, reviewed=True)
        assert record["pluginId"] == item["id"] and record["version"] not in versions
        assert source["repository"] == f"https://github.com/{record['repository']}"
        versions.add(record["version"])
    if item["status"] == "published":
        installable += len(item["releases"])
assert seen and len(seen) <= 128, "目录不能为空或超过 128 项"
submissions = list((root / "submissions").glob("*/*.json"))
for path in submissions:
    item = json.loads(path.read_text())
    release(item)
    assert path.parent.name == item["pluginId"] and path.stem == item["version"]
print(f"资料校验通过：{len(seen)} 个插件，{len(submissions)} 个待审核发布，{installable} 个可安装版本")
