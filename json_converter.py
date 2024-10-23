import json
import os

def parse_packet(packet):
    """패킷을 파싱하여 채널과 데이터를 추출합니다."""
    if len(packet) != 522:
        raise ValueError("Invalid packet length")

    channel = packet[6]
    data = packet[7:519]
    end_sequence = packet[519:522]

    # 엔드 시퀀스 확인
    if end_sequence != b'\x03\x0d\x0a':
        raise ValueError("Invalid end sequence")

    return channel, list(data)

def chunk_list(data, chunk_size):
    """리스트를 chunk_size 크기로 나눕니다."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# 파일 경로 설정
bin_file_path = 'sent_data.bin'
output_dir = 'converted_channels'

# 출력 디렉토리 생성
os.makedirs(output_dir, exist_ok=True)

# 바이너리 파일 읽기
with open(bin_file_path, 'rb') as f:
    binary_data = f.read()

# 패킷 크기
packet_size = 522

# 패킷 단위로 데이터 파싱
packets = [binary_data[i:i + packet_size] for i in range(0, len(binary_data), packet_size)]

# 채널별 데이터 저장
channel_data = {}
for packet in packets:
    try:
        channel, data = parse_packet(packet)
        chunked_data = chunk_list(data, 16)  # 16개씩 나누기
        formatted_data = [', '.join(map(str, chunk)) for chunk in chunked_data]
        json_entry = {
            'channel': str(channel),
            'data': formatted_data
        }
        if channel not in channel_data:
            channel_data[channel] = []
        channel_data[channel].append(json_entry)
    except ValueError as e:
        print(f"Error parsing packet: {e}")

# 채널별 JSON 파일 저장
total_entries = 0
for channel, data in channel_data.items():
    json_file_path = os.path.join(output_dir, f'channel_{channel}.json')
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '))
    entry_count = len(data)
    total_entries += entry_count
    print(f"Data for channel {channel} written to {json_file_path} with {entry_count} entries.")

# 총합 로그 출력
print(f"Total number of entries across all channels: {total_entries}") 