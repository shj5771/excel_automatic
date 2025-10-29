# 파일명: dedupe_phone.py
# 사용법: python dedupe_phone.py real_csv.csv
# (입력 파일은 C:\Users\ST\Desktop\excel_program\input 안에 있어야 함)

### 원본 엑셀을 csv로 저장 한 후, 그 csv를 전화번호 중복 제거 및 분리하는 스크립트 ###
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
phone_col = '매칭용'  # 전화번호 들어있는 컬럼명

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

# ===== 5️⃣ 전화번호 없는 행 제거 =====
before_len = len(df)
df = df[df['정규화전화번호'].str.strip() != '']
removed = before_len - len(df)
if removed > 0:
    print(f"⚠️ 전화번호가 비어있는 {removed:,}행은 제외됨")

# ===== 6️⃣ 중복 계산 =====
phone_counts = df['정규화전화번호'].value_counts().to_dict()
df['중복횟수'] = df['정규화전화번호'].map(phone_counts)
df['중복여부'] = df['중복횟수'] > 1

# ===== 7️⃣ 중복 분리 (1행만 남기기) =====
dup_df = df[df['중복여부']].drop_duplicates(subset=['정규화전화번호'], keep='first')
unique_df = df[~df['중복여부']]

# ===== 8️⃣ 불필요한 컬럼 제거 =====
drop_cols = ["정규화전화번호", "휴대전화번호"]
dup_df = dup_df.drop(columns=[c for c in drop_cols if c in dup_df.columns])
unique_df = unique_df.drop(columns=[c for c in drop_cols if c in unique_df.columns])

# ===== 9️⃣ 파일 저장 =====
out_duplicates = output_dir / f"{src.stem}_only_duplicates.csv"
out_unique = output_dir / f"{src.stem}_only_unique.csv"
out_duplicates_xlsx = output_dir / f"{src.stem}_only_duplicates.xlsx"
out_unique_xlsx = output_dir / f"{src.stem}_only_unique.xlsx"

# 🔹 CSV로 저장
dup_df.to_csv(out_duplicates, index=False, encoding='utf-8-sig')
unique_df.to_csv(out_unique, index=False, encoding='utf-8-sig')

# 🔹 Excel로도 저장 (열 순서 유지)
dup_df.to_excel(out_duplicates_xlsx, index=False, engine='openpyxl')
unique_df.to_excel(out_unique_xlsx, index=False, engine='openpyxl')


# ===== 🔟 요약 =====
print("\n🎉 완료!")
print(f"📁 중복된 전화번호 (1개씩만): {out_duplicates}")
print(f"📁 중복 없는 행: {out_unique}")
print(f"📊 중복 {len(dup_df):,}건 | 비중복 {len(unique_df):,}건 | 제외 {removed:,}건 | 총 {before_len:,}건")