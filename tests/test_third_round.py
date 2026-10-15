from pathlib import Path
import importlib.util,sys,unittest,tempfile,json
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('third',ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class LocalRetrieval(unittest.TestCase):
    def test_identical_beats_different_color(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);Image.new('RGB',(40,40),'red').save(p/'query.png');Image.new('RGB',(40,40),'red').save(p/'same.png');Image.new('RGB',(40,40),'blue').save(p/'other.png')
            r=load('scripts/search_local_images.py').search(p/'query.png',p);self.assertEqual(r['results'][0]['file'],'same.png');self.assertFalse(r['results'][0]['identity_verified'])
    def test_broken_candidate_skipped(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);Image.new('RGB',(40,40),'red').save(p/'q.png');(p/'broken.png').write_bytes(b'not an image')
            self.assertEqual(load('scripts/search_local_images.py').search(p/'q.png',p)['skipped'],['broken.png'])
    def test_invalid_limit_rejected(self):
        with self.assertRaises(ValueError):load('scripts/search_local_images.py').search('q','d',0)
