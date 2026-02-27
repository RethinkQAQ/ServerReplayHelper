import json
import os.path
from threading import RLock
from typing import List, Optional, Union

from mcdreforged import RTextMCDRTranslation, ServerInterface, RTextList, RText, RAction

help_dict = {
    "list": "[<pageNum>]",
    "start": "[<ID>]",
    "pause": "[<ID>]",
    "stop": "[<ID>]",
    "cut": "[<ID>]",
    "chunk start": "<radius> <name>",
    "chunk stop": "<name>",
    "chunk cut": "<name>"
}

class Recording:
    def __init__(self, record_type: str, name: str):
        self.type = record_type
        self.name = name


def tr(key: str, *args, **kwargs) -> RTextMCDRTranslation:
    return ServerInterface.si().rtr(f"server_replay_helper.{key}", args, **kwargs)


def help_message(command: str, key: str):
    return RTextList(RText(f"§7{command} {key} {help_dict[key]}").c(RAction.suggest_command, f"{command} {key}"), " ",
                     tr(f"help.{key}"))


def parse_single_recording(path: str) -> Optional[Recording]:
    try:
        normalized_path = os.path.normpath(path)
        split_path = normalized_path.split(os.sep)

        type_indicators = ["players", "chunks"]

        for i, part in enumerate(split_path):
            if part in type_indicators and i + 2 < len(split_path):
                recording_type = part
                subject_name = split_path[i + 1]

                return Recording(recording_type, subject_name)
        from server_replay_helper.entry import server_inst as server
        server.logger.error(f"Failed to parse recording path {path}")
        return Recording("unknown", "unknown")

    except Exception as e:
        from server_replay_helper.entry import server_inst as server
        server.logger.error(f"Failed to parse recording path {path}: {e}")
        return Recording("unknown", "unknown")


def parse_recording_list(recording_list: List[str]) -> List[Recording]:
    if not recording_list:
        return []
    return [parse_single_recording(path) for path in recording_list]

def get_chunk_coords(x: float, z: float) -> tuple[int, int]:
    return int(x // 16), int(z // 16)

def get_dim_key(dim: Union[int, str]) -> str:
    dim_convert = {0: 'minecraft:overworld', -1: 'minecraft:the_nether', 1: 'minecraft:the_end'}
    return dim_convert.get(dim, dim)


class RecordingManager:

    def __init__(self):
        self.__replay_list: List[Recording] = []
        self.__lock = RLock()

    def load_from_file(self, file_path: str):
        with self.__lock:
            folder = os.path.dirname(file_path)
            if os.path.isdir(folder):
                try:
                    with open(file_path, 'r', encoding="utf-8") as f:
                        data = json.load(f)
                        self.__replay_list = parse_recording_list(data)
                except Exception as e:
                    from server_replay_helper.entry import server_inst as server
                    server.logger.error(f'Failed to load replay list from {file_path}, reason: {e}')

    def get_top_recordings(self, top: int = 3) -> List[Recording]:
        with self.__lock:
            if not self.__replay_list:
                return []
            actual_top = min(top, len(self.__replay_list))
            return self.__replay_list[:actual_top]

def test_path_parsing():
    """测试路径解析"""

    # 测试路径
    test_paths = [
        "E:\\Server\\MCDR\\server\\recordings\\players\\Steve\\2026-02-27--13-53-40",
        "./server/recordings/players/Steve/2026-02-27--14-30-15",
        "/home/user/mc/recordings/chunks/world/2026-02-27--15-22-08"
    ]

    print("=== 单个路径解析测试 ===")
    for path in test_paths:
        print(f"\n测试路径: {path}")
        result = parse_single_recording(path)
        if result:
            print(f"  解析成功: 类型={result.type}, 名称={result.name}")
        else:
            print("  解析失败")

    print("\n=== 批量解析测试 ===")
    results = parse_recording_list(test_paths)
    print(f"成功解析 {len(results)} 个录制项:")
    for i, recording in enumerate(results, 1):
        print(f"  {i}. 类型: {recording.type}, 名称: {recording.name}")

if __name__ == "__main__":
    test_path_parsing()
