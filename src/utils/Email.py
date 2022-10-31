from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from smtplib import SMTP_SSL
from sunday.core.logger import Logger

logger = Logger('MAIL').getLogger()

class Email(object):
    def __init__(self, host=None, user=None, pwd=None, tars=None, info='info', title='title', **argvs):
        '''
        :param host: smtp服务地址
        :param user: 邮箱账号
        :param pwd: 授权码
        :param tars: 收件人
        :param title: 邮件标题
        :param info: 发件人描述
        '''
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
        '''
        :param content: 邮件内容
        :param users: 收件人
        :param msg_type: 邮件内容类型，文本(plain)/网页(html)
        :param title: 邮件标题
        :param info: 发件人描述
        :param docs: 附件
        '''
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
    file = MIMEApplication(stream)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    return file

if __name__ == '__main__':
    email = Email('smtp.xxx.com', 'user@xxx.com', 'xxxxxx')
    email.send_mail('content', ['user1@xxx.com', 'user2@xxx.com'], title='title', info='info')
