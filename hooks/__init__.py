from . import slack, karma

hooks = [slack.message_hook,
         karma.message_hook]
