from . import slack, karma, translate_ru

hooks = [slack.message_hook,
         karma.message_hook,
         translate_ru.message_hook]
