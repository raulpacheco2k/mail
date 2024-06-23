from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from smtplib import SMTP

import OpenSSL

certificate_directory = "."

days_of_advance_notice = 30

application_name = "Foo bar"

sender = "from@example.com"
receivers = [
    "foo@example.com",
    "bar@example.com",
]

host = "sandbox.smtp.example.io"
port = 0000
user = "user"
password = "password"

for filename in Path(certificate_directory).rglob("*.pem"):
    with open(filename, "rb") as file:
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, file.read())
        timestamp = x509.get_notAfter().decode('utf-8')
        certificate_expiration_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').date()
        days_to_expire = (certificate_expiration_date - datetime.now().date()).days

        if days_to_expire < days_of_advance_notice:

            subject = f"{application_name}: Certificado SSL irá expirar em {days_to_expire} dias ou já expirado."
            message = (f"Gostaríamos de informá-lo(a) que o certificado {filename} do projeto {application_name} "
                       f"expirará em {days_to_expire} dias, no dia {certificate_expiration_date.strftime('%d/%m/%Y')}.")

            for receiver in receivers:
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                with SMTP(host, port) as server:
                    server.starttls()
                    server.login(user, password)
                    server.sendmail(sender, receiver, msg.as_string())
