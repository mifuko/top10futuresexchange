2024-03-27

- 淦郑商所网页改了，在`bssss.py`中BeautifulSoup和urllib不得行了，报错:

```urllib.error.HTTPError: HTTP Error 412: Precondition Failed```

- 上期所的`shangqiso.py`当天只能爬取前一天的，修改日期好像失效了，估计页面也有改动，但至少还能用

- 中金所的`ssszhijiexiazai.py`根据不同合约构建url还正常，得到`merged.csv`正常，但是计算top10的部分有问题，因为经纪商名字改了，在后面加了（经纪），需要修改这个字典

```
# 创建 brokerlist 列表
brokerlist = ['上海东证', '华泰期货', '南华期货', '中信建投', '招商期货', '中泰期货', '银河期货', 
              '中信期货', '国泰君安', '海通期货', '申银万国', '国信期货', '方正中期', '光大期货', 
              '东吴期货', '平安期货', '华安期货', '浙商期货', '广发期货', '宏源期货']
```
