import threading

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


def worker(n: int) -> None:
    with grpc.insecure_channel("localhost:8000") as channel:
        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
        for i in range(200):
            stub.Put(
                kvstore_pb2.PutRequest(key=f"k{i % 20}", value=str(n), ttl_seconds=0)
            )
            try:
                stub.Get(kvstore_pb2.GetRequest(key=f"k{i % 20}"))
            except grpc.RpcError:
                pass


threads = [threading.Thread(target=worker, args=(n,)) for n in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

with grpc.insecure_channel("localhost:8000") as channel:
    stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
    items = stub.List(kvstore_pb2.ListRequest(prefix="k")).items
    print("keys in store:", len(items))