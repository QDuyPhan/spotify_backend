# from models import album
# from models import message
# # from .song import Song
# from models import song
# from models import user

from .album import Album
from .song import Song
from .user import User
from .message import Message
__all__ = ['Album', 'Message', 'Song', 'User']