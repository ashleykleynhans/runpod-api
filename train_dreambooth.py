#!/usr/bin/env python3
import runpod
import json

CONCEPT_NAME = 'OHWXman'


if __name__ == '__main__':
    serverless = runpod.Serverless()

    response = serverless.train_dreambooth({
        'input': {
            'train': {
                'concept_name': CONCEPT_NAME,
                'ckpt_link': 'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt',
                'data_url': 'https://my-dreambooth-datasets.s3.amazonaws.com/dataset.zip',
                'unet_epochs': 100,
                'text_steps': 150,
                'text_batch_size': 1,
                'unet_batch_size': 1,
                'text_resolution': 512,
                'unet_resolution': 512,
                'text_learning_rate': 0.000001,
                'unet_learning_rate': 0.000002,
                'text_lr_scheduler': 'constant',
                'unet_lr_scheduler': 'constant',
                'text_8_bit_adam': False,
                'unet_8_bit_adam': False,
                'text_seed': 420420,
                'unet_seed': 420420,
                'offset_noise': False
            },
            'inference': [
                {
                    'prompt': f'{CONCEPT_NAME}',
                    'sampler_name': 'Euler a',
                    'batch_size': 1,
                    'steps': 40,
                    'cfg_scale': 7
                },
                {
                    'prompt': f'{CONCEPT_NAME} by Tomer Hanuka',
                    'sampler_name': 'Euler a',
                    'batch_size': 4,
                    'steps': 40,
                    'cfg_scale': 7
                },
            ],
        },
        'webhook': 'https://3fa5-45-222-2-229.ngrok.io/',
        's3Config': {
            'bucketName': 'my-runpod-dreambooth-output',
            'accessId': 'ACCESS_KEY',
            'accessSecret': 'SECRET_KEY',
            'endpointUrl': 'https://mydreambooth-output.s3.us-east-1.amazonaws.com'
        }
    })

    resp_json = response.json()

    if response.status_code == 401:
        print('401: Unauthorized')
    else:

        # if 'errors' in response:
        #     print('ERROR:')
        #     for error in response['errors']:
        #         print(error['message'])
        # else:
        #     pass

        print(json.dumps(resp_json, indent=4, default=str))
