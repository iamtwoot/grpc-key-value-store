FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY kvstore_pb2.py kvstore_pb2_grpc.py store.py server.py ./

CMD ["uv", "run", "--no-sync", "python", "server.py"]
