import requests
import time

# =================配置区================
source_list = [
    "https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u",
    "https://iptv-org.github.io/iptv/countries/cn.m3u"
]
output_file = "live.m3u"
timeout = 25
# ========================================

def parse_m3u(content: str):
    """解析m3u，返回 [(extinf_line, url), ...]"""
    entries = []
    lines = content.splitlines()
    extinf = None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            extinf = line
        elif line and not line.startswith("#"):
            if extinf is not None:
                entries.append((extinf, line))
                extinf = None
    return entries

def main():
    all_entries = []
    seen_url = set()

    for src_url in source_list:
        print(f"正在获取源：{src_url}")
        try:
            resp = requests.get(src_url, timeout=timeout)
            resp.encoding = "utf-8"
            items = parse_m3u(resp.text)
            for extinf, play_url in items:
                if play_url not in seen_url:
                    seen_url.add(play_url)
                    all_entries.append((extinf, play_url))
            print(f"该源解析得到 {len(items)} 条，累计不重复 {len(all_entries)}")
            time.sleep(1)
        except Exception as e:
            print(f"源获取失败 {src_url} ：{str(e)}")

    # 组装标准m3u
    out_lines = ["#EXTM3U"]
    for extinf, playurl in all_entries:
        out_lines.append(extinf)
        out_lines.append(playurl)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"\n✅完成，输出文件 {output_file}，总频道数：{len(all_entries)}")

if __name__ == "__main__":
    main()
