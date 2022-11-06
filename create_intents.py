import json
import sys
from argparse import ArgumentParser

from environs import Env
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from tqdm import tqdm


def create_parser():
    parser = ArgumentParser(
        description="Create intent for dialogflow"
    )
    parser.add_argument(
        '--path_to_json',
        '-p',
        type=str,
        help='json file with training phrases',
        required=True
    )
    return parser


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    env = Env()
    env.read_env()

    try:
        with open(args.path_to_json, 'r') as new_intents_file:
            new_intents_data = json.load(new_intents_file)
    
    except FileNotFoundError:
        sys.stdout.write('File not found.\n')
        sys.exit()

    except json.decoder.JSONDecodeError:
        sys.stdout.write('Broken JSON.\n')
        sys.exit()

    for display_name, new_intent_data in tqdm(new_intents_data.items(),
                                              desc='creating intents'):
        try:
            create_intent(
                env.str('GOOGLE_PROJECT_ID'),
                display_name,
                new_intent_data['questions'],
                [new_intent_data['answer']]
            )
        except InvalidArgument as error:
            sys.stdout.write(f'GOOGLE_API_ERROR: {error}\n')
    sys.stdout.write('All intents loaded.\n')