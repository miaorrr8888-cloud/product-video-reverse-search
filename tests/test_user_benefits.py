from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, struct, os
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class RankingInputs(unittest.TestCase):
    def setUp(self): self.m=load('ranking',ROOT/'scripts/extract_and_rank.py')
    def data(self): return {'product':{'brand':'Demo','keywords':['demo','demo']},'candidates':[{'url':'https://videos.example/watch?v=A&utm_source=demo','title':'Demo product','match_level':'similar','views':None}]}
    def test_tracking_duplicates_removed_without_losing_video_id(self):
        data=self.data(); data['candidates'] += [dict(data['candidates'][0],url='https://videos.example/watch?v=A'),dict(data['candidates'][0],url='https://videos.example/watch?v=B')]
        report=self.m.rank(data,self.m.parse_date('2026-10-15T00:00:00Z'))
        self.assertEqual(len(report['results']),2); self.assertEqual(report['duplicates_removed'],1)
    def test_score_reproducible_and_explained(self):
        data=self.data(); now=self.m.parse_date('2026-10-15T00:00:00Z')
        self.assertEqual(self.m.rank(data,now),self.m.rank(data,now))
        row=self.m.rank(data,now)['results'][0]; self.assertAlmostEqual(sum(row['score_parts'].values()),row['score']); self.assertFalse(row['content_verified'])
    def test_future_date_unknown_and_invalid_counts_unknown(self):
        self.assertIsNone(self.m.recency_score('2099-01-01',self.m.parse_date('2026-10-15T00:00:00Z')))
        for value in [-1,True,float('inf')]: self.assertIsNone(self.m.interaction_score(value))
    def test_invalid_metrics_remain_strict_json_unknown(self):
        data=self.data(); data['candidates'][0].update(views=float('nan'),likes=-1,comments=True)
        report=self.m.rank(data); json.dumps(report,allow_nan=False)
        for field in ('views','likes','comments'): self.assertIsNone(report['results'][0][field])
    def test_bad_match_and_dangerous_url_rejected(self):
        for change in [{'match_level':'definitely_real'},{'url':'javascript:alert(1)'}]:
            data=self.data(); data['candidates'][0].update(change)
            with self.assertRaises(ValueError): self.m.rank(data)

if __name__=="__main__": unittest.main()
