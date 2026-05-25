def split(s: str):
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

for i in range(380):
    id = str(i).zfill(5)
    s = ""
    with open(f"./异世界语入门-jp-{id}_bilingual.txt", encoding="utf-8") as f:
        s = f.read()
    with open(f"./_splitOut/异世界语入门-jp-{id}_ainiee_trans.txt", "w", encoding="utf-8") as f:
        f.write(split(s))