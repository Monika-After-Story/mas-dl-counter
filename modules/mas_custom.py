import config
import contentman
import requests
import re

from collections import defaultdict

from modules.webhookembed import EmbedData, FieldData
from modules import ghstats

from typing import Tuple, List

MAS_USER = "Monika-After-Story"
MAS_REPO = "MonikaModDev"

PKG_NAME = "Monika_After_Story"
PKG_NAME_DLX = "Dlx"

VER_REGEX = re.compile(r"Monika_After_Story-(\d+\.\d+\.\d+)-")

SPACK = "spritepacks.zip"
SPACK_COMB = "spritepacks-combined.zip"

ROSES_OBJ = "roses.obj"
PARTY_SUP = "partysupplies.zip"

INS_NAME = "mas-installer"
INS_NAME_WIN = "exe"
INS_NAME_NIX = "linux"
INS_NAME_MAC = "mac"

ICON_URL = "https://cdn.discordapp.com/emojis/536169079640162315.webp?size=160&quality=lossless"


_MOD_REG = "Mod (Regular)"
_MOD_DLX = "Mod (Deluxe)"
_SPACK = "Spritepacks"
_SPACK_C = "Spritepacks Combined"
_ROSES = "Roses"
_PARTY_SUP = "Party Supplies"
_INS_WIN = "Installer (Windows)"
_INS_NIX = "Installer (Linux)"
_INS_MAC = "Installer (Mac)"


VER_MAJOR = 10000000
VER_MINOR = 100000

def split_num(value: int) -> str:
    """
    Makes number look nice
    :param value:
    :return:
    """
    return "{:,}".format(value)


def ver_value(ver: str) -> int:
    """
    Converts a version string into a version value
    :param ver: version to convert
    :return: value
    """
    ver_parts = ver.split(".")
    return (
        (int(ver_parts[0]) * VER_MAJOR)
        + (int(ver_parts[1]) * VER_MINOR)
        + int(ver_parts[2])
    )


def ver_str(value: int) -> str:
    """
    Converts a version value into a version string
    :param value: value to convert
    :return: version str
    """
    major = value // VER_MAJOR
    value %= VER_MAJOR

    minor = value // VER_MINOR
    value %= VER_MINOR

    build = value

    return "{0:01}.{1:01}.{2:01}".format(major, minor, build)


class PackageCounter():

    counts: dict
    ver_counts: dict

    def __init__(self):
        self.counts = {
            _MOD_REG: 0,
            _MOD_DLX: 0,
            _SPACK: 0,
            _SPACK_C: 0,
            _ROSES: 0,
            _PARTY_SUP: 0,
            _INS_WIN: 0,
            _INS_NIX: 0,
            _INS_MAC: 0,
        }
        self.ver_counts = defaultdict(int)

    #region props
    @property
    def mod_regular(self) -> int:
        return self.counts[_MOD_REG]

    @mod_regular.setter
    def mod_regular(self, value: int):
        self.counts[_MOD_REG] = value

    @property
    def mod_deluxe(self) -> int:
        return self.counts[_MOD_DLX]

    @mod_deluxe.setter
    def mod_deluxe(self, value: int):
        self.counts[_MOD_DLX] = value

    @property
    def spritepacks(self) -> int:
        return self.counts[_SPACK]

    @spritepacks.setter
    def spritepacks(self, value: int):
        self.counts[_SPACK] = value

    @property
    def spritepacks_combined(self) -> int:
        return self.counts[_SPACK_C]

    @spritepacks_combined.setter
    def spritepacks_combined(self, value: int):
        self.counts[_SPACK_C] = value

    @property
    def roses(self) -> int:
        return self.counts[_ROSES]

    @roses.setter
    def roses(self, value: int):
        self.counts[_ROSES] = value

    @property
    def party_supplies(self) -> int:
        return self.counts[_PARTY_SUP]

    @party_supplies.setter
    def party_supplies(self, value: int):
        self.counts[_PARTY_SUP] = value

    @property
    def installer_windows(self) -> int:
        return self.counts[_INS_WIN]

    @installer_windows.setter
    def installer_windows(self, value: int):
        self.counts[_INS_WIN] = value

    @property
    def installer_linux(self) -> int:
        return self.counts[_INS_NIX]

    @installer_linux.setter
    def installer_linux(self, value: int):
        self.counts[_INS_NIX] = value

    @property
    def installer_mac(self) -> int:
        return self.counts[_INS_MAC]

    @installer_mac.setter
    def installer_mac(self, value: int):
        self.counts[_INS_MAC] = value

    #endregion

    def count_package(self, package: dict):
        """
        Counts downloads from a package
        :param package: package to count
        """
        name = PackageCounter.package_name(package)
        count = PackageCounter.package_downloads(package)

        if name == ROSES_OBJ:
            self.roses += count

        elif name == PARTY_SUP:
            self.party_supplies += count

        elif name == SPACK:
            self.spritepacks += count

        elif name == SPACK_COMB:
            self.spritepacks_combined += count

        elif INS_NAME in name:

            if name.endswith(INS_NAME_WIN):
                self.installer_windows += count

            elif name.endswith(INS_NAME_NIX):
                self.installer_linux += count

            elif name.endswith(INS_NAME_MAC):
                self.installer_mac += count

        elif PKG_NAME in name:

            if PKG_NAME_DLX in name:
                self.mod_deluxe += count

            else:
                self.mod_regular += count

            # add version counts
            self.ver_counts[ver_value(VER_REGEX.match(name).group(1))] += count

    def latest(self) -> List[Tuple[str, int]]:
        """
        get latest versions
        :return: tuple: ver name, count
        """
        sorted_vers = sorted(list(self.ver_counts.keys()), reverse=True)

        return [
            (ver_str(sorted_vers[i]), self.ver_counts[sorted_vers[i]])
            for i in range(config.LATEST_VER)
        ]

    def total_installer(self) -> int:
        """
        total installer downloads
        :return:  total
        """
        return self.installer_windows + self.installer_linux + self.installer_mac

    def total_mod(self) -> int:
        """
        total mod downloads
        :return: total
        """
        return self.mod_deluxe + self.mod_regular

    def total_spritepacks(self) -> int:
        """
        Total spritepacks
        :return: total
        """
        return self.spritepacks + self.spritepacks_combined

    def _total_all(self) -> int:
        """
        if you want all downloads for some reason
        :return: total
        """
        total = 0
        for value in self.counts.values():
            total += value
        return total

    @staticmethod
    def package_name(package: dict) -> str:
        """
        Gets name of a package
        :param package: package to get name of
        :return: name of package
        """
        name = package["label"]
        if not name:
            name = package["name"]

        return name

    @staticmethod
    def package_downloads(package: dict) -> int:
        """
        Gets downloads from a package
        :param package: package to get downloads from
        :return: download count of package
        """
        return package["download_count"]


class MASCustom():

    gh_token: str
    webhook_url: str

    def __init__(self):
        self.gh_token = config.GH_TOKEN
        self.webhook_url = config.WEBHOOK_URL

    def run_mas_download_counter(self):
        """
        counts downloads accordingly.
        :param log:
        :return:
        """

        # download the stats
        stats = ghstats.download_stats(user=MAS_USER, repo=MAS_REPO, token=self.gh_token, quiet=True)

        if isinstance(stats, dict):
            stats = [stats]

        # go through stats and count valid downloads
        counter = PackageCounter()
        for release in stats:
            if "assets" in release:
                for package in release["assets"]:
                    counter.count_package(package)

        # generate embed field data)
        fields = [
            FieldData(_MOD_REG, split_num(counter.mod_regular)),
            FieldData(_MOD_DLX, split_num(counter.mod_deluxe)),
            FieldData("Total Installer", split_num(counter.total_installer())),
            FieldData(_INS_WIN, split_num(counter.installer_windows)),
            FieldData(_INS_NIX, split_num(counter.installer_linux)),
            FieldData(_INS_MAC, split_num(counter.installer_mac)),
            FieldData(_SPACK, split_num(counter.spritepacks)),
            FieldData(_SPACK_C, split_num(counter.spritepacks_combined)),
            FieldData("Total Spritepacks", split_num(counter.total_spritepacks())),
            FieldData(_PARTY_SUP, split_num(counter.party_supplies)),
            FieldData(_ROSES, split_num(counter.roses)),
        ]

        # latest versions
        latest_ver_stats = counter.latest()
        for ver_name, ver_count in latest_ver_stats:
            fields.append(FieldData("v" + ver_name, split_num(ver_count)))

        # post count to discord
        content = {}
        contentman.set_username(content, "counter")
        contentman.set_avatar_url(content, ICON_URL)
        contentman.set_embeds(
            content,
            [
                EmbedData(
                    title="Total Mod: {:,}".format(counter.total_mod()),
                    fields=fields
                )
            ]
        )
        requests.post(config.WEBHOOK_URL, json=content)
