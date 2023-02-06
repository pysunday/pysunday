from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from smtplib import SMTP_SSL
from sunday.core.logger import Logger

logger = Logger('MAIL').getLogger()

class Email(object):
    """
    发送邮件，用于程序运行监控时的异常预警

    **Usage:**

    ```
    >>> from sunday.utils.Email import Email, getEmailFile
    >>> config = {'host': 'smtp.163.com', 'user': '发送方邮箱地址', 'pwd': '发送方邮箱密码', 'info': '发件人描述', 'tars': '收件人邮箱', 'title': '报错预警邮件'}
    >>> email = Email(**config)
    >>> email.send_mail('<center><h3>HTML文本</h3></center>', msg_type='html')
    >>> email.send_mail('纯文本', msg_type='plain')
    >>> email.send_mail('带附件邮件', docs=getEmailFile(b'二进制', '附件.excel'))
    ```

    **Parameters:**

    * **host:** `str` -- smtp服务地址
    * **user:** `str` -- 邮箱账号
    * **pwd:** `str` -- 授权码
    * **tars:** `str` -- 收件人
    * **title:** `str` -- 邮件标题
    * **info:** `str` -- 发件人描述

    **Return:** `email`
    """
    def __init__(self, host=None, user=None, pwd=None, tars=None, info='info', title='title', **argvs):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.tars = tars
        self.info = info
        self.title = title

    def new_msg(self, content, users, msg_type='plain', info=None, title=None, docs=[]):
        msg = MIMEMultipart()
        msg.attach(MIMEText(content, msg_type, 'utf-8'))
        msg['From'] = f'{info or self.info}<{self.user}>'
        msg['To'] = ','.join(users)
        msg['Subject'] = Header(title or self.title, 'utf-8')
        if type(docs) != list: docs = [docs]
        for doc in docs: msg.attach(doc)
        return msg

    def send(self, msg, users):
        server = SMTP_SSL(self.host, 465)
        server.login(self.user, self.pwd)
        server.sendmail(self.user, users, msg.as_string())
        server.quit()

    def send_mail(self, content, users=None, **argvs):
        """
        执行发送邮件

        **Parameters:**

        * **content:** `str` -- 邮件内容
        * **users:** `str` -- 收件人
        * **msg_type:** `str` -- 邮件内容类型，文本(plain)/网页(html)，默认为plain
        * **title:** `str` -- 邮件标题
        * **info:** `str` -- 发件人描述
        * **docs:** `MIMEApplication` -- 附件
        """
        logger.debug('执行邮件发送')
        users = users or self.tars
        if not users: logger.error('收件人必传')
        if type(users) == str: users = [users]
        try:
            msg = self.new_msg(content, users, **argvs)
            self.send(msg, users)
            logger.info('邮件发送成功')
        except Exception as e:
            logger.exception(e)

def getEmailFile(stream, filename):
    """
    生成文件流对象，用于带附件邮件发送使用

    **Parameters:**

    * **stream:** `binary` -- 二进制流文本
    * **filename:** `str` -- 文件名
    """
    file = MIMEApplication(stream)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    return file

if __name__ == '__main__':
    email = Email('smtp.xxx.com', 'user@xxx.com', 'xxxxxx')
    email.send_mail('content', ['user1@xxx.com', 'user2@xxx.com'], title='title', info='info')
