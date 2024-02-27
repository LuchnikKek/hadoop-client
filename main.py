from src.client import HDFSClient

STUB_HOST = 'localhost'
STUB_PORT = 9870
STUB_USER = 'some_user'


def get_client(host: str, port: int, user: str) -> HDFSClient:
    return HDFSClient(host, port, user)


if __name__ == '__main__':
    client = get_client(STUB_HOST, STUB_PORT, STUB_USER)
