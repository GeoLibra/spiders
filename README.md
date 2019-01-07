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
`a/@*[name()="href" or name()="title"]` 可以获取href和title属性值  
1、XPATH使用方法  
使用XPATH有如下几种方法定位元素（相比CSS选择器，方法稍微多一点）：  
a、通过绝对路径定位元素（不推荐！）  
WebElement ele = driver.findElement(By.xpath("html/body/div/form/input"));

b、通过相对路径定位元素

WebElement ele = driver.findElement(By.xpath("//input"));

c、使用索引定位元素

WebElement ele = driver.findElement(By.xpath("//input[4]"));

d、使用XPATH及属性值定位元素

WebElement ele = driver.findElement(By.xpath("//input[@id='fuck']"));

//其他方法(看字面意思应该能理解吧)

WebElement ele = driver.findElement(By.xpath("//input[@type='submit'][@name='fuck']"));

WebElement ele = driver.findElement(By.xpath("//input[@type='submit' and @name='fuck']"));

WebElement ele = driver.findElement(By.xpath("//input[@type='submit' or @name='fuck']"));

e、使用XPATH及属性名称定位元素

元素属性类型：@id 、@name、@type、@class、@tittle

//查找所有input标签中含有type属性的元素

WebElement ele = driver.findElement(By.xpath("//input[@type]"));

f、部分属性值匹配

WebElement ele = driver.findElement(By.xpath("//input[starts-with(@id,'fuck')]"));//匹配id以fuck开头的元素，id='fuckyou'

WebElement ele = driver.findElement(By.xpath("//input[ends-with(@id,'fuck')]"));//匹配id以fuck结尾的元素，id='youfuck'

WebElement ele = driver.findElement(By.xpath("//input[contains(@id,'fuck')]"));//匹配id中含有fuck的元素，id='youfuckyou'

g、使用任意值来匹配属性及元素

WebElement ele = driver.findElement(By.xpath("//input[@*='fuck']"));//匹配所有input元素中含有属性的值为fuck的元素
