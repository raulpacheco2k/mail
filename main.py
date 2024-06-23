from datetime import datetime
from pathlib import Path
from smtplib import SMTP

import OpenSSL

cert_directory = "path/to/certificates"
dias_aviso = 30
data_atual = datetime.now()
aplicacao = "Aplicacao"

assunto = f"Certificados SSL prestes a expirar em {dias_aviso} dias ou expirados na aplicação {aplicacao}"

for filename in Path(".").rglob("*.pem"):
    print(filename)
    with open(filename, "rb") as file:
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, file.read())
        timestamp = x509.get_notAfter().decode('utf-8')
        data_certificado = datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').date()
        data_atual = datetime.now().date()
        emitir_aviso = (data_certificado - data_atual).days < dias_aviso
        print(emitir_aviso)

        if emitir_aviso:
            sender = "from@example.com"
            receiver = "to@example.com"

            message = "Hello World!"

            with SMTP("host", 0000) as server:
                server.starttls()
                server.login("user", "password")
                server.sendmail(sender, receiver, message)
