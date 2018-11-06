instancias={}


def add_instancia(key,instancia):
    instancias[key]=instancia

def remove_instancia(key):
    global instancias
    new_instancias={new_key:instancias[key] for new_key in instancias.keys() if new_key!=key}
    instancias=new_instancias

def get_instancia(key):
    return instancias[key]