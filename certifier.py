import sys
import hash


def is_not_blank(str1: str):
    if str1.strip() != "":
        return True
    return False


def certify(org_file_location: str, encrypted_file_location: str, salt_str: str, unique_number_range: int,
            iteration: int):
    # 이미 연산한 줄은 하지 않는다, 복수 개일 경우 어차피 처음 직면하였을 때 org_line_dict에 저장된 수만큼 돌테니 상관 없음
    dup_dic = {}
    org_line_dict = {}
    # 원문이라 추측되는 파일의 줄
    org_line_list = []
    # 증명율을 위한 사전
    encrypted_line_dict = {}
    with open(org_file_location, "r", encoding="utf-8") as f:
        org_line_list = f.read().splitlines()
        # 빈 줄 제거
        org_line_list = list(filter(is_not_blank, org_line_list))
        
        # 같은 내용을 담은 줄이 있을 경우 여러 해시값으로 도출되기에 무조건 그 개수가 채워질 때까지 연산하기 위한 카운트
        for i in org_line_list:
            if i in org_line_dict:
                org_line_dict[i] += 1
            else:
                org_line_dict[i] = 1
    with open(encrypted_file_location, "r", encoding="utf-8") as f:
        encrypted_line_list = f.read().splitlines()
        # 증명 사전 구성
        for i in encrypted_line_list:
            encrypted_line_dict[i] = False

    # 원문이라 추측되는 글의 개수만큼
    for i in org_line_list:
        # 중복이라면 넘김
        if i in dup_dic:
            continue
        else:
            dup_dic[i] = True
            
        # 원문이라 추측되는 글에 중복 개수 중 현재 몇 개를 만족시켰는지
        num_correct_for_dup = 0
        # 위를 만족할 경우 탈출을 위한 플래그
        flag = False

        for j in range(len(i) + 1):
            if flag:
                break

            i1 = i[:j]
            i2 = i[j:]
            for k in range(unique_number_range):
                salted_str = i1 + "_" + salt_str + "_" + str(k) + "_" + i2
                hashed_str = salted_str
                print(hashed_str)
                for l in range(iteration):
                    hashed_str = hash.sha256(hashed_str)

                # 증명된 경우
                if hashed_str in encrypted_line_dict:
                    encrypted_line_dict[hashed_str] = True
                    num_correct_for_dup += 1
                    if num_correct_for_dup == org_line_dict[i]:
                        flag = True
                        break

    len_correct = 0
    for i in encrypted_line_dict:
        if encrypted_line_dict[i]:
            len_correct += 1

    print("")
    print(encrypted_line_dict)
    print("")
    print("CORRECT : " + str(len_correct) + "/" + str(len(encrypted_line_dict)))
    print("CERTIFICATION RATIO : " + str(100 * (len_correct / len(encrypted_line_dict))) + "%")

    if len(encrypted_line_dict) != len(org_line_list):
        print("")
        print("Alert, Number of lines is different")
        print("ORG : " + str(len(org_line_list)))
        print("Encrypted : " + str(len(encrypted_line_dict)))
    return ""


if __name__ == '__main__':
    certify(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))

# TDL
# 암호화된 파일은 무조건 신뢰함을 기반으로 작동
# 줄의 순서는 검증치 않음
# 증명율(CERTIFICATION RATIO)은 암호화된 것들 중 증명된 것들의 비율
#
# ↓ sys.argv
# original file location
# encrypted file location
# salt string
# unique number range
# iteration
#
# ex )
# "org.txt" "encrypted.txt" 100 20000
