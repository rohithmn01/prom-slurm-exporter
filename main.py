from prometheus_client import REGISTRY
from prometheus_client import start_http_server
import time

import nodes
REGISTRY.register(nodes.NodeInfoCollector())


if __name__ == "__main__":
    start_http_server(9009)
    while True:
        time.sleep(60)
