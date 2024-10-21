import socket
import threading
import time
from normal_data import data_list

send_interval = 0.016   # 데이터 전송 주기
thread_number = 100     # 장비 개수
max_total_count = 30000 # 모든 스레드가 전송할 총 데이터 개수

total_count = 0
count_lock = threading.Lock()

def handle_client(client_socket, address):
    global total_count
    print(f"Connection from {address} has been established.")
    try:
        while True:
            for normal_data in data_list:
                with count_lock:
                    if total_count >= max_total_count:
                        time.sleep(1)
                        continue
                try:
                    # 사용자 정의 데이터를 클라이언트에게 전송
                    client_socket.sendall(normal_data)
                    with count_lock:
                        total_count += 1
                        print(f"Total sends: {total_count}")
                    time.sleep(send_interval)
                except OSError as e:
                    print(f"Error sending data: {e}")
                    return  # 소켓 오류 발생 시 루프 종료
    except ConnectionResetError:
        print(f"Connection reset by {address}")
    except OSError as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()
        print(f"Connection from {address} closed.")

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(thread_number)  # Listen for a single connection
    print(f"Server listening on port {port}")
    
    
    while True:
        client_socket, address = server.accept()
        print(f"Accepted connection from {address}")    
   
        # 클라이언트가 연결되면 thread_number개의 스레드를 생성하여 handle_client 호출
        threads = []
        for _ in range(thread_number):
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
            threads.append(thread)
        
        # 모든 스레드가 종료될 때까지 대기
        for thread in threads:
            thread.join()
        
def create_virtual_servers(start_port, num_servers):
    threads = []
    for i in range(num_servers):
        port = start_port + i
        thread = threading.Thread(target=start_server, args=(port,))
        thread.start()
        threads.append(thread)
    return threads

if __name__ == "__main__":
    start_port = 10000
    num_servers = 1
    print(f"thread number: {thread_number}")
    threads = create_virtual_servers(start_port, num_servers)
    for thread in threads:
        thread.join()