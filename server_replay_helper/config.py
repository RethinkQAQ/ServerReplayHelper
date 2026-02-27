from mcdreforged import Serializable

class Permission(Serializable):
    replay_self: int = 2
    replay_others: int = 3
    replay_chunk: int = 2
    replay_list: int = 1
    replay_delete: int= 4

class Replay(Serializable):
    allow_download: bool = True
    allow_view_btn: bool = True

class Config(Serializable):
    replay_folder: str = "./server/config/ServerReplay/recordings.json"
    prefixes: list[str] = ['replay', 'rp']
    permission: Permission = Permission()
    replay: Replay = Replay()

