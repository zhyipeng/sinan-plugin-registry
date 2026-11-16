"""Only validate metadata; never download or execute plugin packages."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('registry_check', ROOT / 'scripts/check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReleaseTagsTest(unittest.TestCase):
    def record(self, plugin_id='tools.calendar'):
        record = copy.deepcopy(json.loads((ROOT / 'plugins/tools.calendar/plugin.json').read_text())['releases'][0])
        record['pluginId'] = plugin_id
        record['tag'] = plugin_id + '-v' + record['version']
        for asset in record['assets']:
            asset['file'] = f"{plugin_id}-{record['version']}-{asset['os']}-{asset['arch']}.zip"
            asset['downloadUrl'] = f"https://github.com/{record['repository']}/releases/download/{record['tag']}/{asset['file']}"
        return record

    def test_same_repository_same_version_different_plugins(self):
        first, second = self.record(), self.record('tools.clipboard')
        self.assertEqual(first['version'], second['version'])
        self.assertEqual(first['repository'], second['repository'])
        self.assertNotEqual(first['tag'], second['tag'])
        checker.release(first, reviewed=True)
        checker.release(second, reviewed=True)

    def test_existing_legacy_records_remain_valid(self):
        for path in (ROOT / 'plugins').glob('*/plugin.json'):
            for record in json.loads(path.read_text())['releases']:
                checker.release(record, reviewed=True)

    def test_tag_must_bind_exact_plugin_and_version(self):
        for tag in ['tools.clipboard-v0.1.2', 'tools.calendar-v9.0.0', 'tools.calendar/v0.1.2', 'tools.calendar-v0.1.2/../x', 'tools.calendar-v0.1.2-rc.1', '']:
            with self.subTest(tag=tag), self.assertRaises(AssertionError):
                record = self.record()
                record['tag'] = tag
                checker.release(record, reviewed=True)

    def test_download_url_stays_bound_to_tag(self):
        record = self.record()
        record['assets'][0]['downloadUrl'] = record['assets'][0]['downloadUrl'].replace(record['tag'], 'v'+record['version'])
        with self.assertRaises(AssertionError):
            checker.release(record, reviewed=True)


if __name__ == '__main__':
    unittest.main()
