"""List and extract embedded media from a .docx (standard library only)."""
import os
import sys
import zipfile

src = sys.argv[1]
outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)

with zipfile.ZipFile(src) as z:
    media = [n for n in z.namelist() if n.startswith("word/media/")]
    print("media 文件数:", len(media))
    total = 0
    for name in sorted(media):
        info = z.getinfo(name)
        total += info.file_size
        print(f"  {name}  {info.file_size} bytes")
        base = os.path.basename(name)
        with open(os.path.join(outdir, base), "wb") as f:
            f.write(z.read(name))
    print("media 总字节:", total)

    # 也看一下 embeds / 其他可能的媒体目录
    others = [n for n in z.namelist()
              if any(k in n.lower() for k in ("media", "image", "embed"))
              and not n.startswith("word/media/")]
    if others:
        print("其他相关条目:", others[:20])
