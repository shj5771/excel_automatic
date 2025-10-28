# 파일명: main_excel_pipeline.py
# 사용법: python main_excel_pipeline.py real_csv.csv
# 실행 시 dedupe_phone.py → fill_template_split_debug.py 자동 실행

import subprocess
from pathlib import Path

# ===== 경로 설정 =====
base_dir = Path(r"C:\Users\ST\Desktop\excel_program")
input_dir = base_dir / "input"
output_dir = base_dir / "output"
unique_dir = output_dir / "unique"
unique_dir.mkdir(exist_ok=True)

dedupe_script = base_dir / "dedupe_phone.py"
fill_script = base_dir / "fill_template_split_debug.py"

# ===== 입력 CSV 이름 확인 =====
import sys
if len(sys.argv) < 2:
    print("Usage: python main_excel_pipeline.py real_csv.csv")
    sys.exit(1)

input_file = sys.argv[1]
src = input_dir / input_file

if not src.exists():
    print(f"❌ 입력 파일이 존재하지 않습니다: {src}")
    sys.exit(1)

print(f"\n🚀 실행 시작: {input_file}\n")

# ===== 1️⃣ dedupe_phone.py 실행 =====
print("📞 1단계: 전화번호 중복 제거 및 분리 시작...")
dedupe_result = subprocess.run(
    ["python", str(dedupe_script), input_file],
    cwd=str(base_dir),
    text=True
)

if dedupe_result.returncode != 0:
    print("❌ dedupe_phone.py 실행 중 오류 발생. 종료합니다.")
    sys.exit(1)
print("✅ 1단계 완료!\n")

# ===== 2️⃣ fill_template_split_debug.py 실행 =====
unique_csv = output_dir / f"{Path(input_file).stem}_only_unique.csv"

if not unique_csv.exists():
    print(f"❌ {unique_csv} 파일이 존재하지 않아 템플릿 채우기를 건너뜁니다.")
    sys.exit(1)

print("🧩 2단계: 템플릿 자동 채움 및 분할 저장 시작...")
fill_result = subprocess.run(
    ["python", str(fill_script)],
    cwd=str(base_dir),
    text=True
)

if fill_result.returncode != 0:
    print("❌ fill_template_split_debug.py 실행 중 오류 발생.")
    sys.exit(1)

print("\n🎉 전체 파이프라인 완료!")
print(f"📁 결과 경로: {unique_dir}")
print(f"✅ 중복제거 CSV: {unique_csv.name}")
print(f"✅ 엑셀 분할 결과: hangawon_filled_part_*.xlsx\n")
