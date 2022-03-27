import json

from data import db_session
from data.messages import Message


def main():
    db_session.global_init("db/main.db")
    db_sess = db_session.create_session()
    messages = db_sess.query(Message).filter()
    messages_dict = {'messages': {msg.id: {'name': msg.user_name, 'email': msg.contact, 'text': msg.text,
                                           'created_date': msg.created_date.strftime("%H:%M:%S")} for msg in messages}}
    with open('messages.json', 'w') as f:
        json.dump(messages_dict, f)

if __name__ == '__main__':
    main()
