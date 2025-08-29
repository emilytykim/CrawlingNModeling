# split_pid_list.py

import pandas as pd
import os
import json
import math


def split_pid_list(csv_file: str, output_dir: str = "pid", num_files: int = 20):
    # CSV 파일 불러오기
    df = pd.read_csv(csv_file)

    # 상품ID 또는 pid 열 선택
    pid_column = "상품ID" if "상품ID" in df.columns else "pid"
    pid_list = df[pid_column].dropna().astype(str).unique().tolist()

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # PID 목록을 N등분해서 나누기
    chunk_size = math.ceil(len(pid_list) / num_files)
    for i in range(num_files):
        chunk = pid_list[i * chunk_size : (i + 1) * chunk_size]
        if not chunk:
            continue
        path = os.path.join(output_dir, f"pid_{i+1}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(chunk)} PIDs to {path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("❗ 사용법: python split_pid_list.py merged_results_final.csv")
        sys.exit(1)
    split_pid_list(sys.argv[1])
