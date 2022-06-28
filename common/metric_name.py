

def metric_register(federated: bool = None) -> str:
    task_name = "new.register"
    if federated:
        task_name += ".federated"
    return task_name


def metric_login(federated: bool = None) -> str:
    task_name = "new.login"
    if federated:
        task_name += ".federated"
    return task_name


def metric_blocked() -> str:
    task_name = "new.blocked"
    return task_name


def metric_password_reset() -> str:
    task_name = "new.password.reset"
    return task_name

def metric_song() -> str:
    return "new.song"


def get_all_metrics():
    metrics = get_song_metrics() + get_quantity_metrics()
    return metrics

def get_quantity_metrics():
    metrics = [
        "new.login",
        "new.login.federated",
        "new.register",
        "new.register.federated",
        "songs",
        "playlists",
        "albums",
    ]
    return metrics

def get_song_metrics():
    metrics = [
        "song.genre",
        "subscription",
        "user",
        "listener",
        "artist",
    ]
    return metrics