用scrapy框架从www.chahaoba.com爬取各地各运营商的前7位号码段
执行scrapy crawl chahaoba -o test.csv即可得到

更改gen_sjhm.py中sf变量定义，并执行即可得到该省份所有地市，运营商的手机号码（输出文件路径output）