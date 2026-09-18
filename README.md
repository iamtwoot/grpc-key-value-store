# KV Store (mini Redis) на gRPC

In-memory хранилище ключ-значение с TTL и LRU-вытеснением.

## Запуск

uv sync\
uv run python server.py

Сервер слушает порт 8000.

## Генерация кода из .proto

uv run python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. kvstore.proto

## Проверка

uv run python client.py    # базовый сценарий\
uv run python load.py      # параллельная нагрузка

## Реализация

- Хранилище: `OrderedDict`, TTL как абсолютный момент истечения, `inf` для ключей без TTL
- LRU: `move_to_end` при `Get` и `Put`, `popitem(last=False)` при превышении лимита в 10 ключей
- Потокобезопасность: один `threading.Lock` на хранилище