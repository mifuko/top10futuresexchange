2024-03-27

- 淦郑商所网页改了，在`bssss.py`中BeautifulSoup和urllib不得行了，报错:

```urllib.error.HTTPError: HTTP Error 412: Precondition Failed```

改了header之后，在console中发现直接被拒绝

```Failed to load resource: the server responded with a status of 400 (Bad Request)```

抓这个网页都失败了```http://www.czce.com.cn/cn/DFSStaticFiles/Future/2024/20240326/FutureDataTradeamt.htm```，换个思路直接从主页一路模拟鼠标点进去，也是空白

手动点击发现Agent是这个```Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36```



- 上期所的`shangqiso.py`当天只能爬取前一天的，修改日期好像失效了，估计页面也有改动，但至少还能用

- 中金所的`ssszhijiexiazai.py`根据不同合约构建url还正常，得到`merged.csv`正常，但是计算top10的部分有问题，因为经纪商名字改了，在后面加了（经纪），需要修改这个字典

```
# 创建 brokerlist 列表
brokerlist = ['上海东证', '华泰期货', '南华期货', '中信建投', '招商期货', '中泰期货', '银河期货', 
              '中信期货', '国泰君安', '海通期货', '申银万国', '国信期货', '方正中期', '光大期货', 
              '东吴期货', '平安期货', '华安期货', '浙商期货', '广发期货', '宏源期货']
```

- 大商所的`ddds.py`最后获取结果有问题，页面直接显示top150，修改一下爬取的内容，舍弃成交额的排名，只保留成交量的排名

- 广期所的`ggfex.py`可以用，不落地，table在div里面，layui，官网不能开代理访问


2024-03-28

- 上期所【待修改】
  - 办公环境要开代理才能访问
  - 运行前要删除历史结果文件

- 郑商所【待修改】
  - 先运行得到源代码
  - 再处理源代码得到结果

- 广期所
  - 要关闭代理才能访问

- 大商所【待修改】
  - 是某个天所在当月的，不是具体日期的
  - 某个交易日好像硬算也可以算

- 中金所【待修改】
  - 运行前需要删除历史结果文件
  - 要关闭代理才能访问
