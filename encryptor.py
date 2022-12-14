import hash
import random
import sys
import uuid


def salt(org_str: str, salt_str: str, unique_number_range: int):
    unique_number = random.randrange(0, unique_number_range)
    salted = org_str + "_" + salt_str + "_" + str(unique_number)
    return salted


def encrypt(file_location: str, salt_str: str, unique_number_range: int, iteration: int, output_location: str):
    with open(file_location, "r", encoding="utf-8") as f:
        # 개행 문자 제거를 위한 splitlines() 사용
        line_list = f.read().splitlines()
        result_output = []
        for i in line_list:
            if i.strip() == "":
                continue
            encryption_target = salt(i, salt_str, unique_number_range)
            for j in range(iteration):
                encryption_target = hash.sha256(encryption_target)
            result_output.append(encryption_target)
        uuid_str = str(uuid.uuid4())

        summary_file_location = output_location + "Summary_" + uuid_str + ".txt"
        result_file_location = output_location + "Result_" + uuid_str + ".txt"

        with open(summary_file_location, "w") as outfile:
            summary_output = ["FILE_LOCATION : " + file_location, "SALT : " + salt_str,
                              "UNIQUE_NUMBER_RANGE : " + str(unique_number_range), "ITERATION : " + str(iteration)]
            outfile.write("\n".join(summary_output))

        with open(result_file_location, "w") as outfile:
            outfile.write("\n".join(result_output))

        print(uuid_str)

if __name__ == '__main__':
    encrypt(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] + "\\" if len(sys.argv) > 5 else "")

# TDL
# 줄(Line)의 개수가 노출되는 것이 핵심 -> 개별 Line의 암호화를 통해 변화율 측정 가능, 다만 Line을 섞는 것은 가능할 듯
# 해독은 줄위치에 무관함(dict) -> 수정에 유연함

# ↓ sys.argv
# file location
# salt string
# unique number range(같은 문장의 경우 같은 값이 나오는 상황을 방지하기 위해 정해진 범위 내에 랜덤 값을 추가한다, 범위는 0이상 해당 숫자 미만)
# iteration
# output file location(optional)
#
# ex )
# "target.txt" "salt_message" 100 20000 "output"
