import pandas as pd
import random

# 총 행 개수 (테스트용)
n = 190_000

# 샘플 데이터
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

# 중복 전화번호 일부러 섞기 (랜덤 1000개 중복)
for i in range(1000):
    dup_phone = df.loc[random.randint(0, n - 1), "전화번호"]
    df.loc[random.randint(0, n - 1), "전화번호"] = dup_phone

# 엑셀 or CSV로 저장
df.to_csv("dummy_190k.csv", index=False, encoding="utf-8-sig")
print("✅ 더미 CSV 생성 완료: dummy_190k.csv")
