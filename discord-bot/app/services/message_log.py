import disnake
import io
import json

from datetime import datetime
from typing import List


def delete_messages_log(messages: List[disnake.Message], reason: str) -> disnake.File:
    _file = io.StringIO()
    _file.write("Reason: " + reason + '\n')

    for i, m in enumerate(messages):
        line = {
            str(i): {
                'author': m.author.name,
                'timestamp': str(m.created_at),
                'content': m.content
            }
        }

        _file.write("=" * 30 + '\n')
        _file.write(f'{json.dumps(line, indent=2)}\n')

    _file.seek(0)

    return disnake.File(_file, filename=f'Transcript_{datetime.now()}.txt')
