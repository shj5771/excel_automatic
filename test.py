import pandas as pd
from pathlib import Path

# ✅ 중복 검사할 파일 지정
path = Path(r"C:\Users\ST\Desktop\excel_program\input\real_csv.csv")
# path = Path(r"C:\Users\ST\Desktop\excel_program\output\real_csv_only_unique.csv")  # <- 비중복 파일 검사하려면 이 줄로 바꾸기

df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
col = "매칭용"  # 전화번호 컬럼명

# 중복 탐지
dupes = df[col].value_counts()
dupes = dupes[dupes > 1]

print(f"\n📂 검사 대상 파일: {path.name}")

if len(dupes) == 0:
    print("✅ 완벽! 중복 전화번호 없음.")
else:
    print(f"⚠️ 중복된 전화번호 {len(dupes)}건 발견:")
    print(dupes.head(20))