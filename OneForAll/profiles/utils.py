import uuid

def get_randomcode():
    code = str(uuid.uuid5())[:8].replace('-','').lower()
    return code