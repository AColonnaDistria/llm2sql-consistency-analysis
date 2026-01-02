import openai
import ollama

from dotenv import load_dotenv
import os

from diskcache import Cache
import hashlib

from abc import ABC, abstractmethod

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class IPromptManager(ABC):
    @abstractmethod
    def get_response(self, system_prompt: str = None, user_prompt: str = None, model: str = None, temperature: float = 1.0):
        pass

class CacheManager:
    def __init__(self, cache_name: str):
        self.cache = Cache(f'cache/{cache_name}')
    
    def get_cache_key(self, *keys):
        return tuple(keys)

    def contains_key(self, *keys):
        return self.get_cache_key(*keys) in self.cache

    def set_value(self, *keys, value = None):
        cache_key = self.get_cache_key(*keys)

        self.cache[cache_key] = value

    def get_value(self, *keys):
        cache_key = self.get_cache_key(*keys)

        if cache_key in self.cache:
            print("[CACHE HIT]")
            return self.cache[cache_key]
        
        return None

class OpenaiPromptManager(IPromptManager):
    def __init__(self, api_key: str = OPENAI_API_KEY, seed: int = 0, keeps_cache: bool = True, max_tokens: int = 600, timeout: float = 30.0):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.keeps_cache = keeps_cache

        self._max_tokens = max_tokens
        self._timeout = timeout

        self._seed = seed
        self._iteration = 0
        
        if self.keeps_cache:
            self.cache = CacheManager('openai')

    def __build_keys(self, system_prompt, user_prompt, model, temperature):
        return (
            system_prompt,
            user_prompt,
            model,
            temperature,
            self._seed,
            self._iteration
        )

    def __get_response_from_cache(self, system_prompt, user_prompt, model, temperature: float = 1.0):
        keys = self.__build_keys(
            system_prompt,
            user_prompt,
            model,
            temperature
        )

        if self.cache.contains_key(*keys):
            self._iteration += 1
            return self.cache.get_value(*keys)
        
        return self.__get_response_from_openai(
            system_prompt, 
            user_prompt, 
            model,
            temperature=temperature
        )

    def __get_response_from_openai(self, system_prompt, user_prompt, model, temperature: float = 1.0):
        keys = self.__build_keys(
            system_prompt,
            user_prompt,
            model,
            temperature
        )
        
        messages = []

        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        
        if user_prompt is not None:
            messages.append({"role": "user", "content": user_prompt})

        print("[API CALL]")
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=self._max_tokens,
            timeout=self._timeout,
            temperature=temperature,
        )
        result = response.choices[0].message.content

        if self.keeps_cache:
            self.cache.set_value(*keys, value = result)
        
        self._iteration += 1
        return result

    # Results only stay reproducible if cache is used. Results are not reproducible without the same cache.
    def get_response(self, system_prompt: str = None, user_prompt: str = None, model: str = None, temperature: float = 1.0):
        if user_prompt is None and system_prompt is None:
            raise Exception('[OPENAI PROMPT MANAGER] User prompt and system prompt cannot be empty at the same time')
        if self.keeps_cache:
            return self.__get_response_from_cache(system_prompt, user_prompt, model, temperature=temperature)
        else:
            return self.__get_response_from_openai(system_prompt, user_prompt, model, temperature=temperature)
