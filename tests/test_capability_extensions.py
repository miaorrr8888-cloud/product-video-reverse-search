from pathlib import Path
import importlib.util,unittest,tempfile,json,sys,subprocess,os
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('extension',ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class SearchAdapter(unittest.TestCase):
    def test_response_keeps_identity_unknown(self):
        m=load('scripts/search_youtube.py');r=m.convert({'items':[{'id':{'videoId':'DEMO0000001'},'snippet':{'title':'Demo'}}]}, {'keywords':['demo']})
        self.assertEqual(r['candidates'][0]['match_level'],'unknown');self.assertIsNone(r['candidates'][0]['views'])
    def test_non_video_entries_ignored(self):self.assertEqual(load('scripts/search_youtube.py').convert({'items':[{'id':{'channelId':'abc'}}]}, {})['candidates'],[])
    def test_live_requires_configuration(self):
        with self.assertRaises(ValueError):load('scripts/search_youtube.py').fetch('demo',5,None)
