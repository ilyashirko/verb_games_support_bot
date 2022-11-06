import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


def message_handler(longpoll):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


def run_vk_bot(vk_token):
    vk_session = vk_api.VkApi(token=vk_token)
    return VkLongPoll(vk_session)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    longpoll = run_vk_bot(env.str('VK_TOKEN'))
    message_handler(longpoll)