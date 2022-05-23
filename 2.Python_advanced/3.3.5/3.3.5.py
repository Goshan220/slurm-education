import re


def get_input():
    input_data = input().split(",")
    for proxy in input_data:
        proxy = re.sub(r'"| |\[|\]', '', proxy)
        yield proxy


def is_valid_proxy_number(proxy) -> bool:
    number = int(proxy[9:-9])
    if not number % 3 or not number % 8:
        return False
    else:
        return True


def do_request(proxy: str, counter: int):
    print(f"Было осуществлено обращение к ресурсу при помощи прокси {proxy}")
    counter += 1
    return counter


def wrong_understanded_solution():
    counter = 0
    while True:
        remaining_proxy_list = all_proxy.copy()
        for _ in range(len(remaining_proxy_list)):
            if counter < 1000:
                proxy = remaining_proxy_list.pop()
                print(f"Обращение при помощи прокси {proxy}")
                if is_valid_proxy_number(proxy):
                    counter = do_request(proxy, counter)
                else:
                    all_proxy.remove(proxy)
            else:
                print(remaining_proxy_list)
                exit(0)


if __name__ == '__main__':
    all_proxy = []
    for proxy in get_input():
        all_proxy.append(proxy)

    for count in range(1000):
        proxy = all_proxy.pop()
        print(f"Обращение при помощи прокси {proxy}")
        if is_valid_proxy_number(proxy):
            print(f"Было осуществлено обращение к ресурсу при помощи прокси {proxy}")
            all_proxy.insert(0, proxy)
    print(all_proxy)

# input example for debug
# ["proxyhost1.slurm.io", "proxyhost2.slurm.io", "proxyhost3.slurm.io", "proxyhost4.slurm.io", "proxyhost5.slurm.io", "proxyhost6.slurm.io", "proxyhost7.slurm.io", "proxyhost8.slurm.io", "proxyhost12.slurm.io", "proxyhost15.slurm.io"]
