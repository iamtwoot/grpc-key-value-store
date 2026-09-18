from concurrent import futures

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


class KeyValueStoreServicer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def Put(self, request, context):
        return kvstore_pb2.PutResponse()

    def Get(self, request, context):
        context.abort(grpc.StatusCode.NOT_FOUND, "key not found")

    def Delete(self, request, context):
        return kvstore_pb2.DeleteResponse()

    def List(self, request, context):
        return kvstore_pb2.ListResponse()


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(), server
    )
    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
