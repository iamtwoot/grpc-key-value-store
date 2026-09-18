import time

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


def main() -> None:
    with grpc.insecure_channel("localhost:8000") as channel:
        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)

        stub.Put(kvstore_pb2.PutRequest(key="a", value="1", ttl_seconds=0))
        print("Put ok")

        try:
            response = stub.Get(kvstore_pb2.GetRequest(key="a"))
            print("Get:", response.value)
        except grpc.RpcError as e:
            print("Get failed:", e.code(), e.details())

        stub.Put(kvstore_pb2.PutRequest(key="user:1", value="alice", ttl_seconds=0))
        stub.Put(kvstore_pb2.PutRequest(key="user:2", value="bob", ttl_seconds=2))
        stub.Put(kvstore_pb2.PutRequest(key="cfg:a", value="on", ttl_seconds=0))

        print(stub.Get(kvstore_pb2.GetRequest(key="user:1")).value)
        print(stub.List(kvstore_pb2.ListRequest(prefix="user:")).items)

        stub.Delete(kvstore_pb2.DeleteRequest(key="no-such-key"))  # не должен падать

        time.sleep(2.5)
        try:
            stub.Get(kvstore_pb2.GetRequest(key="user:2"))
        except grpc.RpcError as e:
            print("expired:", e.code())


if __name__ == "__main__":
    main()
