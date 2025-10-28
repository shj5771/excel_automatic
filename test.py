# 파일명: make_190k_with_url.py
# 사용법: python make_190k_with_url.py

import pandas as pd
import random

# 행 개수 설정
n = 190_000

print("📊 19만 행짜리 CSV 생성 중...")

# 더미 데이터 구성
data = {
    "조사명": ["테스트조사"] * n,
    "이름": [f"홍길동{i}" for i in range(1, n + 1)],
    "전화번호": [
        f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
        for _ in range(n)
    ],
    "소속": [random.choice(["A리서치", "B리서치", "C리서치"]) for _ in range(n)],
    "1": [random.randint(1, 5) for _ in range(n)],
    "2": [random.randint(1, 5) for _ in range(n)],
    "3": [random.randint(1, 5) for _ in range(n)],
    "4": [random.randint(1, 5) for _ in range(n)],
    "5": [random.randint(1, 5) for _ in range(n)],
}

df = pd.DataFrame(data)

# URL 컬럼 추가 (랜덤 예시 링크)
df["URL"] = [
    f"https://survey.example.com/form?id={i:06d}"
    for i in range(1, n + 1)
]

# 중복 전화번호 일부러 섞기 (랜덤 1000개 중복)
for i in range(1000):
    dup_phone = df.loc[random.randint(0, n - 1), "전화번호"]
    df.loc[random.randint(0, n - 1), "전화번호"] = dup_phone

# 저장
output = "C:/Users/ST/Desktop/excel_program/123.csv"
df.to_csv(output, index=False, encoding="utf-8-sig")

print(f"🎉 완료! 생성된 파일 경로: {output}")
print(f"총 {len(df):,}행, URL 포함, 중복 전화번호 약 1000개 삽입됨 ✅")
