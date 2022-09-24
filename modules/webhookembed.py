
from typing import List, Any


class FieldData():

    def __init__(self, name: str, value: Any, inline: bool=True):
        self.name = name
        self.value = value
        self.inline = inline

    def as_payload(self) -> dict:
        """
        Converst to payload for embed
        """
        data = {
            "name": self.name,
            "value": self.value,
        }

        if self.inline:
            data["inline"] = True

        return data


class EmbedData():

    def __init__(self, color: int = 0xDEADBF, title: str = "", fields: List[FieldData] = None):
        if fields is None:
            fields = []

        self.color = color
        self.title = title
        self.fields = fields

    def as_payload(self) -> dict:
        """
        Converts to payload for embed
        """
        data = {
            "color": self.color,
        }

        if self.title:
            data["title"] = self.title

        if len(self.fields) > 0:
            data["fields"] = [
                field.as_payload()
                for field in self.fields
            ]

        return data





