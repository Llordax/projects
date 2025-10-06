# core/risk_management.py
def compute_tp_sl(entry_price, tp_pcts, sl_pcts):
    tps = [entry_price * (1 + pct) for pct in tp_pcts]
    sls = [entry_price * (1 - pct) for pct in sl_pcts]
    return tps, sls
