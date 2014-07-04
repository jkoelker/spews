# -*- coding: utf-8 -*-

from email import utils

from afew.filters.BaseFilter import Filter
from afew import Settings

Settings.value_is_a_list.append('distribution_lists')


class DistributionFilter(Filter):
    message = 'Looking for messages from distribution lists'
    query = 'tag:inbox AND NOT tag:lists'
    distribution_lists = []
    tags = ['+lists', '+lists/{list_id}']

    def __init__(self, *args, **kwargs):
        super(DistributionFilter, self).__init__(*args, **kwargs)

        self._dl_set = set([dl.lower()
                            for dl in self.distribution_lists])

    def handle_message(self, message):
        if not self.distribution_lists:
            return

        elif self._tag_blacklist.intersection(message.get_tags()):
            return

        to = set()

        # TODO(jkoelekr) Optimize this
        for header in ('to', 'cc', 'bcc'):
            addrs = message.get_header(header).split(',')
            for addr in addrs:
                value = utils.parseaddr(addr)[-1]
                if value:
                    to.add(value.lower())

        lists = [l.split('@')[0] for l in to & self._dl_set]
        for list_id in lists:
            sub = lambda tag: tag.format(list_id=list_id)
            self.remove_tags(message, *map(sub, self._tags_to_remove))
            self.add_tags(message, *map(sub, self._tags_to_add))
