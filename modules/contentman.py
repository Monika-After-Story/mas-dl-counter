# manages content for discord json

from webhookembed import EmbedData

from typing import Optional, List

CONTENT_MESSAGE = "content"
CONTENT_USERNAME = "username"
CONTENT_AVATAR_URL = "avatar_url"
CONTENT_EMBED = "embeds"


def get_avatar_url(content: dict) -> Optional[str]:
    """
    Gets avatar url from content
    :param content: content to get url from
    :return: avatar url, or none if not found
    """
    return content.get(CONTENT_AVATAR_URL, None)


def set_avatar_url(content: dict, avatar_url: str) -> dict:
    """
    Adds an avatar url to the content
    :param content: content to add avatar url to
    :param avatar_url: avatar url to add
    :returns: content
    """
    content[CONTENT_AVATAR_URL] = avatar_url
    return content


def get_message(content: dict) -> Optional[str]:
    """
    Gets message from content
    :param content: content to get message from
    :return: message, or None if not found
    """
    return content.get(CONTENT_MESSAGE, None)


def set_message(content: dict, msg: str) -> dict:
    """
    Adds a message to the content
    :param content: content to add message to
    :param msg: message to add
    :returns: content
    """
    content[CONTENT_MESSAGE] = msg
    return content


def get_username(content: dict) -> Optional[str]:
    """
    Gets username from contnet
    :param content:  content to get message from
    :return: message, or None if not found
    """
    return content.get(CONTENT_USERNAME, None)


def set_username(content: dict, username: str) -> dict:
    """
    Adds username to the content
    :param content: content to add username to
    :param username: username to add
    :returns: content
    """
    content[CONTENT_USERNAME] = username
    return content


def set_embeds(content: dict, embeds: List[EmbedData]) -> dict:
    """
    Adds embeds to the content
    :param content: cntent to add embeds to
    :param embeds: embds to set
    :returns: content
    """
    content[CONTENT_EMBED] = [
        embed.as_payload()
        for embed in embeds
    ]
    return content
