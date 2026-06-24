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
