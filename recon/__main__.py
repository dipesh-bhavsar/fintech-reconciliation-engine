import argparse,yaml
from recon.loader import load
from recon.matcher import Matcher
from recon.console import print_summary
from recon.exporter import export_csv
def cmd_run(args):
    cfg={}
    if args.config:
        with open(args.config) as f:cfg=yaml.safe_load(f).get('matching',{})
    results=Matcher(key_col=cfg.get('key_column','transaction_id'),amount_tolerance=cfg.get('amount_tolerance',0.01),date_tolerance_days=cfg.get('date_tolerance_days',1)).match(load(args.source_a),load(args.source_b))
    print_summary(results)
    if args.report:export_csv(results,args.report);print(f'Report:{args.report}')
p=argparse.ArgumentParser(prog='recon');sub=p.add_subparsers()
pr=sub.add_parser('run');pr.add_argument('--source-a',required=True);pr.add_argument('--source-b',required=True);pr.add_argument('--config',default='config/default.yaml');pr.add_argument('--report',default=None);pr.set_defaults(func=cmd_run)
args=p.parse_args()
if hasattr(args,'func'):args.func(args)
else:p.print_help()
