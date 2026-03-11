import os

EXIT_CODES = {
    "0": "SUCCESS", "1": "GENERAL", "2": "MISUSE",
    "126": "NOTEXEC", "127": "NOTFOUND", "128": "ABNORMAL", "255": "OUTOFRANGE",
    # Signals 1-5
    "129": "SIGHUP", "130": "SIGINT", "131": "SIGQUIT", "132": "SIGILL", "133": "SIGTRAP",
    # Signals 6-10
    "134": "SIGABRT", "135": "SIGBUS", "136": "SIGFPE", "137": "SIGKILL", "138": "SIGUSR1",
    # Signals 11-15
    "139": "SIGSEGV", "140": "SIGUSR2", "141": "SIGPIPE", "142": "SIGALRM", "143": "SIGTERM",
    # Signals 17-21
    "145": "SIGCHLD", "146": "SIGCONT", "147": "SIGSTOP", "148": "SIGTSTP", "149": "SIGTTIN",
    # Signals 22-26
    "150": "SIGTTOU", "151": "SIGURG", "152": "SIGXCPU", "153": "SIGXFSZ", "154": "SIGVTALRM",
    # Signals 27-31
    "155": "SIGPROF", "156": "SIGWINCH", "157": "SIGPOLL", "158": "SIGPWR", "159": "SIGSYS",
}


def _get_status():
    return os.environ.get("EXIT_STATUS", "0")


def _get_exit():
    code = os.environ.get("EXIT_STATUS", "0")
    return EXIT_CODES.get(code, "UNKNOWN")


def _human_time():
    s_env = os.environ.get("SECONDS")
    s_start = os.environ.get("SECONDS_START")
    if not s_env or not s_start:
        return ""
    elapsed = int(float(s_env) - float(s_start))
    if elapsed <= 0:
        return ""
    days, rem = divmod(elapsed, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days:
        return f"{days}d{hours}h"
    if hours:
        return f"{hours}h{minutes}m"
    if minutes:
        return f"{minutes}m{secs}s"
    return f"{secs}s"


def _exec_timer():
    if os.environ.get("SECONDS") and os.environ.get("SECONDS_START"):
        elapsed = float(os.environ["SECONDS"]) - float(os.environ["SECONDS_START"])
        return f"[{elapsed:.2f}]"
    return ""


def register(tokens):
    tokens["status"] = lambda: _get_status()
    tokens["exit"] = lambda: _get_exit()
    tokens["time"] = lambda: _human_time()
    tokens["timer"] = lambda: _exec_timer()
