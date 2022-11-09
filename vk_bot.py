import logging
import random

import vk_api as vk
from environs import Env
from telegram import Bot
from vk_api.longpoll import Event, VkEventType, VkLongPoll

from dialogflow_processing import detect_intent_text
from log_handlers import TelegramLogsHandler

logger = logging.getLogger('log.log')


def message_handler(event: Event, vk_api: vk.vk_api.VkApiMethod) -> None:
    dialogflow_response = detect_intent_text(
        env.str('GOOGLE_PROJECT_ID'),
        event.user_id,
        event.text,
    )
    if dialogflow_response.intent.is_fallback:
        return
    vk_api.messages.send(
        user_id=event.user_id,
        message=dialogflow_response.fulfillment_text,
        random_id=random.randint(1,1000)
    )


def run_vk_bot(vk_bot_token: str) -> None:
    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.setLevel(logging.INFO)
    logger.addHandler(
        TelegramLogsHandler(
            Bot(env.str('TELEGRAM_BOT_TOKEN')), env.int('ADMIN_TELEGRAM_ID')
        )
    )
    logger.info('[VK BOT ERROR] Support bot started')

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message_handler(event, vk_api)
    except Exception as error:
        logger.error(msg='[VK]\n', exc_info=error)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    run_vk_bot(env.str('VK_BOT_TOKEN'))
