COMPANIES = ["southbridge.ru", "universe.slurm.io"]

USERS = ["d.krivosheev@slurm.io", "a.egorov@slurm.io", "a.gorina@slurm.io", "d.naumov@slurm.io",
         "a.amantaeva@slurm.io", "v.vostrikova@slurm.io"]

if __name__ == '__main__':
    new_email = []

    for domain in COMPANIES:
        for email in USERS:
            login, old_domain = email.split("@")
            if old_domain != "slurm.io":
                print(f"Внимание! Почта {email} находится не на корпоративном домене")
                break
            new_email.append(login + "@" + domain)
        else:
            continue
        break
    else:
        print("Все данные были провалидированы")
        print(new_email)
