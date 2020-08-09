# 微信公众号接口的业务层,此处代码用于设置了安全模式下的公众号接口
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply,ImageReply
import access_token_get
from wechatpy.crypto import WeChatCrypto
import senya


class poi:
    def __init__(self):
        self.Appid = 'wxc99887c60a8b96ec'
        self.Token = '3b3149d56bd02dd8a3e805b0008bdb13'
        self.encodingkey = 'eLDdhoBB16J4j9pfqPruXz4rJ2sxmHLXbJH5oXgVUSc'

    def _get_args(self,req):
        query_string = req.query_string
        query_list = query_string.split('&')
        try:
            self.b = {}
            for i in query_list:
                self.b[i.split('=')[0]] = i.split('=')[1]
        except:
            pass
        return self.b

    def on_get(self,req,resp):
        try:
            arg = self._get_args(req)
        except:
            pass
        else:
            try:
                check_signature(token='3b3149d56bd02dd8a3e805b0008bdb13',signature=arg['signature'],timestamp=arg['timestamp'], nonce=arg['nonce'])
                resp.body = (arg['echostr'])
            except InvalidSignatureException:
                pass
        resp.status = falcon.HTTP_200

    # 收到xml后解密的代码
    def _get_message(self,req):
        xml = req.stream.read()
        arg = self._get_args(req)
        # 解密信息的代码
        cypro = WeChatCrypto(self.Token,self.encodingkey,self.Appid)
        decrypt = cypro.decrypt_message(
            xml,
            arg['msg_signature'],
            arg['timestamp'],
            arg['nonce']
        )
        msg = parse_message(decrypt)
        return msg,arg

    # 用户通过公众号发送微信后，微信将特定的xml文件以post的方法post到服务器，服务器对其处理后返回xml给微信服务器。
    def on_post(self,req,resp):

        # 加密信息的函数
        def nico(reply):
            xml1 = reply.render()
            crypto1 = WeChatCrypto(self.Token,self.encodingkey,self.Appid)
            encrypted_xml1 = crypto1.encrypt_message(xml1,arg['timestamp'],arg['nonce'])
            resp.body = encrypted_xml1

        try:
            msg,arg = self._get_message(req)
        except InvalidSignatureException:
            pass
        else:
            if msg.type == 'text':
                if msg.content == '作业':
                    access_token_get.wechat().get_access()
                    reply = ImageReply(media_id=access_token_get.wechat().picture(),message=msg)
                    nico(reply)
                elif msg.content == '关键词':
                    reply = TextReply(content='回复“作业”将能得到所布置作业的图片格式\n回复其他语句可直接开启聊天机器人模式！', message=msg)
                    nico(reply)
                else:
                    reply = TextReply(content=senya.chatbot(msg.content),message=msg) #调用机器人
                    nico(reply)
            elif msg.type == 'event':
                if msg.event == 'subscribe':
                    reply = TextReply(content='欢迎关注！',message=msg)
                    nico(reply)
                else:
                    pass
            else:
                reply = TextReply(content='没有这个功能呢！',message=msg)
                nico(reply)


app = falcon.API()
poi = poi()
app.add_route('/poi',poi)