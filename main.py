#!/usr/bin/env python3

import sys
import json
import pandas as pd
from collections import defaultdict


def load_mapping(json_file):
    """담당자 -> 세부파트 Dictionary 생성"""

    with open(json_file, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    member_to_part = {}

    for part, members in mapping.items():
        for member in members:
            member_to_part[member] = part

    return member_to_part


def read_voc(voc_file, member_to_part):

    df = pd.read_excel(voc_file)

    result = defaultdict(lambda: defaultdict(list))

    for _, row in df.iterrows():

        try:
            manager, department = row["담당"].split("/", 1)
        except Exception:
            manager = row["담당"]
            department = "미지정부서"

        manager = manager.strip()
        department = department.strip()

        detail_part = member_to_part.get(manager, "미분류")

        result[department][detail_part].append({
            "VOC번호": row["VOC번호"],
            "제목": row["제목"],
            "담당자": manager
        })

    return result


def print_result(result):

    total = 0

    print("\n")
    print("=" * 80)
    print("VOC 분류 결과")
    print("=" * 80)

    for department, part_dict in sorted(result.items()):

        dept_count = sum(len(v) for v in part_dict.values())
        total += dept_count

        print(f"\n[{department}] ({dept_count}건)")
        print("-" * 80)

        for part, vocs in sorted(part_dict.items()):

            print(f"\n  ▶ {part} ({len(vocs)}건)")

            for voc in vocs:
                print(
                    f"    {voc['VOC번호']:8}"
                    f" | {voc['담당자']:<8}"
                    f" | {voc['제목']}"
                )

    print("\n" + "=" * 80)
    print(f"전체 VOC : {total}건")
    print("=" * 80)


def main():

    if len(sys.argv) < 2:
        print("사용법")
        print("python3 main.py <VOC.xlsx> [part_mapping.json]")
        sys.exit(1)

    voc_file = sys.argv[1]

    if len(sys.argv) >= 3:
        json_file = sys.argv[2]
    else:
        json_file = "part_mapping.json"

    member_to_part = load_mapping(json_file)

    result = read_voc(voc_file, member_to_part)

    print_result(result)


if __name__ == "__main__":
    main()
    