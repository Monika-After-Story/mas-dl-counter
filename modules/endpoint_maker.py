
import config
import json
import os
import os.path

from modules.mas_custom import PackageCounter


EP_FILE = "dl.json"


def update_endpoint(counter: PackageCounter):
    """
    updates the endpoint
    :param counter:
    :return:
    """
    path = os.path.normcase(os.path.join(config.ENDPOINT_PATH, EP_FILE))

    data = {}
    data.update(counter.counts)
    data["Mod (Total)"] = counter.total_mod()
    data["Spritepacks (Total)"] = counter.total_spritepacks()
    data["Installer (Total)"] = counter.total_installer()

    os.umask(0)
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
    with open(fd, "w") as file:
        json.dump(data, file)