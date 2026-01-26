def sl_tp(entry, side, rr=1.5):
    risk = entry * 0.002
    if side == "BUY":
        return round(entry - risk, 2), round(entry + risk * rr, 2)
    else:
        return round(entry + risk, 2), round(entry - risk * rr, 2)
