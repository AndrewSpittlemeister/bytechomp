import socket
from typing import Final
from threading import Thread, Event

from bytechomp import dataclass, Reader, serialize, Annotated

HOST: Final[str] = "127.0.0.1"
PORT: Final[int] = 55555


@dataclass
class PingRequest:
    request_id: int
    data: Annotated[bytes, 4]


@dataclass
class PingResponse:
    request_id: int
    data: Annotated[bytes, 4]


def run_server(ready: Event) -> None:
    # construct reader for requests
    reader = Reader[PingRequest]().allocate()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))

        ready.set()

        sock.listen()
        conn, addr = sock.accept()

        with conn:
            print(f"server received connection from {addr}")

            while True:
                if reader << conn.recv(1024):

                    request = reader.build()
                    print(f"server received request: {request}")

                    response = PingResponse(request.request_id, data=b"PONG")
                    print(f"server sending response: {response}")

                    conn.sendall(serialize(response))
                    break


def run_client(ready: Event) -> None:
    ready.wait()

    # construct reader for responses
    reader = Reader[PingResponse]().allocate()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"client connected to server at {(HOST, PORT)}")

        request = PingRequest(15, b"PING")
        print(f"client sending request: {request}")

        sock.sendall(serialize(request))

        reader << sock.recv(1024)

        if not reader.is_complete():
            print(f"client failed to received response from server")
            return

        response = reader.build()
        print(f"client received response: {response}")


def main() -> None:
    ready = Event()
    server_thread = Thread(target=run_server, args=(ready,))
    client_thread = Thread(target=run_client, args=(ready,))

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    main()
