## spiders
Python爬虫集锦

| 代码 | 功能 |
| ------ | ------ |
| whu_seat | 武大占座程序 |
| whu_wxseat | 武大占座程序(通过微信) |
| github  | 模拟登陆github |
| dianping  | 大众点评爬虫 |
| proxy  | 抓取代理 |
| task  | 定时任务 |

## scrapy
注意关闭HTTP缓存，之前请求出现302，导致通过Scrapy请求一直是320，而通过requests访问可以成功，后来关闭HTTP缓存便能访问成功
## xpath小技巧
1. `a/@*[name()="href" or name()="title"]` 可以获取href和title属性值