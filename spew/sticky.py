# -*- coding: utf-8 -*-

from afew.filters.BaseFilter import Filter


class StickyFilter(Filter):
    message = 'Looking for messages in threads that are not tagged consistant'
    query = 'tag:inbox AND NOT tag:lists'

    def handle_message(self, message):
        tags = set()
        thread_id = message.get_thread_id()

        for m in self.database.get_messages('thread:"%s"' % thread_id):
            tags.update(m.get_tags())

        self.add_tags(message, *tags)
