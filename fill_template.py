# 파일명: fill_template.py
# 사용법: python fill_template.py

import pandas as pd
from openpyxl import load_workbook
from pathlib import Path

# 경로 설정
template_path = Path(r"C:\Users\ST\Desktop\excel_program\hangawon.xlsx")
csv_path = Path(r"C:\Users\ST\Desktop\excel_program\123_only_unique.csv")
output_path = Path(r"C:\Users\ST\Desktop\excel_program\hangawon_filled.xlsx")

# 1️⃣ unique CSV 불러오기
print("📂 unique CSV 불러오는 중...")
df = pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig')

# 컬럼 이름 자동 감지 (첫 컬럼 = 수신자 번호, 마지막 컬럼 = URL)
phone_col = df.columns[0]
url_col = df.columns[-1]

print(f"✅ 수신자 번호 컬럼: {phone_col}")
print(f"✅ URL 컬럼: {url_col}")
print(f"총 데이터 수: {len(df):,}건")

# 2️⃣ 템플릿 엑셀 로드
wb = load_workbook(template_path)
ws = wb.active  # 기본 첫 시트

# 3️⃣ 채워넣기
start_row = 2
for i, row in df.iterrows():
    ws[f"A{start_row + i}"] = row[phone_col]  # 수신자 번호
    ws[f"G{start_row + i}"] = row[url_col]    # URL
    if (i + 1) % 500 == 0:
        print(f"  ↳ {i + 1:,}건 채워넣는 중...")

# 4️⃣ 새 파일로 저장
wb.save(output_path)
print(f"\n🎉 완료! 결과 파일 저장됨: {output_path}")