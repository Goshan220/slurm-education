import queue
import threading
import time


def network_call(wait_for: int, queue: queue.Queue):
    time.sleep(wait_for)
    queue.put(wait_for)


def main():
    q = queue.Queue()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=network_call, args=(i, q))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(q.queue)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Completed at {time.time() - start_time}")
