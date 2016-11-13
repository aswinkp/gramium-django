# coding=latin-1
from dbclients.MySqlClient import MySqlClient
from sms.TwilioClient import TwilioClient
import datetime


class AppRunner:

    def diff_month(d1, d2):
        return (d1.year - d2.year)*12 + d1.month - d2.month

    def run(self):
        print "Running App"
        mysql_client = MySqlClient()
        mysql_db_conn = mysql_client.getDatabaseConnection()
        mysql_cursor  = mysql_db_conn.cursor()
        current_day = str( datetime.date.today().day)
        if current_day=="1" or current_day=="3":
            due_day = "5"
        else:
            due_day = "15"

        query = "SELECT core_member.phone, core_loan.due_date, core_loan.monthly_installment " \
                "FROM core_member join core_loan where core_member.group_id=core_loan.group_id " \
                "AND core_loan.is_active=1 " \
                "AND DATE_FORMAT(core_loan.due_date,'%d')=" + due_day

        #date = #update date for installment payment
        mysql_cursor.execute(query)
        client = TwilioClient()
        result = mysql_cursor.fetchall()
        for row in result:
            to = '+91' + str(row[0])
            due_date = str(row[1])
            due_year_diff = datetime.date.today().year - int(due_date.split("-")[0])
            due_month_diff = datetime.date.today().month - int(due_date.split("-")[1])
            amount = str(row[2] * (due_year_diff*12 + (due_month_diff + 1)))
            body = "கிராமியம் : உங்கள் தவணைத் தொகை   ₹."+ amount + " யை, " + due_date + "ஆம் தேதிக்குள் செலுத்தவும்"
            client.sendSMS(to=to, from_="(267) 433-0959", body=body)
        return

if __name__ == "__main__":
    app = AppRunner()
    app.run()