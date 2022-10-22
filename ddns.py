import json
from os.path import exists
import requests

ZONE_ID = ""
RECORD_ID = ""
RECORD_NAME = ""
USER_EMAIL = ""
API_KEY = ""

def compare_ip(new_ip):
    # Verifica se o arquivo de ultimo ip existe
    file_exists = exists("last_ip.txt")
    if ( file_exists ):
        # lê o arquivo e compara com o IP atual
        f = open("last_ip.txt", "r")
        # Verifica se o IP atual é igual ao antigo
        if ( f.read() == new_ip ):
            return True
        else:
            f = open("last_ip.txt", "w")
            f.write(new_ip)
            f.close()
            return False
    else:
        f = open("last_ip.txt", "a")
        f.write(new_ip)
        f.close()
        return False

def get_ip() -> str:
    """
    get the ip address of whoever executes the script
    """
    url = "https://api.ipify.org"
    response = requests.get(url)
    return str(response.text)


def set_ip(current_ip: str):
    """
    sets the ip in via cloudflare api
    """
    zone_id = ZONE_ID
    record_id = RECORD_ID

    url = (
        "https://api.cloudflare.com/client/v4/zones/%(zone_id)s/dns_records/%(record_id)s"
        % {"zone_id": zone_id, "record_id": record_id}
    )

    api_key = API_KEY
    user_email = USER_EMAIL
    record_name = RECORD_NAME

    headers = {
        "X-Auth-Email": user_email,
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }

    payload = {"type": "A", "name": record_name, "content": current_ip}
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    print("requisição enviada!\n")
    print(response.status_code)


def main():
    current_ip = get_ip()
    if ( compare_ip(current_ip) == False ):
        set_ip(current_ip)
    else:
        print("Não é necessário alterar o IP!")


if __name__ == "__main__":
    main()