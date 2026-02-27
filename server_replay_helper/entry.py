from mcdreforged import PluginServerInterface, SimpleCommandBuilder, CommandSource, RTextList, RText, RAction, RColor, \
    QuotableText, new_thread, PlayerCommandSource, Integer

from server_replay_helper.config import Config
from server_replay_helper.utils import tr, RecordingManager, get_chunk_coords, get_dim_key

server_inst: PluginServerInterface
config = Config()
replay_manager = RecordingManager()


def on_load(server: PluginServerInterface, pre_module):
    global server_inst, config, replay_manager
    server_inst = server
    config = server.load_config_simple(
        'config.json',
        target_class=Config
    )
    load_recording_list()
    server.register_help_message("!!replay", tr("help_msg"))
    register_command(server)

@new_thread
def load_recording_list():
    replay_manager.load_from_file(config.replay_folder)

def print_replay_message(source: CommandSource):
    load_recording_list()
    source.reply(tr("help.replay"))
    print_replay_list(source)

def print_replay_list(source: CommandSource, top: int = 3):
    recordings = replay_manager.get_top_recordings(top)
    source.reply(tr("list"))
    if not recordings:
        source.reply(tr('list.no_recordings'))
        return
    for recording in recordings:
        text_item = RTextList(
            RText(tr("list.mode.replay")),
            RText(tr(f"list.type.{recording.type}")),
            RText(recording.name),
            )
        if recording.type == "players":
            text_item.append(RText("[⏹]", color=RColor.dark_red)
                             .h(tr("action.stop"))
                             .c(RAction.run_command, f"!!replay stop {recording.name}"))
        elif recording.type == "chunks":
            text_item.append(RText("[⏹]", color=RColor.dark_red)
                             .h(tr("action.stop"))
                             .c(RAction.run_command, f"!!replay chunk stop {recording.name}"))
        source.reply(text_item)
    source.reply("...")

def start_player(src: CommandSource, player: str):
    if not src.has_permission(config.permission.replay_self):
        src.reply(tr("permission"))
        return
    if isinstance(src, PlayerCommandSource) and src.player != player:
        src.reply(tr("command.not_self"))
        return
    server_inst.execute(f"replay start players {player}")
    src.reply(tr("command.execute"))

def stop_player(src: CommandSource, player: str):
    if not src.has_permission(config.permission.replay_self):
        src.reply(tr("permission"))
        return
    if isinstance(src, PlayerCommandSource) and src.player != player:
        src.reply(tr("command.not_self"))
        return
    server_inst.execute(f"replay stop players {player}")
    src.reply(tr("command.execute"))

@new_thread
def start_chunk(src: CommandSource, name: str, radius: int):
    if not src.has_permission(config.permission.replay_chunk):
        src.reply(tr("permission"))
        return
    if not isinstance(src, PlayerCommandSource):
        src.reply(tr("command.not_player"))
        return
    api = server_inst.get_plugin_instance("minecraft_data_api")
    pos = api.get_player_coordinate(src.player)
    dim = api.get_player_dimension(src.player)
    cX, cZ = get_chunk_coords(pos.x, pos.z)
    dim_key = get_dim_key(dim)
    server_inst.execute(f"replay start chunks around {cX} {cZ} radius {radius} in {dim_key} named {name}")

def stop_chunk(src: CommandSource, name: str):
    if not src.has_permission(config.permission.replay_chunk):
        src.reply(tr("permission"))
        return
    server_inst.execute(f"replay stop chunks named {name}")

def register_command(server: PluginServerInterface):
    builder = SimpleCommandBuilder()

    for prefix in config.prefixes:

        builder.command(f"!!{prefix}", lambda src: print_replay_message(src))

        builder.command(f"!!{prefix} help", lambda src: print_replay_message(src))

        # !!replay start|stop [<player>]   start or stop recording self or other player
        builder.arg("player", QuotableText)
        builder.command(f"!!{prefix} start", lambda src: start_player(src, src.player))
        builder.command(f"!!{prefix} stop", lambda src: stop_player(src, src.player))
        builder.command(f"!!{prefix} start <player>", lambda src, ctx: start_player(src, ctx["player"]))
        builder.command(f"!!{prefix} stop <player>", lambda src, ctx: stop_player(src, ctx["player"]))

        # !!replay chunk start|stop <name> <radius>   start or stop recording chunk
        builder.arg("name", QuotableText)
        builder.arg("radius", lambda radius: Integer(radius).in_range(2, 25))
        builder.command(f"!!{prefix} chunk start <name> <radius>", lambda src, ctx: start_chunk(src, ctx["name"], ctx["radius"]))
        builder.command(f"!!{prefix} chunk stop <name>", lambda src, ctx: stop_chunk(src, ctx["name"]))

        builder.register(server)

