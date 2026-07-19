import csv
from dataclasses import asdict
from pathlib import Path
from recon.matcher import MatchResult
def export_csv(results,path,include_matched=False):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    rows=results if include_matched else [r for r in results if r.status!='matched']
    fields=['transaction_id','status','amount_a','amount_b','amount_diff','date_a','date_b','notes']
    with open(p,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        w.writeheader();w.writerows([asdict(r) for r in rows])
    return p
