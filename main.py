# 파일명: main_excel_pipeline.py
# 사용법: python main_excel_pipeline.py real_csv.csv

import sys
import subprocess
from pathlib import Path

# ===============================
# 0. 경로 설정
# ===============================
BASE_DIR = Path(r"C:\Users\ST\Desktop\excel_program")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
UNIQUE_DIR = OUTPUT_DIR / "unique"
UNIQUE_DIR.mkdir(exist_ok=True)

DEDUPE_SCRIPT = BASE_DIR / "dedupe_phone.py"
FILL_SCRIPT = BASE_DIR / "fill_template_split_debug_tomix.py"


# ===============================
# 1. 함수: 스크립트 실행
# ===============================
def run_script(script_path, args=None):
    cmd = ["python", str(script_path)]
    if args:
        cmd.extend(args)

    print(f"▶ 실행: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(BASE_DIR), text=True)

    if result.returncode != 0:
        print(f"❌ 오류 발생: {script_path.name}")
        sys.exit(1)
    print(f"✅ 완료: {script_path.name}\n")


# ===============================
# 2. 메인 프로세스
# ===============================
def main():
    # (1) 인자 확인
    if len(sys.argv) < 2:
        print("Usage: python main_excel_pipeline.py real_csv.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    src = INPUT_DIR / input_file

    if not src.exists():
        print(f"❌ 입력 파일을 찾을 수 없습니다: {src}")
        sys.exit(1)

    print("\n🚀 전체 파이프라인 시작")
    print(f"📂 입력 파일: {src.name}\n")

    # (2) 1단계: 중복 제거
    print("📞 [1단계] 전화번호 중복 제거 및 CSV 분리 실행 중...")
    run_script(DEDUPE_SCRIPT, [input_file])

    # (3) 유니크 CSV 확인
    unique_csv = OUTPUT_DIR / f"{Path(input_file).stem}_only_unique.csv"
    if not unique_csv.exists():
        print(f"❌ 중복 제거 후 결과 CSV가 없습니다: {unique_csv}")
        sys.exit(1)

    print("✅ [1단계 완료] 중복 제거 결과 생성됨:", unique_csv.name, "\n")

    # (4) 2단계: 템플릿 채워서 분할 저장
    print("🧩 [2단계] 엑셀 템플릿 자동 채우기 + 파일 분할 저장 시작...")
    run_script(FILL_SCRIPT)

    # (5) 완료 메시지
    print("\n🎉 전체 프로세스 완료!")
    print(f"📁 결과 폴더: {OUTPUT_DIR}")
    print(f"✅ 중복 제거 CSV: {unique_csv.name}")
    print("✅ 분할 엑셀 파일: hangawon_filled_part_*.xlsx")


# ===============================
# 3. 실행 트리거
# ===============================
if __name__ == "__main__":
    main()
