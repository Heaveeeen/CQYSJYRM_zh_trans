def splitZh(s: str):
    zhJp = s.split("\n")
    zh = []
    i = 0
    while i < len(zhJp):
        zh.append(zhJp[i])
        if zhJp[i] == "":
            i += 1
        else:
            i += 2
    return "\n".join(zh)

def splitJp(s: str):
    zhJp = s.split("\n")
    jp = []
    i = 0
    while i < len(zhJp):
        if zhJp[i] != "":
            i += 1
        jp.append(zhJp[i])
        i += 1
    return "\n".join(jp)

# for i in range(380):
#     id = str(i).zfill(5)
#     s = ""
#     with open(f"./异世界语入门-jp-{id}_bilingual.txt", encoding="utf-8") as f:
#         s = f.read()
#     with open(f"./_splitOut/异世界语入门-jp-{id}_ainiee_trans.txt", "w", encoding="utf-8") as f:
#         f.write(splitZh(s))

for i in range(380):
    id = str(i).zfill(5)
    s = ""
    with open(f"./异世界语入门-jp-{id}_bilingual.txt", encoding="utf-8") as f:
        s = f.read()
    with open(f"../jp_raw/异世界语入门-jp-{id}_raw.txt", "w", encoding="utf-8") as f:
        f.write(splitJp(s))
