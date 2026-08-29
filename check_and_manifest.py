#!/usr/bin/env python3
"""
Data D 公開前チェック + MANIFEST.json 生成

  python3 check_and_manifest.py weight_history_1976_2026.csv

実行内容(公開パッケージ準備 v1.0 §7・§8 に対応):
  1. 列構成の検査(列名・型・欠損)
  2. ウェイト合計 = 1 の検算(許容誤差つき)
  3. 期間の連続性(欠落期の検出)と頻度の自動判定
  4. 丸め桁の実測(偽精度の検出)
  5. sha256 生成 → MANIFEST.json の □ を自動で埋める

数値は一切書き換えません。検査して報告し、MANIFEST を書くだけです。
"""
import sys, csv, json, hashlib, datetime as dt
from collections import Counter

TOL = 1e-6          # 合計=1 の許容誤差
PCT_TOL = 1e-4      # 100% 表記の場合の許容誤差

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_date(s):
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y-%m', '%Y/%m', '%Y'):
        try:
            return dt.datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    return None

def main(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit('ERROR: 空のCSVです')

    cols = list(rows[0].keys())
    date_col = cols[0]
    weight_cols = cols[1:]
    problems = []

    print(f"■ ファイル      : {path}")
    print(f"■ 行数          : {len(rows)}")
    print(f"■ 列数          : {len(cols)}  (日付列: '{date_col}' / ウェイト列: {len(weight_cols)})")
    print(f"■ ウェイト列名  : {', '.join(weight_cols)}\n")

    # --- 日付と頻度 ---
    dates = [parse_date(r[date_col]) for r in rows]
    if any(d is None for d in dates):
        bad = [rows[i][date_col] for i, d in enumerate(dates) if d is None][:5]
        problems.append(f"日付として解釈できない値: {bad}")
    else:
        gaps = Counter((dates[i+1] - dates[i]).days for i in range(len(dates)-1))
        common = gaps.most_common(1)[0][0] if gaps else 0
        freq = 'annual' if 350 <= common <= 380 else 'monthly' if 27 <= common <= 32 else f'irregular({common}d)'
        print(f"■ 期間          : {dates[0]} 〜 {dates[-1]}")
        print(f"■ 頻度(推定)    : {freq}")
        odd = [(dates[i], (dates[i+1]-dates[i]).days) for i in range(len(dates)-1)
               if abs((dates[i+1]-dates[i]).days - common) > 3]
        if odd:
            problems.append(f"期間の不連続 {len(odd)}件 (先頭: {odd[:3]})")
        if dates != sorted(dates):
            problems.append("日付が昇順に並んでいません")

    # --- 合計と丸め ---
    sums, decimals = [], set()
    for i, r in enumerate(rows):
        vals = []
        for c in weight_cols:
            raw = (r[c] or '').strip()
            if raw == '':
                problems.append(f"欠損: 行{i+2} 列'{c}'")
                continue
            try:
                vals.append(float(raw))
            except ValueError:
                problems.append(f"数値でない値: 行{i+2} 列'{c}' = {raw!r}")
                continue
            if '.' in raw:
                decimals.add(len(raw.split('.')[1]))
        sums.append(sum(vals))

    scale = '0–1' if sums and max(sums) < 2 else '0–100 (%)'
    target, tol = (1.0, TOL) if scale == '0–1' else (100.0, PCT_TOL * 100)
    off = [(i+2, s) for i, s in enumerate(sums) if abs(s - target) > tol]
    print(f"■ 単位(推定)    : {scale}")
    print(f"■ 合計の範囲    : {min(sums):.10f} 〜 {max(sums):.10f}  (目標 {target})")
    if off:
        problems.append(f"合計が{target}から外れる行 {len(off)}件 (先頭: {off[:3]})")
    print(f"■ 小数桁の実測  : {sorted(decimals)}  ← 推奨は4桁 (bp精度)。5桁以上は偽精度")

    # --- 判定 ---
    print("\n=== 検査結果 ===")
    if problems:
        for p in problems:
            print("  ✗", p)
        print(f"\n  {len(problems)}件の要確認事項があります。MANIFESTは生成しません。")
        return 1
    print("  ✓ 欠損なし / 合計=目標値 / 期間連続 / 日付昇順")

    # --- MANIFEST 更新 ---
    digest = sha256(path)
    try:
        man = json.load(open('MANIFEST.json', encoding='utf-8'))
    except FileNotFoundError:
        man = {"dataset": "capitalcensus-weight-history", "files": [{}]}
    e = man["files"][0]
    e.update({
        "name": path.split('/')[-1],
        "sha256": digest,
        "rows": len(rows),
        "columns": len(cols),
        "period": f"{dates[0]} to {dates[-1]}",
        "frequency": freq,
        "weight_scale": scale,
        "decimal_places": sorted(decimals),
    })
    json.dump(man, open('MANIFEST.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f"\n  ✓ MANIFEST.json を更新しました")
    print(f"    sha256 = {digest}")
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
