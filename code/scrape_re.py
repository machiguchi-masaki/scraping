import re
from html import unescape

with open('work/dp.html') as f:
    html = f.read()

for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
    # <p itemprop="name" class="title"><span class="series">情報処理技術者試験</span> 【改訂<wbr/>4<wbr/>版】<wbr/>要点・<wbr/>用語早わかり 応用情報技術者 ポケット攻略本</p>
    title = title.replace('<wbr/>', ' ')
    title = re.sub(r'<.*?>', '', title)
    print(title)


