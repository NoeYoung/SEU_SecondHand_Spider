import scrapy
import json
import time
import sqlite3
import platform
from functools import reduce

import seu_spider.wechat as wechat
import seu_spider.sqllib as sqllib

class SEU_2Hand_Spider(scrapy.Spider):
    name = "seu2hand"
    allowed_domains = ["seu.edu.cn"]
    table_name = "SEU2Hand"
    database_name = "SEU_sechand.db"
    queue = []

    def database_operation(self,dicts):
        # Database Operation
        conn = sqlite3.connect(self.database_name)
        c = conn.cursor(sqllib.DB_Exec)
        c.create_table(self.table_name,("id int primary key","title text","author text","time int"))
        
        for i in dicts['topics']:
            if (c.check_num_in_database(self.table_name,'id',i['id']) == 0):
                c.insert_data(self.table_name,(i['id'],i['title'],i['author'],i['time']))
                self.queue.append(i['title'])

        conn.commit()
        conn.close()

    def wechat_operation(self):
        if self.queue:
            mychat = wechat.MyChat()

            #login wechat
            mychat.auto_login(enableCmdQR=2,hotReload=True)
            #mychat.send_debug(reduce(lambda str1,str2:str1 + '\n' + str2,self.queue))
            inform_str = platform.platform() + '\n' + time.strftime("%m/%d/%Y %H:%M:%S");
            mychat.send_debug(inform_str)
            mychat.send_debug('\n'.join(self.queue))

        else:
            print("=========No New Items==========")
     
    def clear_queue(self):
        self.queue = []
        
    def start_requests(self):

        conn = sqlite3.connect(self.database_name)
        c = conn.cursor(sqllib.DB_Exec)
        table_exist = c.check_table(self.table_name)
        conn.close()

        if not table_exist:
            # if the table does not exist, create and scrapy max number of items
            print("=========create table===========")
            yield scrapy.Request("http://bbs.seu.edu.cn/api/board/secondhand.js?mode=1&limit=100000", self.sechand_init_parse)
        else:
            # scrap 100 items
            print("=========scrap new items===========")
            yield scrapy.Request("http://bbs.seu.edu.cn/api/board/secondhand.js?mode=1&limit=100", self.sechand_parse)

    def sechand_init_parse(self, response):
        spider_json_data = json.loads(response.body_as_unicode())
        self.database_operation(spider_json_data)
        self.clear_queue()

    def sechand_parse(self, response):
        spider_json_data = json.loads(response.body_as_unicode())
        self.database_operation(spider_json_data)
        self.wechat_operation()
        self.clear_queue()
