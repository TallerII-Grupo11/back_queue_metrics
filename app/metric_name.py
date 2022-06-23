

def metric_register(federated: bool = None) -> str:
    task_name = "user.login"
    if federated:
        task_name += ".federated"
    return task_name

def metric_register_result(federated: bool = None) -> str:
    task_name = "user.register"
    if federated:
        task_name += ".federated"
    task_name += ".result"
    return task_name


def metric_login(federated: bool = None) -> str:
    task_name = "user.login"
    if federated:
        task_name += ".federated"
    return task_name

def metric_login_result(federated: bool = None) -> str:
    task_name = "user.login"
    if federated:
        task_name += ".federated"
    task_name += ".result"
    return task_name


def metric_blocked() -> str:
    task_name = "user.blocked"
    return task_name


def metric_password_reset() -> str:
    task_name = "user.password.reset"
    return task_name

