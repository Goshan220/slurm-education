if __name__ == '__main__':
    branch_name = str(input()).capitalize()
    is_tests_passed = int(input())
    coverage_change = float(input())
    numbers_of_approve = int(input())

    branch_name_baseline = ("Development", "Staging")
    if branch_name not in branch_name_baseline:
        print(f"В ветке {branch_name} непроверенный код, пропускаем")
    elif \
            (is_tests_passed and coverage_change > 5) or \
            (is_tests_passed and 0 < coverage_change <= 5 and numbers_of_approve > 3):
        print(f"Внимание! Код из {branch_name} отправлен в релиз!")
    else:
        print(f"Код из {branch_name} с результатами тесты: {is_tests_passed}, coverage: "
              f"{coverage_change}, approve: {numbers_of_approve} в релиз не попадает.")
