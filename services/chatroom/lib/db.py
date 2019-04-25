import json
import os

class ConnectionsStore:
    def __init__(self, ddb):
        self._ddb = ddb
        table_name = os.environ["CONNECTIONS_TABLE"]
        self._connections_table = self._ddb.Table(table_name)

    def add_new_connection(self, **params):
        if 'connectionId' not in params:
            raise Exception("connectionId not exist in params:{}".format(json.dumps(params)))
        item = {'connectionId': params['connectionId']}
        response = self._connections_table.put_item(
            Item=item
        )

    def remove_connection(self, **params):
        if 'connectionId' not in params:
            raise Exception("connectionId not exist in params:{}".format(json.dumps(params)))
        item = {'connectionId': params['connectionId']}
        response = self._connections_table.delete_item(
            Key=item
        )

    def get_connections(self):
        response = self._connections_table.scan()
        items = response['Items']
        return items

def main():
    pass

if __name__ == "__main__":
    main()
