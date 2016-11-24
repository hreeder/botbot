from . import slack, karma, translate_ru, buttmaster

hooks = [slack.message_hook,
         karma.message_hook,
         translate_ru.message_hook,
         buttmaster.message_hook]
