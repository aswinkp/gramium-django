# coding=latin-1
from dbclients.MySqlClient import MySqlClient
from sms.TwilioClient import TwilioClient
import datetime


class AppRunner:

    def pre_due_sms(self, due_day):
        client = TwilioClient()
        mysql_client = MySqlClient()
        mysql_db_conn = mysql_client.getDatabaseConnection()
        mysql_cursor  = mysql_db_conn.cursor()

        query = "SELECT core_member.phone, core_loan.due_date, core_loan.monthly_installment " \
                "FROM core_member join core_loan where core_member.group_id=core_loan.group_id " \
                "AND core_loan.is_active=1 " \
                "AND DATE_FORMAT(core_loan.due_date,'%d')=" + due_day

        #date = #update date for installment payment
        mysql_cursor.execute(query)
        result = mysql_cursor.fetchall()
        for row in result:
            to = '+91' + str(row[0])
            due_date = str(row[1])
            due_year_diff = datetime.date.today().year - int(due_date.split("-")[0])
            due_month_diff = datetime.date.today().month - int(due_date.split("-")[1])
            amount = str(row[2] * (due_year_diff*12 + (due_month_diff + 1)))
            body = "கிராமியம் : உங்கள் தவணைத் தொகை   ₹."+ amount + " யை, " + due_date + "ஆம் தேதிக்குள் செலுத்தவும்"
            client.sendSMS(to=to, from_="(267) 433-0959", body=body)
        mysql_client.closeConnection()

    def post_due_sms(self, due_day):
        client = TwilioClient()
        mysql_client = MySqlClient()
        mysql_db_conn = mysql_client.getDatabaseConnection()
        mysql_cursor  = mysql_db_conn.cursor()

        query = "SELECT core_member.phone, core_loan.due_date, core_loan.monthly_installment " \
                "FROM core_member join core_loan where core_member.group_id=core_loan.group_id " \
                "AND core_loan.is_active=1 " \
                "AND DATE_FORMAT(core_loan.due_date,'%d') =" + str(due_day) \
                +" AND core_loan.due_date < cast(now() as date) "

        #date = #update date for installment payment
        mysql_cursor.execute(query)
        result = mysql_cursor.fetchall()
        for row in result:
            to = '+91' + str(row[0])
            body = "தவணை தொகை கட்டா விட்டதால் அடுத்த மாதம் அபாதாரம் செலுத்த வேண்டும்"
            client.sendSMS(to=to, from_="(267) 433-0959", body=body)
        mysql_client.closeConnection()

    def run(self):
        print "Running App"

        current_day = str( datetime.date.today().day)
        if current_day=="1" or current_day=="3":
            due_day = "5"
            self.pre_due_sms(due_day)
        elif current_day=="11" or current_day=="13":
            due_day = "15"
            self.pre_due_sms(due_day)
        else:
            due_day = "-1"
            self.pre_due_sms(due_day)


        if current_day=="6":
            due_day = "5"
            self.post_due_sms(due_day)
        elif current_day=="16":
            due_day = "15"
            self.post_due_sms(due_day)
        else:
            due_day = "-1"
            self.post_due_sms(due_day)

        return

if __name__ == "__main__":
    app = AppRunner()
    app.run()
