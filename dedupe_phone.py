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
    """전화번호에서 숫자만 남기기"""
    if pd.isna(x):
        return ''
    return re.sub(r'\D', '', str(x))

print("📊 전화번호 중복 스캔 중...")
phone_counts = {}

# 1️⃣ 전화번호별 등장 횟수 계산
for chunk in pd.read_csv(src, chunksize=chunksize, dtype=str, low_memory=True):
    norms = chunk[phone_col].map(normalize_phone)
    for ph in norms:
        if ph:
            phone_counts[ph] = phone_counts.get(ph, 0) + 1

print(f"✅ 고유 전화번호 수: {len(phone_counts):,}개")

# 2️⃣ 출력 파일 경로
out_duplicates = src.with_name(src.stem + '_only_duplicates.csv')  # 중복(True)
out_unique = src.with_name(src.stem + '_only_unique.csv')          # 비중복(False)
dup_rows_written = 0
unique_rows_written = 0

print("🧩 중복/비중복 파일 생성 중...")

# 3️⃣ 청크 단위로 처리
for chunk in pd.read_csv(src, chunksize=chunksize, dtype=str, low_memory=True):
    normalized = chunk[phone_col].map(normalize_phone)
    chunk['중복횟수'] = normalized.map(lambda x: phone_counts.get(x, 0))
    chunk['중복여부'] = chunk['중복횟수'] > 1

    dup_chunk = chunk[chunk['중복여부']]       # True만
    unique_chunk = chunk[~chunk['중복여부']]   # False만

    if not dup_chunk.empty:
        mode = 'w' if dup_rows_written == 0 else 'a'
        dup_chunk.to_csv(
            out_duplicates, index=False, encoding='utf-8-sig',
            mode=mode, header=(dup_rows_written == 0)
        )
        dup_rows_written += len(dup_chunk)

    if not unique_chunk.empty:
        mode = 'w' if unique_rows_written == 0 else 'a'
        unique_chunk.to_csv(
            out_unique, index=False, encoding='utf-8-sig',
            mode=mode, header=(unique_rows_written == 0)
        )
        unique_rows_written += len(unique_chunk)

print("\n🎉 완료!")
print(f"📁 중복된 행만 저장: {out_duplicates}")
print(f"📁 중복 없는 행만 저장: {out_unique}")
