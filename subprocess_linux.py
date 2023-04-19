from subprocess import (
    run, PIPE
)

from datetime import datetime

def get_uniq_active_users():
    collector = []
    with open("/etc/passwd", 'r') as passwd:
        for user in passwd.read().split("\n"):
            # Условие, если требуются активные пользователи if user.split(":")[-1].find("sbin") == -1:
            collector.append(user.split(":")[0])
        collector.pop()
    return ", ".join(collector)


def get_proc_info():
    total = -2
    collector = {}
    max_cpu_user = 0.0
    max_mem_user = 0.0
    max_mem_user_name = ""
    total_cpu_usage = 0
    max_cpu_user_name = ""
    total_mem_usage = 0
    result = "Пользовательских процессов: \n "
    ps = run(["ps", "aux"], capture_output=True)
    for process in ps.stdout.decode().split("\n"):
        total += 1
        if process == "":
            continue
        name = process.split()[0]
        if name == "USER":
            continue
        total_cpu_usage += float(process.split()[2])
        if float(process.split()[2]) > float(max_cpu_user):
            max_cpu_user = process.split()[2]
            max_cpu_user_name = process.split()[10]
        total_mem_usage += float(process.split()[3])
        if float(process.split()[2]) > float(max_mem_user):
            max_mem_user = process.split()[2]
            max_mem_user_name = process.split()[10]
        if process.split()[0] not in collector:
            collector[name] = 1
        else:
            collector[name] += 1

    sorted_collector = sorted(collector.items(), key=lambda x: x[1], reverse=True)
    for assemble_keys, assemble_value in sorted_collector:
        result += f'{assemble_keys}: {assemble_value}, \n '

    return f'Процессов запущено: {total}', result, \
        f'Всего памяти используется:{round(total_mem_usage, 1)}%\n' \
        f'Всего CPU используется: {round(total_cpu_usage, 1)}%\n'\
        f'Больше всего памяти использует:{max_mem_user_name} = {max_mem_user}%\n' \
        f'Больше всего CPU использует:{max_cpu_user_name} = {max_cpu_user}%'


def main():
    output_string = f'Отчёт о состоянии системы:\n'\
                    f'Пользователи системы: {get_uniq_active_users()}\n'.join(get_proc_info())
    print(output_string)
    date_string = datetime.now().strftime("%d-%m-%Y-%I:%M")
    file_name = f'{date_string}-scan.txt'
    output_file = open(file_name, "w")
    output_file.write(output_string)


if __name__ == '__main__':
    main()
