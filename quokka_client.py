import json
import requests
import urllib3
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
QUOKKA_URL = "http://quokka1.quokkacomputing.com/qsim/qasm"
 
def run_on_quokka(qasm_str: str) -> str:
    # send the circuit and return the measurement bitstring
    data = {"script": qasm_str, "count": 1}
    result = requests.post(QUOKKA_URL, json=data, verify=False)
    json_obj = json.loads(result.content)
    return ''.join(map(str, json_obj['result']['c'][0]))
 