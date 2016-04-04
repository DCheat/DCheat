# -*-coding: utf-8 -*-
from __future__ import absolute_import

from DCheat_Server.celeryServer import app

@app.task(name = 'task.send_mail')
def send_mail(stdCode, stdName, programName, score, adminAddress):
    import smtplib
    from email.mime.text import MIMEText

    serverAddress = 'DCheat@dcheat.com'

    contents = '''
    %s(%s) 학생이 허용하지 않은 프로그램(%s)%s
    해당 학생에 대해 지도가 %s




    발신 전용 메일 주소 입니다.
    '''

    if score > 10:
        stdAction = '을 사용했습니다.'
        adminAction = '필요합니다.'

    else:
        stdAction = '의 사용이 의심됩니다.'
        adminAction = '필요할 수 있습니다.'

    contents = contents % (stdCode, stdName, programName, stdAction, adminAction)

    message = MIMEText(contents, _charset='utf-8')
    message['Subject'] = '%s(%s)의 허용하지 않은 프로그램 사용이 포착됐습니다.'%(stdCode, stdName)
    message['From'] = serverAddress
    message['To'] = adminAddress

    s = smtplib.SMTP('localhost')
    s.sendmail(serverAddress, [adminAddress], message.as_string())
    s.quit()

@app.task(name = 'task.send_char_with_mail')
def send_chart_with_mail(adminAddress, filePath):
    pass