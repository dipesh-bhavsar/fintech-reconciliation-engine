import pandas as pd,pytest
from recon.loader import load
def test_valid(tmp_path):
    p=tmp_path/'t.csv';p.write_text('transaction_id,date,amount\nT1,2024-01-01,100\n')
    df=load(str(p));assert len(df)==1 and df['amount'].iloc[0]==100.0
def test_dates(tmp_path):
    p=tmp_path/'t.csv';p.write_text('transaction_id,date,amount\nT1,2024-03-15,50\n')
    assert pd.api.types.is_datetime64_any_dtype(load(str(p))['date'])
def test_missing_col(tmp_path):
    p=tmp_path/'t.csv';p.write_text('id,date,amount\nT1,2024-01-01,100\n')
    with pytest.raises(ValueError):load(str(p))
