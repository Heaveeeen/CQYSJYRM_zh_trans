
import os

for i in range(380):
    id = str(i).zfill(5)
    os.rename(
        f"./bilingual_auto/异世界语入门-jp-{id}_bilingual.txt",
        f"./bilingual_auto/{id}_bilingual.cqyr.txt"
    )
    os.rename(
        f"./jp_raw/异世界语入门-jp-{id}_raw.txt",
        f"./jp_raw/{id}_raw.cqyr.txt"
    )
    os.rename(
        f"./zh_trans/异世界语入门-jp-{id}_ainiee_trans.txt",
        f"./zh_trans/{id}_zh.cqyr.txt"
    )