import time
import threading
import pyExcelerator
from DCheat_Server.tasks import send_chart_with_mail
from DCheat_Server.utils.selectQuery import select_end_course_for_chart, select_user_in_end_course, select_master_email

class chart(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(1800)

            courseList = select_end_course_for_chart()

            if len(courseList) is not 0:
                for course in courseList:
                    wb, sheet, style = self.setChart(course)
                    userInfo = select_user_in_end_course(course.index)

                    if len(userInfo) is 0:
                        wb.save()
                        continue

                    posY = 2
                    for info in userInfo:
                        sheet.write(posY, 0, info.name, style)
                        sheet.write(posY, 1, info.firstLogin, style)
                        sheet.write(posY, 2, info.lastLogin, style)
                        sheet.write(posY, 3, info.lastLogout, style)

                        posX = 4
                        procList = info.individualInfomation.split('*')

                        for proc in procList:
                            sheet.write(posY, posX, proc, style)
                            posX += 1

                        posY += 1

                    wb.save()
                    send_chart_with_mail.delay(select_master_email(course.testName)[0]) #path 추가

    def setChart(self, course):
        align = pyExcelerator.Alignment()
        wb = pyExcelerator.Workbook()

        align.horz = pyExcelerator.Alignment.HORZ_CENTER
        align.vert = pyExcelerator.Alignment.VERT_CENTER

        fontStyle = pyExcelerator.XFStyle()
        fontStyle.alignment = align

        sheet = wb.add_sheet("Sheet1")

        sheet.write_merge(0, 0, 3, 5, course.testName, fontStyle)
        sheet.write(1, 0, '이름', fontStyle)
        sheet.write(1, 1, '최초 로그인 시간', fontStyle)
        sheet.write(1, 2, '최근 로그인 시간', fontStyle)
        sheet.write(1, 3, '최종 로그아웃 시간', fontStyle)
        sheet.write(1, 4, '추가 의심 프로세스', fontStyle)

        return wb, sheet, fontStyle