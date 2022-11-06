import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_processing import detect_intent_text


def message_handler(event, vk_api):
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


def run_vk_bot(vk_bot_token):
    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message_handler(event, vk_api)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    run_vk_bot(env.str('VK_BOT_TOKEN'))
