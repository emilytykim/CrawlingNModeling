# details.py

import requests
import json
import sys
import os
import csv
from concurrent.futures import ThreadPoolExecutor


def fetch_detail(pid: str):
    url = f"https://api.bunjang.co.kr/api/pms/v3/products-detail/{pid}?viewerUid=-1"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",  # zstd 생략
        "user-agent": "Mozilla/5.0",
        "origin": "https://m.bunjang.co.kr",
        "referer": "https://m.bunjang.co.kr/",
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        data = res.json()
        return {
            "pid": pid,
            "title": data.get("item_info", {}).get("title"),
            "description": data.get("item_info", {}).get("description"),
            "price": data.get("item_info", {}).get("price"),
            "seller_nickname": data.get("seller_info", {}).get("nickname"),
            "update_time": data.get("item_info", {}).get("update_time"),
        }
    except Exception as e:
        return {"pid": pid, "error": str(e)}


def main(input_json_path: str):
    with open(input_json_path, "r", encoding="utf-8") as f:
        pid_list = json.load(f)

    print(f"📦 Crawling {len(pid_list)} items from {input_json_path}")

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_detail, pid_list))

    # 저장 디렉토리
    os.makedirs("details_results", exist_ok=True)
    output_csv = os.path.join(
        "details_results", os.path.basename(input_json_path).replace(".json", ".csv")
    )

    # CSV로 저장
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Done: saved to {output_csv}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗ 사용법: python details.py pid/pid_1.json")
        sys.exit(1)
    main(sys.argv[1])
