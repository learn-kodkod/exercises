
data = [
'2025-10-08T06:41:00Z;auth;INFO;user login ok',
'2025-10-08T06:42:00Z;db;ERROR;connection timeout',
'2025-10-08T06:43:00Z;api;WARN;slow response detected',
'2025-10-08T06:44:00Z;auth;INFO;new user registered',
'2025-10-08T06:45:00Z;web;DEBUG;session cookie created',
'2025-10-08T06:46:00Z;auth;INFO;user logout ok',
'2025-10-08T06:47:00Z;db;INFO;query executed successfully',
'2025-10-08T06:48:00Z;api;ERROR;invalid json format',
'2025-10-08T06:49:00Z;cache;INFO;cache cleared',
'2025-10-08T06:50:00Z;auth;WARN;multiple failed logins',
'2025-10-08T06:51:00Z;db;INFO;replica sync complete',
'2025-10-08T06:52:00Z;api;INFO;endpoint /status called',
'2025-10-08T06:53:00Z;web;INFO;homepage rendered',
'2025-10-08T06:54:00Z;auth;ERROR;invalid token',
'2025-10-08T06:55:00Z;cache;DEBUG;cache hit for user id=23',
'2025-10-08T06:56:00Z;db;WARN;slow query detected',
'2025-10-08T06:57:00Z;api;INFO;GET /users successful',
'2025-10-08T06:58:00Z;auth;INFO;password reset requested',
'2025-10-08T06:59:00Z;web;ERROR;missing static resource',
'2025-10-08T07:00:00Z;cache;INFO;cache warmup completed',
'2025-10-08T07:01:00Z;auth;INFO;user verified via email',
'2025-10-08T07:02:00Z;db;INFO;backup completed',
'2025-10-08T07:03:00Z;api;WARN;rate limit reached',
'2025-10-08T07:04:00Z;auth;DEBUG;JWT token created',
'2025-10-08T07:05:00Z;web;INFO;page /profile loaded',
'2025-10-08T07:06:00Z;cache;INFO;cache updated for /api/users',
'2025-10-08T07:07:00Z;db;ERROR;duplicate key error',
'2025-10-08T07:08:00Z;api;INFO;POST /login success',
'2025-10-08T07:09:00Z;auth;INFO;2FA verified',
'2025-10-08T07:10:00Z;web;INFO;assets preloaded',
'2025-10-08T07:11:00Z;cache;WARN;cache miss for session id=45',
'2025-10-08T07:12:00Z;db;INFO;transaction committed',
'2025-10-08T07:13:00Z;api;ERROR;missing authorization header',
'2025-10-08T07:14:00Z;auth;INFO;role updated to admin',
'2025-10-08T07:15:00Z;web;INFO;logout page rendered',
'2025-10-08T07:16:00Z;cache;INFO;cache entry expired',
'2025-10-08T07:17:00Z;db;DEBUG;query plan optimized',
'2025-10-08T07:18:00Z;api;INFO;PUT /settings success',
'2025-10-08T07:19:00Z;auth;WARN;user session expired',
'2025-10-08T07:20:00Z;web;INFO;error 404 rendered',
'2025-10-08T07:21:00Z;cache;DEBUG;cache cleanup started',
'2025-10-08T07:22:00Z;db;INFO;index rebuilt',
'2025-10-08T07:23:00Z;api;INFO;DELETE /session ok',
'2025-10-08T07:24:00Z;auth;INFO;user deleted',
'2025-10-08T07:25:00Z;web;WARN;redirect loop detected',
'2025-10-08T07:26:00Z;cache;INFO;cache compression done',
'2025-10-08T07:27:00Z;db;INFO;schema migration complete',
'2025-10-08T07:28:00Z;api;ERROR;internal server error',
'2025-10-08T07:29:00Z;auth;INFO;user login ok',
'2025-10-08T07:30:00Z;web;INFO;dashboard loaded'
]



def parse_line(line: str) -> dict | None:
    line_parts = {}
    line_split = line.split(';')
    # print(line_split)
    if line == "" or len(line_split) < 4:
        return None
    parts_names = ["timestamp", "service", "level", "message"]
    for index, part in enumerate(line_split):
        line_parts[parts_names[index]] = part

    return line_parts


def parse_logs(lines: list[str]) -> list[dict]:
    all_dict = []
    for log in lines:
        res = parse_line(log)
        if res:
            all_dict.append(res)
    return all_dict


def count_by_level(log_dicts: list[dict]) -> dict:
    # log_level = ["DEBUG", "INFO", "ALERT", "FATAL", "WARN"]
    log_level_counter = {}
    for log_dict in log_dicts:
        if log_dict["level"] not in log_level_counter:
            log_level_counter[log_dict["level"]] = 1
        else:
            log_level_counter[log_dict["level"]] += 1
    return log_level_counter

def services_by_errors(log_dicts):
    service_error_count = {}
    for log_dict in log_dicts:
        if log_dict["level"] == "ERROR":
            if log_dict["service"] not in service_error_count.keys():
                service_error_count[log_dict["service"]] = 1
            else:
                service_error_count[log_dict["service"]] += 1
    return service_error_count


def top_service_by_errors(log_dicts):
    services_error = services_by_errors(log_dicts)
    service_max = ""
    max_value = max(services_error.values())
    for service in services_error.keys():
        if int(services_error[service]) == max_value:
            service_max = service
    return (service_max , max_value)


def all_service_count(logs_dicts):
    service_count = {}
    for log_dict in logs_dicts:
        if log_dict["service"] not in service_count.keys():
            service_count[log_dict["service"]] = 1
        else:
            service_count[log_dict["service"]] += 1
    return service_count

def worst_service_ratio(logs_dicts: list[dict]) -> tuple[str, float] | None:
    service_by_errors = services_by_errors(logs_dicts)
    service_count = all_service_count(logs_dicts)
    worst_service_ratio = 0
    worst_service_name = ""
    for service in service_count.keys():
        if service in service_by_errors.keys():
            service_error_ratio =  service_by_errors[service] / service_count[service]
            if service_error_ratio > worst_service_ratio:
                worst_service_name = service
                worst_service_ratio = service_error_ratio

    return (worst_service_name,round(worst_service_ratio * 100 ,1))


def sort_by_severity(logs_dicts: list[dict]) -> list[dict]:

    error_list = []
    warn_list = []
    info_lst = []
    for log_dict in logs_dicts:
        if log_dict["level"] == "ERROR":
            error_list.append(log_dict)
        elif log_dict["level"] == "WARN":
            warn_list.append(log_dict)
        elif log_dict["level"] == "INFO":
            info_lst.append(log_dict)
    return error_list + warn_list + info_lst

def find_by_message(logs_dicts: list[dict], keyword: str) -> list[dict]:
    new_log = []
    for log_dict in logs_dicts:
        if keyword.lower() in log_dict["message"].lower():
            new_log.append(log_dict)
    return new_log

def generate_report(logs_dicts)-> str:
    report = f"Total entries: {len(logs_dicts)} \n"
    total_errors = sum(services_by_errors(logs_dicts).values())
    report += f"Total errors {total_errors} \n"
    service, ratio = worst_service_ratio(logs_dicts)
    report+= f"Most problematic service (by ratio): {service} ({ratio})%\n)"
    max_service, max_value = top_service_by_errors(logs_dicts)
    report += f"Most errors (by count):{max_service} ({max_value} errors)"
    return report


logs_dict = parse_logs(data)
print(generate_report(logs_dict))
# print(f"count by level {count_by_level(logs_dict)}")
# print(f"count service errors {top_service_by_errors(logs_dict)}")
# service, ratio =   worst_service_ratio(logs_dict)
# print(f"all services {all_service_count(logs_dict)}")
# print(f"worst service {service} and ratio {ratio} %")
# order_log = sort_by_severity(logs_dict)
# for log in order_log:
#     print(f"{log}")
# print("-----------------------------")
# log_with_keyword = find_by_message(logs_dict, "session")
# for log in log_with_keyword:
#     print(f"{log}")