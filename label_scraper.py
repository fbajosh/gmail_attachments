import imapclient
import email
from email.header import decode_header

username = 'email@gmail.com'
password = 'app-specific-password'

label_name = 'specify-label'

server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
server.login(username, password)

server.select_folder(label_name)

messages = server.search('has:attachment')

for uid in messages:
    raw_email = server.fetch(uid, ['BODY.PEEK'])
    email_message = email.message_from_bytes(raw_email[uid][b'BODY.PEEK'])
    attachments = email_message.get_all('attachment')

    for attachment in attachments:
        content_type, filename = decode_header(attachment.get('Content-Disposition'))[0]
        filename = filename.decode('utf-8')
        attachment_data = attachment.get_payload(decode=True)
        with open(filename, 'wb') as f:
            f.write(attachment_data)

server.logout()
