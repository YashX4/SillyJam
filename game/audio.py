"""
Background music: load and stream the looping soundtrack.

raylib plays .ogg as a *streamed* Music (decoded on the fly), so the track has
to be fed each frame with rl.update_music_stream(). Looping is handled by
raylib itself once Music.looping is set.

Requires rl.init_audio_device() to have been called first (needs an audio
context, just like textures need a GL context).
"""

import pyray as rl

_MUSIC_PATH = "assets/sound/music/Empty_Streets.ogg"
_ROBOT_TALK_PATH = "assets/sound/effects/robot_talk_Sequence_03.ogg"
_ROBOT_DIALOG_OPENS_PATH = "assets/sound/effects/robot_dialog_opens_Data_Point_04.ogg"


def load_music() -> rl.Music:
    """Load the background track and start it looping."""
    music = rl.load_music_stream(_MUSIC_PATH)
    music.looping = True
    rl.play_music_stream(music)
    return music


def update_music(music: rl.Music) -> None:
    """Refill the stream's buffer; call once per frame."""
    rl.update_music_stream(music)


def unload_music(music: rl.Music) -> None:
    rl.stop_music_stream(music)
    rl.unload_music_stream(music)


def load_robot_talk() -> rl.Sound:
    """Load the short blip played when the dialog advances a line.

    Unlike the music this is a fully-decoded Sound (cheap, fire-and-forget),
    so it can be replayed on demand without streaming.
    """
    return rl.load_sound(_ROBOT_TALK_PATH)


def load_robot_dialog_opens() -> rl.Sound:
    """Load the chime played when the dialog box opens and closes."""
    return rl.load_sound(_ROBOT_DIALOG_OPENS_PATH)


def unload_sound(sound: rl.Sound) -> None:
    rl.unload_sound(sound)
