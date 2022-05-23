import time


def network_call(wait_for: int):
    time.sleep(wait_for)
    return wait_for


def main():
    for i in range(5):
        print(network_call(i))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Completed at {time.time() - start_time}")
