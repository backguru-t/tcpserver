import socket
import threading
import time
import os
from normal_data import data_list

send_interval = 0.016   # 데이터 전송 주기
thread_number = 100       # 장비 개수
max_total_count = 30000 # 모든 스레드가 전송할 총 데이터 개수
start_port = 10000      # 시작 포트 번호

total_count = 0
count_lock = threading.Lock()
sent_data = []
sent_data_lock = threading.Lock()

def handle_client(client_socket, address):
    global total_count
    print(f"Thread started for {address}")
    try:
        while True:
            for normal_data in data_list:
                with sent_data_lock:
                    if total_count >= max_total_count:
                        # time.sleep(1)
                        # continue
                        return
                try:
                    with sent_data_lock:
                        # 사용자 정의 데이터를 클라이언트에게 전송
                        client_socket.sendall(normal_data)
                        total_count += 1
                        print(f"Total sends: {total_count}")
                        sent_data.append(normal_data)
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
    server.listen(1)  # Listen for multiple connections
    print(f"Server listening on port {port}")
    
    client_socket, address = server.accept()
    print(f"Accepted connection from {address}")
            
    # thread_number개의 스레드를 생성하여 handle_client 호출
    threads = []
    for _ in range(thread_number):
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    server.close()
    
    # 파일을 저장할 디렉토리 경로
    # save_dir = './'
    # os.makedirs(save_dir, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성

    # 파일 경로
    # file_path = os.path.join(save_dir, 'sent_data.bin')
    
    file_path = 'sent_data.bin' # working directory에 저장
    
    # 서버가 종료될 때 sent_data 리스트를 파일로 저장
    with sent_data_lock:
        with open(file_path, 'wb') as f:
            for data in sent_data:
                f.write(data)
    print(f"Sent data written to {file_path}")

if __name__ == "__main__":
    print(f"thread number: {thread_number}, start port: {start_port}")
    start_server(start_port)