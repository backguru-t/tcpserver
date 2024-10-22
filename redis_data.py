import base64
import binascii
import redis
import os
import json

# Redis 연결 설정
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

# Redis 클라이언트 생성
client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# 채널 번호 범위
channel_range = range(1, 11)

# 파일을 저장할 디렉토리 경로 (현재 작업 디렉토리)
save_dir = 'redis_data'
os.makedirs(save_dir, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성

def chunk_list(data, chunk_size):
    """리스트를 chunk_size 크기로 나눕니다."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# 각 채널에 대한 데이터 읽기 및 파일 저장
for ch_num in channel_range:
    key = f"GM4000:1:0281:{ch_num}"
    file_path = os.path.join(save_dir, f"channel_{ch_num}.json")

    # Redis 스트림에서 데이터 읽기
    data = client.xrange(key)
    
    # 엔트리 개수 로그 출력
    entry_count = len(data)
    print(f"Key: {key}, Entry count: {entry_count}")

    # 데이터 저장
    with open(file_path, 'w') as f:
        json_data = []
        for entry in data:
            entry_id, entry_data = entry
            data_list = list(entry_data[b'data'])  # 바이트 배열을 정수 배열로 변환
            chunked_data = chunk_list(data_list, 16)  # 16개씩 나누기
            formatted_data = [', '.join(map(str, chunk)) for chunk in chunked_data]  # 16개씩 가로로 표시
            json_entry = {
                'timestamp': entry_data[b'timestamp'].decode('utf-8'),
                'channel': entry_data[b'channel'].decode('utf-8'),
                'data': formatted_data  # 바이트 배열을 정수 배열로 변환
            }
            json_data.append(json_entry)
        json.dump(json_data, f, indent=4, separators=(',', ': '))

    print(f"Data for channel {ch_num} written to {file_path}")