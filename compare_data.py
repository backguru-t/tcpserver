def compare_data(sent_data_file, received_data_file):
    with open(sent_data_file, 'rb') as f:
        sent_data = f.read()

    with open(received_data_file, 'rb') as f:
        received_data = f.read()

    if sent_data == received_data:
        print("Data integrity test passed: Sent data and received data are identical.")
    else:
        print("Data integrity test failed: Sent data and received data are different.")

if __name__ == "__main__":
    compare_data('sent_data.bin', 'gm4000.bin')