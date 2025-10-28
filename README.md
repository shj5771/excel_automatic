dedue_phone_1 = csv파일을 받아서 중복, 비중복 분리
fill_template_2.py = template에 맞춰서 중복 false인 애들 자동입력

실행코드 :  python main.py (csv 파일 명).csv


***** 실행 방법 *****

1. input 폴더 안에 두개의 템플릿(양식)을 첨부한다.
    > 1) hangawon.xlsx   < csv에서 중복 검출해서 보내야 하는 양식 xlsx
    > 2) real_csv.csv    < xlsx 받은 거 csv로 저장
    
2. python main.py (input에 넣은 csv파일 명).csv 로 실행한다.

3. output > csv에서 전화번호 중복된 값들 > (input에 넣은 {csv파일 명_only_duplicates.csv})
          > csv에서 전화번호 중복되지 않은 값들 > (input에 넣은 {csv파일 명_only_unique.csv}

4. output > unique 안에는 중복되지 않은 값들을 xlsx 양식에 맞춰서, 1500줄씩 쪼개서 
분할저장된다.

5. 끝


C:\Users\ST\Desktop\excel_program\
│
├─ main.py                           ← 실행할 메인 파일
├─ dedupe_phone.py                   ← 1단계: 중복 제거
├─ fill_template_split_debug.py       ← 2단계: 템플릿 채우기
│
├─ input\
│   ├─ real_csv.csv                  ← ✅ csv(false, tru 추)
│   └─ hangawon.xlsx                 ← ✅ 템플릿 (A열 번호 / G열 URL)
│
└─ output\
    ├─ real_csv_only_duplicates.csv  ← (자동 생성) 중복된 행
    ├─ real_csv_only_unique.csv      ← (자동 생성) 중복 없는 행
    └─ unique\
        ├─ hangawon_filled_part_1.xlsx
        ├─ hangawon_filled_part_2.xlsx
        └─ … (1500줄씩 분할된 결과)

