# information_string.py
class information_string:
    _instance = None  # Class variable to store the instance

    def __new__(cls):
        # Create a new instance only if it doesn't exist
        if cls._instance is None:
            cls._instance = super(information_string, cls).__new__(cls)
            cls._instance._get_memory_info = None
            cls._instance._get_cpu_temp = None
            cls._instance._get_cpu_percentage = None
            cls._instance._get_system_info = None
            cls._instance._get_os_info = None
            cls._instance._get_process_list = None
            cls._instance._get_cpu_count = None
            cls._instance._get_cpu_main_core = None
            cls._instance._storage = None
            cls._instance._net_cnn = None
            cls._instance._get_date = None
            cls._instance._get_time = None
        return cls._instance

    @classmethod
    def update_memory_info(cls, new_ip):
        cls._instance._get_memory_info = new_ip

    @classmethod
    def update_cpu_temp(cls, new_name):
        cls._instance._get_cpu_temp = new_name
    
    @classmethod
    def update_cpu_percentage(cls, new_name):
        cls._instance._get_cpu_percentage = new_name
    
    @classmethod
    def update_system_info(cls, new_name):
        cls._instance._get_system_info = new_name
        
    @classmethod
    def update_os_info(cls, new_name):
        cls._instance._get_os_info = new_name

    @classmethod
    def update_process_list(cls, new_name):
        cls._instance._get_process_list = new_name

    @classmethod
    def update_cpu_count(cls, new_name):
        cls._instance._get_cpu_count = new_name

    @classmethod
    def update_cpu_main_core(cls, new_name):
        cls._instance._get_cpu_main_core = new_name

    @classmethod
    def update_storage(cls, new_name):
        cls._instance._storage = new_name

    @classmethod
    def update_network_connections(cls, new_name):
        cls._instance._net_cnn = new_name

    @classmethod
    def update_date(cls, new_name):
        cls._instance._get_date = new_name

    @classmethod
    def update_time(cls, new_name):
        cls._instance._get_time = new_name

    @classmethod
    def get_time(cls):
        return cls._instance._get_time

    @classmethod
    def get_date(cls):
        return cls._instance._get_date

    @classmethod
    def get_memory_info(cls):
        return cls._instance._get_memory_info

    @classmethod
    def get_cpu_temp(cls):
        return cls._instance._get_cpu_temp

    @classmethod
    def get_cpu_percentage(cls):
        return cls._instance._get_cpu_percentage

    @classmethod
    def get_system_info(cls):
        return cls._instance._get_system_info
    
    @classmethod
    def get_os_info(cls):
        return cls._instance._get_os_info
    
    @classmethod
    def get_process_list(cls):
        return cls._instance._get_process_list
    
    @classmethod
    def get_cpu_count(cls):
        return cls._instance._get_cpu_count
    
    @classmethod
    def get_cpu_main_core(cls):
        return cls._instance._get_cpu_main_core
    
    @classmethod
    def get_storage(cls):
        return cls._instance._storage

    @classmethod
    def get_network_connections(cls):
        return cls._instance._net_cnn