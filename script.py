from web3 import Web3
import json
import time

# Infomacion importante

private_key = "ac7863650f40c33dc3b994ea94d803f8477a9000e63597e667c82157da79c0eb"
cuenta = "0x00aa634A97d1392ED915527d3986246d6fD02384"

infura_url = "https://sepolia.infura.io/v3/36b2ba4be08f4b408ae786cf03f108ed"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Dirección del contrato y su ABI
contract_address = "0x2D945b051eDF0cA1D03a7f0963fCa9deEA50C33F"

abi = '''[
    {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"modificadaPor","type":"address"},
    {"indexed":false,"internalType":"uint256","name":"nuevoValor","type":"uint256"}],"name":"ContadorModificado","type":"event"},
    {"inputs":[{"internalType":"address","name":"cuenta","type":"address"}],"name":"AddToWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"cantidad","type":"uint256"}],"name":"decrementarContador","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"cantidad","type":"uint256"}],"name":"incrementarContador","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"obtenerContador","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"cuenta","type":"address"}],"name":"removeFromWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelist","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'''

# Crear una instancia del contrato
contract = w3.eth.contract(address=contract_address, abi=abi)

# a- Leer la información del contrato
def leer_informacion():
    valor_contador = contract.functions.obtenerContador().call()
    print(f"Valor del contador: {valor_contador}")

# b- Escribir en el contrato 
def escribir_en_contrato(valor): 
    nonce = w3.eth.get_transaction_count(cuenta)
    if valor >= 0:
        transaccion = contract.functions.incrementarContador(valor).build_transaction({
            'chainId': 11155111,  
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
    else:
        transaccion = contract.functions.decrementarContador(valor).build_transaction({
            'chainId': 11155111,  
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

    signed_transaccion = w3.eth.account.sign_transaction(transaccion, private_key)  
    tx_hash = w3.eth.send_raw_transaction(signed_transaccion.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transacción exitosa. Nuevo valor del contador: {contract.functions.obtenerContador().call()}")

# c- Escuchar el evento y mostrar la información del evento cuando se dispara

def handle_event(event):
    print("Evento capturado")
    print(f"Evento 'ContadorModificado' capturado:")
    print(f"Modificado por: {event['args']['modificadaPor']}")
    print(f"Nuevo valor: {event['args']['nuevoValor']}")

def escuchar_evento():
    contract_event = contract.events.ContadorModificado.create_filter(fromBlock="latest")
    while True:
        for event in contract_event.get_new_entries():
            handle_event(event)
        time.sleep(10)


leer_informacion()
aumento=int(input("Ingrese el aumento del contador: "))
escribir_en_contrato(aumento) 
escuchar_evento() 