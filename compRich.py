
import json
from typing import TypedDict, List
import os
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

class Episode(TypedDict):
    webRawUrl: str
    topic: str
    datetime: str
    timeText: str
    id: str

class Chapter(TypedDict):
    chapterName: str
    episodes: List[Episode]

class Book(TypedDict):
    bookName: str
    chapters: List[Chapter]

InfoJson = List[Book]

infoJp: InfoJson
with open("./info_jp.json", "r", encoding="utf-8") as file:
    infoJp = json.load(file)

import regex

removedComments: dict[str, int] = {}
def replComment(match):
    comment = match.group(0)
    if comment in removedComments:
        removedComments[comment] += 1
    else:
        removedComments[comment] = 1
    return ""

def printRemovedComments():
    if len(removedComments) == 0: return
    print(f"Removed {sum(removedComments.values())} comments:")
    for comment, count in removedComments.items():
        print(f"  {count} * {comment}")

def toPlainText(richText: str) -> str:
    plainText = regex.sub(r'(?<!:)//.*?(?<!:)(//|$)', replComment, richText, flags=regex.MULTILINE)
    plainText = plainText.replace("**", "").replace("{", "").replace("$", "（").replace("}", "）")
    plainText = regex.sub(r'^~book~ (.*?)$', r'== \1 ==', plainText, flags=regex.MULTILINE)
    plainText = regex.sub(r'^~chapter~ (.*?)$', r'~ \1 ~', plainText, flags=regex.MULTILINE)
    return plainText

def toHtml(richText: str, title: str) -> str:
    content = regex.sub(r'(?<!:)//.*?(?<!:)(//|$)', replComment, richText, flags=regex.MULTILINE)
    content = content.replace('"', "&quot;").replace("'", "&#39;").replace("<", "&lt;").replace(">", "&gt;")
    html = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8"></meta>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no"></meta>
    <style>
        body {
            margin: 0;
            background-color: hsl(36deg 60% 90%);
        }
        p {
            line-height: 1.8;
            margin: 0;
            break-inside: avoid;
        }
        em {
            font-style: normal;
            font-weight: bold;
        }
        #novelMain {
            width: 100%;
            max-width: 700px;
            margin: 0 auto;
            padding: 0 15px;
            box-sizing: border-box;
        }
    </style>
    <title>""" + title + """</title>
</head>
<body>
<div id="novelMain">
"""
    iota = 0
    def getNextH3Txt(match):
        nonlocal iota
        iota += 1
        return f'<h3 id="episodeTopic{iota}">{match.group(0)}</h3>'
    content = regex.sub(r'^~book~ (.*?)$', r'<h1>\1</h1>', content, flags=regex.MULTILINE)
    content = regex.sub(r'^~chapter~ (.*?)$', r'<h2>\1</h2>', content, flags=regex.MULTILINE)
    content = regex.sub(r'^#.*?$', getNextH3Txt, content, flags=regex.MULTILINE)
    content = regex.sub(r'(^[^<\r\n].*$)|(^\s*$)', lambda match : f"<p>{match.group(0)}</p>" if match.group(0).strip() else '<p class="blank"><br /></p>', content, flags=regex.MULTILINE)
    content = regex.sub(r'\*\*(.*?)\*\*', r'<em>\1</em>', content)
    content = regex.sub(r'\{(.*?)\$(.*?)\}', r'<ruby><rb>\1</rb><rp>（</rp><rt>\2</rt><rp>）</rp></ruby>', content)
    content += '<p class="blank"><br /><br /></p>'
    html += content
    html += """
</div>
</body>
</html>"""
    return html

def compRichForAFile(inputFile: str, title: str):
    with open(inputFile, "r", encoding="utf-8") as f:
        richText = f.read()
    html = toHtml(richText, title)
    plainText = toPlainText(richText)
    dirpath, filename = os.path.split(inputFile)
    filename = os.path.splitext(filename)[0]
    with open(os.path.join(dirpath, "CQHtm_" + filename + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(dirpath, "CQTxt_" + filename + ".txt"), "w", encoding="utf-8") as f:
        f.write(plainText)

debugForeword = f"""此文档是《异世界语入门》 Web 版的 AI 粗翻版。
日文版来源于：https://kakuyomu.jp/works/1177354054883808252
目前该版本只是粗翻版，我都不好意思端出去。仅供个人使用，请勿传播。
项目地址：https://github.com/heaveeeen/CQYSJYRM_zh_trans
构建时间：{timestamp}"""

if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:
        print("Usage: python compRich.py <inputFile> <title?>")
        sys.exit(1)

    arg1 = sys.argv[1]
    if arg1 == "--debug-fullNovel":
        outDir = f"./out/debug_fullNovel/{timestamp}/"
        os.makedirs(outDir)
        fullNovel = f"~book~ -译者前言-\n\n{debugForeword}\n\n"
        for i in range(380):
            id = str(i).zfill(5)
            dir = f"./src/zh_trans/{id}_zh.cqyr.txt"
            with open(dir, encoding="utf-8") as f:
                fullNovel += f.read() + "\n\n\n"
        with open(f"{outDir}[AI粗翻]异世界语入门ep0~380-web版-debug{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write(toPlainText(fullNovel))
        with open(f"{outDir}[AI粗翻]异世界语入门ep0~380-web版-debug{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(toHtml(fullNovel, f"[AI粗翻]异世界语入门ep0~380-web版-debug{timestamp}"))

    elif arg1 == "--debug-each":
        outDir = f"./out/debug_each/{timestamp}/"
        os.makedirs(outDir)
        os.makedirs(outDir + "txt/")
        os.makedirs(outDir + "html/")
        for i in range(380):
            id = str(i).zfill(5)
            dir = f"./src/zh_trans/{id}_zh.cqyr.txt"
            with open(dir, encoding="utf-8") as f:
                episode = f"========\n\n{debugForeword}\n\n========\n\n" + f.read()
            with open(f"{outDir}txt/{id}.txt", "w", encoding="utf-8") as f:
                f.write(toPlainText(episode))
            with open(f"{outDir}html/{id}.html", "w", encoding="utf-8") as f:
                f.write(toHtml(episode, f"[AI粗翻]异世界语入门ep0~380-web版-debug{timestamp}"))

    else:
        compRichForAFile(arg1, sys.argv[2] if len(sys.argv) == 3 else "CQHtm_" + arg1)
    
    printRemovedComments()