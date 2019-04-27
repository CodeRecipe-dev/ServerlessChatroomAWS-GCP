import json
import os

class MessagesStore:
    def __init__(self, ddb):
        self._ddb = ddb
        table_name = os.environ["MESSAGES_TABLE"]
        self._messages_table = self._ddb.Table(table_name)

    def add_new_message(self, **params):
        if 'message' not in params:
            raise Exception("message not exist in params:{}".format(json.dumps(params)))
        item = {'date': json.dumps(params['date']), 'timestamp': json.dumps(params['timestamp']), 'message': json.dumps(params['message'])}
        response = self._messages_table.put_item(
            Item=item
        )

    def get_messages(self):
        response = self._messages_table.scan()
        items = response['Items']
        return items

def main():
    pass

if __name__ == "__main__":
    main()
