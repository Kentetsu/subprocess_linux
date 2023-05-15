from subprocess import (
    run, PIPE
)

from datetime import datetime


def get_proc_info():
    total = 0
    collector = {}
    user_collector_string = []
    max_cpu_user = 0.0
    max_mem_user = 0.0
    max_mem_user_name = ""
    total_cpu_usage = 0
    max_cpu_user_name = ""
    total_mem_usage = 0
    result = "Пользовательских процессов: \n "
    ps = run(["ps", "aux"], capture_output=True)
    for process in ps.stdout.decode().split("\n"):
        if process == "":
            continue
        name = process.split()[0]
        if name == "USER":
            continue
        total += 1
        total_cpu_usage += float(process.split()[2])
        if float(process.split()[2]) > float(max_cpu_user):
            max_cpu_user = process.split()[2]
            max_cpu_user_name = process.split()[10]
        if float(process.split()[3]) > float(max_mem_user):
            max_mem_user = float(process.split()[3])
            max_mem_user_name = process.split()[10]
        total_mem_usage += float(process.split()[3])
        if process.split()[0] not in collector:
            collector[name] = 1
            user_collector_string.append(process.split()[0])
        else:
            collector[name] += 1
        if len(max_mem_user_name) > 20:
            max_mem_user_name = max_mem_user_name[:20]
        if len(max_cpu_user_name) > 20:
            max_cpu_user_name = max_cpu_user_name[:20]

    sorted_collector = sorted(collector.items(), key=lambda x: x[1], reverse=True)
    for assemble_keys, assemble_value in sorted_collector:
        result += f'{assemble_keys}: {assemble_value}, \n '

    return f'Пользователи системы: {user_collector_string}\n'\
        f'Процессов запущено: {total}\n', result, \
        f'Всего памяти используется:{round(total_mem_usage, 1)}%\n' \
        f'Всего CPU используется: {round(total_cpu_usage, 1)}%\n'\
        f'Больше всего памяти использует:{max_mem_user_name} = {max_mem_user}%\n' \
        f'Больше всего CPU использует:{max_cpu_user_name} = {max_cpu_user}%'


def main():
    get_string = ''
    for el in get_proc_info():
        get_string += str(el)
    output_string = f'Отчёт о состоянии системы:\n'\
                    f'{get_string} \n'
    print(output_string)
    date_string = datetime.now().strftime("%d-%m-%Y-%I:%M")
    file_name = f'{date_string}-scan.txt'
    output_file = open(file_name, "w")
    output_file.write(output_string)
    output_file.close()


if __name__ == '__main__':
    main()
