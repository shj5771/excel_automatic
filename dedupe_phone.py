# 파일명: dedupe_phone.py
# 사용법: python dedupe_phone.py 123.csv

import sys
import re
import pandas as pd
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python dedupe_phone.py 123.csv")
    sys.exit(1)

src = Path(sys.argv[1])
if not src.exists():
    print("❌ File not found:", src)
    sys.exit(1)

chunksize = 20000
phone_col = '전화번호'

def normalize_phone(x):
    if pd.isna(x):
        return ''
    return re.sub(r'\D', '', str(x))

print("📊 전화번호 중복 스캔 중...")
phone_counts = {}
for chunk in pd.read_csv(src, chunksize=chunksize, dtype=str, low_memory=True):
    norms = chunk[phone_col].map(normalize_phone)
    for ph in norms:
        if ph:
            phone_counts[ph] = phone_counts.get(ph, 0) + 1

print(f"✅ 고유 전화번호 수: {len(phone_counts):,}개")

out_flagged = src.with_name(src.stem + '_flagged.csv')
out_duplicates = src.with_name(src.stem + '_only_duplicates.csv')
first_write = True
dup_rows_written = 0

print("🧩 중복 표시 및 파일 생성 중...")

for chunk in pd.read_csv(src, chunksize=chunksize, dtype=str, low_memory=True):
    # 정규화는 내부 계산용
    normalized = chunk[phone_col].map(normalize_phone)

    # 중복정보 계산
    chunk['중복횟수'] = normalized.map(lambda x: phone_counts.get(x, 0))
    chunk['중복여부'] = chunk['중복횟수'] > 1

    # 전체 CSV (중복여부, 중복횟수 포함)
    mode = 'w' if first_write else 'a'
    chunk.to_csv(out_flagged, index=False, encoding='utf-8-sig', mode=mode, header=first_write)
    first_write = False

    # 중복만 별도 CSV
    dup_chunk = chunk[chunk['중복여부']]
    if not dup_chunk.empty:
        mode = 'w' if dup_rows_written == 0 else 'a'
        dup_chunk.to_csv(out_duplicates, index=False, encoding='utf-8-sig', mode=mode, header=(dup_rows_written == 0))
        dup_rows_written += len(dup_chunk)

print("\n🎉 완료!")
print(f"📁 전체 데이터(중복표시 포함): {out_flagged}")
print(f"📁 중복된 행만 저장: {out_duplicates}")
