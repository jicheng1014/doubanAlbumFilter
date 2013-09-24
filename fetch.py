#coding:utf-8
from pyquery.pyquery import PyQuery as pq
import urllib2
import json

answer = []
getIt=False
init_url = raw_input("输入豆瓣活动相册类似（http://www.douban.com/online/11463780/album/85256333/）\n地址:")

search_location = raw_input("输入地理位置:")
#init_url = "http://www.douban.com/online/11463780/album/85256333/";
try:
	d = pq(url=init_url)
	
	l = d(".paginator a")
	
	l = [int(i.attrib["href"].split("=")[1]) for i  in l]
	max_page = max(l)
	for tmp in range(0,max_page,30):
		try:
			current_url = init_url + "?start="+str(tmp)
			print "正在访问页面",current_url
			d = pq(url=current_url)
			tmpA = d(".pl > a")
			people_node_list = [node for node in tmpA if node.attrib["href"].find("people")>-1]
			
			print "." 
			for uri_node in people_node_list :
				person_id = uri_node.attrib["href"].split("/")[-2]
				personjson = urllib2.urlopen("http://api.douban.com/v2/user/"+ person_id).read()
				name = ""
				try:
					loc_name = json.loads(personjson)["loc_name"]
					name =  json.loads(personjson)["name"]
				except:
					continue
				if loc_name.encode("utf-8").find(search_location) != -1:
					info_a = pq(uri_node.getparent()).prev()
					answer.append([name,info_a.attr("href"),info_a.eq(0).html()])
					print name, info_a.attr("href")
					print "ok"
		except Exception,tmpE:
			print tmpE
			print "访问出错了，跳过继续执行"
			continue


except Exception,e:
	print e
	print "出错了，我们显示出错前的数据"

print "#############################"
 

for line in answer:
	print line[0],line[1]
print "结果同时在同级目录的output.html中，可用浏览器直接打开查看"

try:
	file = open("output.html","w")
	file.write("<html><body><table>")
	for line in answer:
		file.write("<tr><td>"+line[0].encode("utf-8")+"</td><td><a href='"+line[1]+"'>"+line[2].encode("utf-8")+"</a></td></tr>")
	file.write("</table></body></html>")
except Exception, x:
	print x
finally:
	file.close()
