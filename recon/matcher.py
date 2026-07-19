from dataclasses import dataclass,field
from datetime import timedelta
import pandas as pd
@dataclass
class MatchResult:
    transaction_id:str;status:str
    amount_a:float|None=None;amount_b:float|None=None
    date_a:str|None=None;date_b:str|None=None
    amount_diff:float=0.0;date_diff_days:int=0;notes:str=''
class Matcher:
    def __init__(self,key_col='transaction_id',amount_col='amount',date_col='date',amount_tolerance=0.01,date_tolerance_days=1):
        self.key=key_col;self.amount=amount_col;self.date=date_col
        self.amount_tol=amount_tolerance;self.date_tol=timedelta(days=date_tolerance_days)
    def match(self,df_a,df_b):
        results=[];a=df_a.set_index(self.key);b=df_b.set_index(self.key)
        for key in sorted(set(a.index)|set(b.index)):
            in_a,in_b=key in a.index,key in b.index
            if not in_b: r=a.loc[key];results.append(MatchResult(key,'missing_in_b',amount_a=float(r[self.amount]),date_a=str(r[self.date]),notes='In A only'))
            elif not in_a: r=b.loc[key];results.append(MatchResult(key,'missing_in_a',amount_b=float(r[self.amount]),date_b=str(r[self.date]),notes='In B only'))
            else:
                ar,br=a.loc[key],b.loc[key]
                amt_a,amt_b=float(ar[self.amount]),float(br[self.amount])
                da,db=pd.to_datetime(ar[self.date]),pd.to_datetime(br[self.date])
                amt_diff=abs(amt_a-amt_b);date_diff=abs((da-db).days)
                if amt_diff>self.amount_tol:status='amount_mismatch';notes=f'Amt diff:{amt_diff:.2f}'
                elif date_diff>self.date_tol.days:status='date_mismatch';notes=f'Date diff:{date_diff}d'
                else:status='matched';notes=''
                results.append(MatchResult(key,status,amt_a,amt_b,str(da.date()),str(db.date()),round(amt_diff,4),date_diff,notes))
        return results
