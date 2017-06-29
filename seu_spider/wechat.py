import itchat

class MyChat(itchat.Core):
    def get_username_by_name(self,name):
        dict_list = self.search_friends(name=name)
        return dict_list[0]['UserName']
          
    def send_message_by_name(self,name,message):
        self.send(message, toUserName=self.get_username_by_name(name))

    def send_debug(self,message):
        self.send(message,toUserName='filehelper')

