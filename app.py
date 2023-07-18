from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
import time
from redis import Redis
import os
import logging
import sys
import json
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(asctime)s - %(name)s - %(lineno)d - '
                                                                   '%(levelname)s - ''Message: %(message)s - '
                                                                   'Method: %(funcName)s - '
                                                                   '  - %(pathname)s - Process: %(process)d'
                                                                   ' - Tread: %(thread)d')
logger = logging.getLogger(__name__)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
API_KEY = os.getenv('API_KEY')
openai.api_key = OPEN_AI_API_KEY

logger.debug(f'Start Flask')
app = Flask(__name__)
logger.debug(f'Redis start')
redis = Redis(host="redis", port=6379, db=0, decode_responses=True)
logger.debug(f'Redis end')


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    """
    Отправить запрос на OpenAI с обработкой  ошибок
    :param kwargs:
    :return:
    """
    return openai.ChatCompletion.create(**kwargs)


def rate_limited(user):
    current_minute = int(time.time() / 60)
    key = f'{user}:{current_minute}'
    current_count = redis.get(key)
    logger.debug(f'Current count: {current_count}')
    if current_count is not None and int(current_count) > 10:  # Предполагаемый лимит - 10 запросов в минуту
        logger.debug(f'Rate limit exceeded for {user}')
        return True
    logger.debug(f'Rate limit not exceeded for {user}')
    redis.incr(key, 1)
    logger.debug(f'Current count: {current_count}')
    redis.expire(key, 59)  # Устанавливаем время жизни ключа в одну минуту
    logger.debug(f'Current count: {current_count}')
    return False


@app.route('/api/chat/completions', methods=['POST'])
def proxy():
    # Извлекаем API-ключ из заголовка запроса
    api_key = request.headers.get('Authorization')
    if not api_key or api_key != API_KEY:
        logger.debug(f'Invalid API key: {api_key}')
        return jsonify({'error': 'Invalid API key'}), 401

    if rate_limited(api_key):
        logger.debug(f'Rate limit exceeded for {api_key}')
        return jsonify({'error': 'Rate limit exceeded'}), 429
    logger.debug(f'Rate limit not exceeded for {api_key}')
    # Отправляем запрос в OpenAI

    response = completion_with_backoff(**request.get_json())
    logger.debug(f'Response: {response}')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
