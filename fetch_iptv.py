import requests
import time

# ==========在这里修改你的公开直播源地址==========
source_list = [
    "https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u"
]
output_file = "live.m3u"
# =============================================

all_content = ""
for url in source_list:
    try:
        print(f"正在获取: {url}")
        r = requests.get(url, timeout=25)
        r.encoding = "utf-8"
        all_content += r.text + "\n"
        time.sleep(1)
    except Exception as e:
        print(f"获取失败 {url} : {e}")

# 写入输出文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"✅已生成 {output_file}")
