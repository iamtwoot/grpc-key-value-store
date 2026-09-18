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


if __name__ == "__main__":
    main()
