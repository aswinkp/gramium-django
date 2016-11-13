# coding=latin-1
from dbclients.MySqlClient import MySqlClient
from sms.TwilioClient import TwilioClient
import datetime


class AppRunner:

    def run(self):
        print "Running App"
        mysql_client = MySqlClient()
        mysql_db_conn = mysql_client.getDatabaseConnection()
        mysql_cursor  = mysql_db_conn.cursor()
        current_day =str( datetime.date.today().day)
        query = "SELECT core_member.phone,core_loan.rate_of_interest,core_loan.monthly_installment " \
                "FROM core_member join core_loan where core_member.group_id=core_loan.group_id " \
                "AND core_loan.is_active=1 " \
                #"AND DATE_FORMAT(core_loan.date,'%d')=" + current_day
        mysql_cursor.execute(query)
        client = TwilioClient()
        result = mysql_cursor.fetchall()
        for row in result:
            to = '+91' + str(row[0])
            rate_of_interest = str(row[1])
            amount = str(row[2])
            body = ''
            client.sendSMS(to=to, from_="(267) 433-0959", body=body)
        return

if __name__ == "__main__":
    app = AppRunner()
    app.run()