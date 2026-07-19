import pandas as pd
from pathlib import Path
REQUIRED_COLS={'transaction_id','date','amount'}
def load(path,date_col='date'):
    path=Path(path);suffix=path.suffix.lower()
    if suffix=='.csv': df=pd.read_csv(path)
    elif suffix in ('.xlsx','.xls'): df=pd.read_excel(path)
    elif suffix=='.json': df=pd.read_json(path)
    else: raise ValueError(f'Unsupported:{suffix}')
    missing=REQUIRED_COLS-set(df.columns)
    if missing: raise ValueError(f'Missing required columns:{missing}')
    df[date_col]=pd.to_datetime(df[date_col],errors='coerce')
    df['amount']=pd.to_numeric(df['amount'],errors='coerce')
    return df
