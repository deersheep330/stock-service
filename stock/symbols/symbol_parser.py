import json
from abc import ABC
import os
import grpc

from symbols.utils import get_grpc_hostname
from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Stock

class SymbolParser(ABC):

    def __init__(self):
        self.dict = None

    def parse(self):
        pass

    def get_dict(self):
        return self.dict

    def dump_to_file(self):

        if self.dict is None or len(self.dict) == 0:
            pass
        else:

            print(f'==> dump to file')

            filename = './symbols/dump/' + self.filename
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w+', encoding='utf-8') as f:
                json.dump(self.dict, f, ensure_ascii=False, indent=4)

        return self

    def update_db(self):

        if self.dict is None or len(self.dict) == 0:
            pass
        else:
            print(f'==> update db')
            try:
                channel = grpc.insecure_channel(f'{get_grpc_hostname()}:6565')
                stub = database_pb2_grpc.DatabaseStub(channel)
                rowcount = stub.upsert_stocks((Stock(symbol=key, name=value) for key, value in self.dict.items()))
                print(rowcount)
            except grpc.RpcError as e:
                status_code = e.code()
                print(e.details())
                print(status_code.name, status_code.value)

        return self
