from src.client import HDFSClient

# hdfs dfs -mkdir -p /user/root
# hdfs dfs -ls /


# или namenode:8020
STUB_HOST = 'localhost'
STUB_PORT = 9870
STUB_USER = 'some_user'


def get_client(host: str, port: int, user: str) -> HDFSClient:
    return HDFSClient(host, port, user)


if __name__ == '__main__':
    client = get_client(STUB_HOST, STUB_PORT, STUB_USER)
