# RaspInfo.py
class RaspInfo:
    _instance = None  # Class variable to store the instance

    def __new__(cls):
        # Create a new instance only if it doesn't exist
        if cls._instance is None:
            cls._instance = super(RaspInfo, cls).__new__(cls)
            cls._instance._rasp_ip = None
            cls._instance._rasp_port = None
            cls._instance._rasp_name = None
            cls._instance._rasp_password = None
        return cls._instance

    @classmethod
    def update_config(cls, new_ip, new_port,new_name,new_password):
        cls._instance._rasp_ip = new_ip
        cls._instance._rasp_port = new_port
        cls._instance._rasp_name=new_name
        cls._instance._rasp_password=new_password

    @classmethod
    def update_info(cls, new_name, new_password,):
        cls._instance._rasp_name = new_name
        cls._instance._rasp_password = new_password
        

    @classmethod
    def get_rasp_ip(cls):
        return cls._instance._rasp_ip

    @classmethod
    def get_rasp_port(cls):
        return cls._instance._rasp_port

    @classmethod
    def get_rasp_name(cls):
        return cls._instance._rasp_name

    @classmethod
    def get_rasp_password(cls):
        return cls._instance._rasp_password
