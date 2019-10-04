import src.mail.core as mail
import src.db.jokes as jokes
import src.db.core as db
from src.mail.secret import YAHOO_USER as USER, YAHOO_PWD as PASSWORD

conn = db.get_jokes_app_connection()


df_joke = jokes.get_random_joke_not_sent_by_mail_already(conn)
s_joke = df_joke["joke"][0].replace("\n", "<br>")
joke_id = int(df_joke["id"][0])

is_sent = mail.send_mail(USER, PASSWORD, mail.RECEIVERS, s_joke, mail.SUBJECT, provider='smtp')

if is_sent:
    jokes.put_sent_joke_db(conn, joke_id)
    print("Mail sent!")
else:
    print("Mail not sent!!")
