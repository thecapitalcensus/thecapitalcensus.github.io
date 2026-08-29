#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""データD 公開用CSVの生成 — source/bt/pit_weights_v2.csv (B6.1最終版) から。

規約 amendment_03(第3号改訂)に従い2ファイルを出力する:
  正式公表  7スリーブ  IG+HY をクレジット合算
  補助推計  8スリーブ  IG/HY 内訳(未較正)

処理: 4桁(bp精度)へ丸め → 最大ウェイト列で残差を吸収し合計を厳密に100.0000へ。
入力の数値は改変しない(丸めと正規化のみ)。
"""
import csv, os
from decimal import Decimal, ROUND_HALF_EVEN

B = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(B, "source", "bt", "pit_weights_v2.csv")

# 略号 → 規約のスリーブ名
NAME = {"EQ":"Global Equity", "GOV":"DM Govt Bond", "ILB":"Inflation Linked",
        "IG":"IG Credit", "HY":"High Yield", "SEC":"Securitised",
        "EMD":"EM Debt", "GOLD":"Gold"}
OFFICIAL = ["Global Equity","DM Govt Bond","Inflation Linked","Credit","Securitised","EM Debt","Gold"]
AUX      = ["Global Equity","DM Govt Bond","Inflation Linked","IG Credit","High Yield",
            "Securitised","EM Debt","Gold"]

def q4(x):
    return Decimal(str(x)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN)

def normalise(d, cols):
    """4桁に丸め、残差を最大値の列に寄せて合計を厳密に100.0000にする。"""
    r = {c: q4(d[c]) for c in cols}
    diff = Decimal("100.0000") - sum(r.values())
    if diff != 0:
        big = max(cols, key=lambda c: r[c])
        r[big] += diff
    assert sum(r.values()) == Decimal("100.0000")
    return r

def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    ykey = list(rows[0].keys())[0]
    out_off, out_aux = [], []
    for row in rows:
        y = int(row[ykey])
        v = {NAME[k]: float(row[k]) for k in NAME}
        # 正式: IG + HY を Credit に合算(合算は丸め前に行う)
        off = {c: v[c] for c in OFFICIAL if c != "Credit"}
        off["Credit"] = v["IG Credit"] + v["High Yield"]
        asof = f"{y}-12-31"
        out_off.append({"asof": asof, **{c: str(x) for c, x in normalise(off, OFFICIAL).items()}})
        out_aux.append({"asof": asof, **{c: str(x) for c, x in normalise(v,   AUX     ).items()}})

    def write(path, cols, data):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["asof"] + cols)
            w.writeheader(); w.writerows(data)
        print(f"  {os.path.basename(path):48s} {len(data)}行 x {len(cols)+1}列")

    write(os.path.join(B, "weight_history_1976_2026.csv"), OFFICIAL, out_off)
    write(os.path.join(B, "weight_history_1976_2026_auxiliary_8sleeve.csv"), AUX, out_aux)
    print(f"\n  期間: {out_off[0]['asof']} 〜 {out_off[-1]['asof']}  (年次・年末時点)")
    print(f"  各年の合計 = 100.0000 を検算済み")

if __name__ == "__main__":
    main()
