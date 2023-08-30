import hashlib
import json
import socket
import threading

# Definición de un bloque
def create_block(prev_hash, transactions):
    block = {
        'prev_hash': prev_hash, #hash bloque anterior
        'transactions': transactions,
        'timestamp': 'some_timestamp'
    }
    block_string = json.dumps(block, sort_keys=True).encode() #Psamos la info de block a JSON
    block['hash'] = hashlib.sha256(block_string).hexdigest() 
    return block

# Blockchain inicial
blockchain = [create_block('genesis', ['tx1', 'tx2'])]

# Manejar conexiones entrantes
def handle_client(client_socket):
    global blockchain
    request = client_socket.recv(1024) #Datos que recibe
    new_block = json.loads(request.decode('utf-8')) #se encarga de convertir 
    
    # Validar y añadir el nuevo bloque (si el hash del bloque anterior 
    # (prev_hash) en el nuevo bloque coincide con el hash del último bloque en la blockchain actual.)
    last_block = blockchain[-1]
    if new_block['prev_hash'] == last_block['hash']:
        blockchain.append(new_block)
        print("Nuevo bloque añadido:", new_block)
    else:
        print("Bloque inválido")

    client_socket.close()  #Cierra la conexion del cliente

# Iniciar servidor P2P
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #los socket permiten que diferentes maquinas se conecten entre ellas
    server.bind(("0.0.0.0", 9996)) #Lo de arriba se enlaza #la ip y ekl puerto son componentes del socket
    server.listen(5) #conexiones entrantes escuchadas
    print("Esperando conexiones...")
    
    while True: #Para ceptar conexiones indefinidamente
        client_sock, addr = server.accept() #Esta aceptando la conecion t obtiene los datos (los del socket)
        print(f"Conexión aceptada de: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_sock,)) #Ae cre un nuevo hilo para la nueva conexion
        client_handler.start()

# Conectar a otro nodo y enviar un bloque a otros nodos
def connect_to_node(host, port, block):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port)) #Se establece conexin con el nodo
    client.send(json.dumps(block).encode()) #Se serializa en cadena JSON, se codifica a bytes y se envia al nodo onjetivo

# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Crear un nuevo bloque y enviarlo a otro nodo (para probar)
new_block = create_block(blockchain[-1]['hash'], ['tx3', 'tx4'])
# enviar el nuevo bloque a otro nodo
connect_to_node("127.0.0.1", 9998, new_block)
