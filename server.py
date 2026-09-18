from concurrent import futures

import grpc

import kvstore_pb2
import kvstore_pb2_grpc
from store import KVStore


class KeyValueStoreServicer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, store: KVStore) -> None:
        self._store = store

    def Put(self, request, context):
        if request.ttl_seconds < 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "ttl_seconds must be non-negative",
            )

        self._store.put(request.key, request.value, request.ttl_seconds)
        return kvstore_pb2.PutResponse()

    def Get(self, request, context):
        value = self._store.get(request.key)
        if value is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "key not found")

        return kvstore_pb2.GetResponse(value=value)

    def Delete(self, request, context):
        self._store.delete(request.key)
        return kvstore_pb2.DeleteResponse()

    def List(self, request, context):
        items = [
            kvstore_pb2.KeyValue(key=key, value=value)
            for key, value in self._store.list(request.prefix)
        ]
        return kvstore_pb2.ListResponse(items=items)


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(KVStore()), server
    )
    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
