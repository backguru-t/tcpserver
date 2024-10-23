# TCP 가상 서버

TCP 가상 서버로 사용자 정의 데이터를 연결된 클라이언트에 전송하고 수신된 데이터를 검증하는 프로젝트

## gm4000.py

서버로 동작하는 가상의 장비를 구현한 프로그램으로 normal_data.py에 정의된 데이터를 연속적으로 전송하는 프로그램으로 다음의 파라미터를 사용자가 조정할 수 있다.

```python
send_interval = 0.016       # 데이터 전송 주기
thread_number = 100         # 장비 개수
max_total_count = 30000     # 모든 스레드가 전송할 총 데이터 개수
start_port = 10000          # 시작 포트 번호
file_path = 'sent_data.bin' # working directory에 저장
```
서버는 전송한 데이터를 file_path에 정의된 파일이름으로 저장된다.

## redis_data.py

레디스에서 특정 키 값에 대한 데이터를 취득하고 키 값 마다 파일을 생성하여 Json형태로 저장하는 프로그램이다.
아래와 같이 레디스 키를 정의하고 엔트리 데이터를 취득하는 코드가 있다.

```python
key = f"GM4000:1:0281:{ch_num}"     # 키 설정

json_entry = {                  
    'channel': entry_data[b'channel'].decode('utf-8'),
    'data': formatted_data  # 바이트 배열을 정수 배열로 변환
}
```

## convert_bin_to_json.py

서버에서 전송한 데이터를 파일로 저장하고 해당 파일을 파싱하여 Json형태의 신규 파일을 생성하는 프로그램이다. 이것은 수신 장비가 레디스에 저장하는 동작이 올바르게 동작하는지 확인하기 위한 데이터 무결성 테스트를 진행하는 데 사용된다. 즉, gm4000.py에서 생성한 파일을 파싱하여 Json 파일을 만들고 redis_data.py에서 생성한 Json파일을 beyond compare 등으로 파일 비교를 해서 데이터 무결성을 확인할 수 있다.

## normal_data.py

해당 코드는 서버가 전송할 데이터를 생성하는 파일이다.

