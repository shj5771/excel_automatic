# 파일명: dedupe_phone.py
# 사용법: python dedupe_phone.py real_csv.csv

import sys
import re
import pandas as pd
from pathlib import Path

# ===== 0️⃣ 경로 설정 =====
base_dir = Path(r"C:\Users\ST\Desktop\excel_program")
input_dir = base_dir / "input"
output_dir = base_dir / "output"
output_dir.mkdir(exist_ok=True)

# ===== 1️⃣ 명령행 인자 확인 =====
if len(sys.argv) < 2:
    print("Usage: python dedupe_phone.py real_csv.csv")
    sys.exit(1)

file_name = sys.argv[1]
src = input_dir / file_name

if not src.exists():
    print(f"❌ 입력 파일을 찾을 수 없습니다: {src}")
    sys.exit(1)

# ===== 2️⃣ 기본 설정 =====
phone_col = '매칭용'      # 전화번호 열
boundary_col = '조사 URL'  # 경계 기준 컬럼 (첫 공백 이후 전부 중복 처리)

# ===== 3️⃣ 전화번호 정규화 함수 =====
def normalize_phone(x: str) -> str:
    if pd.isna(x):
        return ''
    return re.sub(r'\D', '', str(x))

print(f"📂 입력 파일: {src}")
print("📊 전화번호 중복 스캔 중...")

# ===== 4️⃣ 파일 로드 및 정규화 =====
df = pd.read_csv(src, dtype=str, encoding='utf-8-sig').fillna('')

if phone_col not in df.columns:
    print(f"❌ '{phone_col}' 컬럼이 존재하지 않습니다. 실제 컬럼명 목록: {list(df.columns)}")
    sys.exit(1)

df['정규화전화번호'] = df[phone_col].map(normalize_phone)

# ===== 5️⃣ 전화번호 비어있는 행은 일단 유지 =====
before_len = len(df)
removed = 0  # 삭제 없음
print(f"⚠️ 전화번호가 비어있어도 행은 유지 (경계 판단용)")

# ===== 6️⃣ 기본 중복 계산 =====
phone_counts = df.loc[df['정규화전화번호'].str.strip() != '', '정규화전화번호'].value_counts().to_dict()
df['중복횟수'] = df['정규화전화번호'].map(phone_counts).fillna(0).astype(int)
df['중복여부'] = df['중복횟수'] > 1

# ===== 7️⃣ 경계 처리: boundary_col 첫 공백 이후 전부 중복(True) =====
if boundary_col not in df.columns:
    raise KeyError(f"❌ '{boundary_col}' 컬럼을 찾지 못했습니다. 실제 헤더: {list(df.columns)}")

blank_idx_list = df.index[df[boundary_col].astype(str).str.strip() == ''].tolist()
flipped = 0
if blank_idx_list:
    first_blank_idx = blank_idx_list[0]
    before_mask = df.loc[first_blank_idx:, '중복여부'].copy()
    df.loc[first_blank_idx:, '중복여부'] = True
    flipped = (before_mask == False).sum()
    total_below = len(df) - first_blank_idx
    print(f"⚠️ '{boundary_col}' 첫 공백 행(index={first_blank_idx}) 이후 전체를 중복(True) 처리")
    print(f"📊 B영역 전체 {total_below:,}행 중 False→True 변경된 {flipped:,}건")

# ===== 8️⃣ 분리 및 중복 대표 1건만 남기기 =====
dup_df = df[df['중복여부']].drop_duplicates(subset=['정규화전화번호'], keep='first')
unique_df = df[~df['중복여부']]


# ===== 9️⃣ 불필요한 컬럼 제거 =====
drop_cols = ["정규화전화번호", "휴대전화번호"]
dup_df = dup_df.drop(columns=[c for c in drop_cols if c in dup_df.columns])
unique_df = unique_df.drop(columns=[c for c in drop_cols if c in unique_df.columns])

# ===== 🔟 파일 저장 =====
out_duplicates = output_dir / f"{src.stem}_only_duplicates.csv"
out_unique = output_dir / f"{src.stem}_only_unique.csv"

dup_df.to_csv(out_duplicates, index=False, encoding='utf-8-sig')
unique_df.to_csv(out_unique, index=False, encoding='utf-8-sig')

# ===== 요약 =====
print("\n🎉 완료!")
print(f"📁 중복 데이터(모두 포함): {out_duplicates}")
print(f"📁 비중복 데이터: {out_unique}")
print(f"📊 중복 {len(dup_df):,}건 | 비중복 {len(unique_df):,}건 | 총 {len(df):,}건")
