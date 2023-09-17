import smtplib
import os


class NotificationManager:
    def __init__(self):
        self.email = os.environ.get("SMTP_EMAIL")
        self.passw = os.environ.get("SMTP_PASS")

    def sendMail(self, flight_data):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.passw)
            message = f"Only {flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}"
            connection.sendmail(from_addr=self.email, to_addrs=self.email,
                                msg=f"Subject:Low proce alert! \n\n{message}")
