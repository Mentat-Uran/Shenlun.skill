"""Extract plain text from a .docx using only the Python standard library.

A .docx is a ZIP containing word/document.xml. This walks the paragraph and run
structure so that行序、段落分隔与软换行都保留，不依赖 python-docx。
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        # 正文可能在 document.xml；少数导出会拆到多个 part
        parts = [n for n in names if re.fullmatch(r"word/document(\d*)\.xml", n)]
        parts.sort(key=lambda n: (len(n), n))
        if not parts:
            raise SystemExit("未找到 word/document*.xml，实际内容：\n  " + "\n  ".join(names[:40]))
        out = []
        for part in parts:
            root = ET.fromstring(z.read(part))
            out.append(_walk(root))
        return "\n".join(out)


def _walk(root):
    lines = []
    for p in root.iter(W + "p"):
        buf = []
        for node in p.iter():
            tag = node.tag
            if tag == W + "t":
                buf.append(node.text or "")
            elif tag == W + "tab":
                buf.append("\t")
            elif tag in (W + "br", W + "cr"):
                buf.append("\n")
        line = "".join(buf)
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    text = extract(src)
    # 压缩连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("段落数:", text.count("\n") + 1)
    print("字符数:", len(text))
    print("写出:", dst)
