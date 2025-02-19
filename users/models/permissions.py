from enum import Enum


class ReaderPermissions(Enum):
    NEWS_ADD = "add_news"
    NEWS_VIEW = "view_news"
    NEWS_CHANGE = "change_news"
    NEWS_DELETE = "delete_news"
