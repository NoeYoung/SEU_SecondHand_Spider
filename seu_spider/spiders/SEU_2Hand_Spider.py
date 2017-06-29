import scrapy
import json
import itchat
import time
import sqlite3
import seu_spider.sqllib as sqllib
from functools import reduce

class MyChat(itchat.Core):
    def get_username_by_name(self,name):
        dict_list = self.search_friends(name=name)
        return dict_list[0]['UserName']
          
    def send_message_by_name(self,name,message):
        self.send(message, toUserName=self.get_username_by_name(name))

    def send_debug(self,message):
        self.send(message,toUserName='filehelper')
    
class SEU_2Hand_Spider(scrapy.Spider):
    name = "seu2hand"
    allowed_domains = ["seu.edu.cn"]
    start_urls = [
        "http://bbs.seu.edu.cn/api/board/secondhand.js?mode=1&limit=100"
    ]
    msg = ""
    queue = []

    def database_operation(self,dicts):
        # Database Operation
        table_name = "SpiderDB"
        conn = sqlite3.connect('SEU_sechand.db')
        c = conn.cursor(sqllib.DB_Exec)
        c.create_table(table_name,("id int primary key","title text","author text","time int"))
        
        for i in dicts['topics']:
            if (c.check_num_in_database(table_name,'id',i['id']) == 0):
                c.insert_data(table_name,(i['id'],i['title'],i['author'],i['time']))
                self.queue.append(i['title'])

        conn.commit()
        conn.close()
        
    def wechat_operation(self):
        mychat = MyChat()

        #login wechat
        mychat.auto_login(enableCmdQR=2,hotReload=True)
        mychat.send_debug(reduce(lambda str1,str2:str1 + '\n' + str2,self.queue))
        
    def parse(self, response):
        js = json.loads(response.body_as_unicode())
        self.database_operation(js)
        self.wechat_operation()
