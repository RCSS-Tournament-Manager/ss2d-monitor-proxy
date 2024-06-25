import json
import logging
import os
from controller.context_model.proxy_info_context import ProxyInfoContext
from storage.storage_interface import IStorage

JSON_STORAGE_DEFAULT_PATH = "./data.json"

class JSONStorage(IStorage):
    def __init__(self, file_path: str = JSON_STORAGE_DEFAULT_PATH) -> None:
        self.file_path = file_path
        self.proxies: list[ProxyInfoContext] = []
        self.logging = logging.getLogger(__name__)
        self.initialize_storage()
        
    def initialize_storage(self) -> None:
        self.logging.info('Initializing storage')
        if os.path.exists(self.file_path):
            self.logging.info('File exists')
            with open(self.file_path, 'r') as file:
                self.parse_data(json.load(file))
        else:
            self.logging.info('File does not exist')
            with open(self.file_path, 'w') as file:
                json.dump({'proxies': []}, file)
            self.initialize_storage()
    
    def parse_data(self, data: dict) -> None:
        self.proxies = [ProxyInfoContext(**proxy) for proxy in data['proxies']]

    def add_proxy(self, proxy: ProxyInfoContext) -> None:
        self.logging.info(f'Adding proxy {proxy.__dict__}')
        self.proxies.append(proxy)
        self.flush()

    def remove_proxy(self, proxy: ProxyInfoContext) -> None:
        self.logging.info(f'Removing proxy {proxy.__dict__}')
        self.proxies.remove(proxy)
        self.flush()

    def get_all_proxies(self) -> list[ProxyInfoContext]:
        return self.proxies

    def remove_all_proxies(self) -> None:
        self.logging.info('Removing all proxies')
        self.proxies.clear()
        self.flush()
    
    def flush(self) -> None:
        self.logging.info('Flushing')
        with open(self.file_path, 'w') as file:
            json.dump({'proxies': [proxy.model_dump(mode='json') for proxy in self.proxies]}, file)