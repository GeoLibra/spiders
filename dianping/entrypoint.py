from scrapy.cmdline import execute
# 第三个参数是spider的名字
# execute(['scrapy','crawl','dpSpider'])
# 续爬模式，会自动生成一个crawls文件夹，用于存放断点文件
# execute('scrapy crawl dpSpider -s JOBDIR=crawls/dpSpider'.split())
'''
 -L WARNING  去掉提示
'''
# 非续爬模式
execute('scrapy crawl dpSpider'.split())
