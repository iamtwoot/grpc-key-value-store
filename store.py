import threading
import time
from collections import OrderedDict
from typing import NamedTuple


class Entry(NamedTuple):
    value: str
    expires_at: float


class KVStore:
    def __init__(self, max_size: int = 10) -> None:
        self._lock = threading.Lock()
        self._store: OrderedDict[str, Entry] = OrderedDict()
        self._max_size = max_size

    def put(self, key: str, value: str, ttl_seconds: int) -> None:
        with self._lock:
            self._store[key] = Entry(
                value=value,
                expires_at=float("inf")
                if ttl_seconds == 0
                else time.monotonic() + ttl_seconds,
            )
            self._store.move_to_end(key)

            if len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def get(self, key: str) -> str | None:
        with self._lock:
            entry = self._store.get(key)

            if entry is None:
                return None

            if time.monotonic() > entry.expires_at:
                del self._store[key]
                return None

            self._store.move_to_end(key)
            return entry.value

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def list(self, prefix: str) -> list[tuple[str, str]]:
        with self._lock:
            results = []
            current_time = time.monotonic()
            for key, entry in self._store.items():
                if current_time > entry.expires_at:
                    continue

                if key.startswith(prefix):
                    results.append((key, entry.value))

            return results
