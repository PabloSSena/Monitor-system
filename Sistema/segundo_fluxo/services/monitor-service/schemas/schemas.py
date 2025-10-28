def individual_serial(host) -> dict:
    return {
        "chat_id": str(host["chat_id"]),
        "url": host["url"],
    }
    

def list_serial(hosts) -> list:
    return [individual_serial(host) for host in hosts]

def list_hosts(hosts) -> list:
    print('hosts in schema:', hosts)
    return [host['url'] for host in hosts]