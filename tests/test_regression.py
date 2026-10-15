from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, os
R=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

class Ranking(unittest.TestCase):
    def test_unknown_and_nonfinite_views_are_not_verified(self):
        m=load('ranking',R/'scripts/extract_and_rank.py')
        for value in [None,'not a number',float('inf'),float('nan')]: self.assertIsNone(m.interaction_score(value))
        self.assertEqual(m.interaction_score(0),0)

if __name__=="__main__": unittest.main(verbosity=2)
