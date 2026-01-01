import openai

from dotenv import load_dotenv
import os

from diskcache import Cache
import hashlib

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class PromptManager:
    def __init__(self, api_key: str = OPENAI_API_KEY, seed: int = 0, keeps_cache: bool = True):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.keeps_cache = keeps_cache

        self._seed = seed
        self._iteration = 0

        if self.keeps_cache:
            self.cache = Cache('cache/openai_cache')

    def __get_cache_key(self, *items):
        hasher = hashlib.md5()
        
        for item in items:
            hasher.update(str(item).encode('utf-8'))
        
        cache_key = hasher.hexdigest()
        return cache_key

    def __get_response_from_cache(self, system_prompt, user_prompt, model, temperature: float = 1.0):
        #index = f"system_prompt:'{system_prompt}'&user_prompt:'{user_prompt}'&model:'{model}'&seed:'{self._seed}'&iteration:'{self._iteration}'&temperature:'{temperature}'"
        cache_key = self.__get_cache_key(
            system_prompt,
            user_prompt,
            model,
            self._seed,
            self._iteration,
            temperature
        )

        if cache_key in self.cache:
            print(f"[CACHE HIT] Iteration {self._iteration}")

            self._iteration += 1
            return self.cache[cache_key]
        else:
            return self.__get_response_from_openai(
                system_prompt, 
                user_prompt, 
                model, 
                cache_key, 
                temperature=temperature
            )

    def __get_response_from_openai(self, system_prompt, user_prompt, model, cache_key, temperature: float = 1.0):
        messages = []

        if system_prompt != None:
            messages.append({"role": "system", "content": system_prompt})
        
        if user_prompt != None:
            messages.append({"role": "user", "content": user_prompt})

        if user_prompt == None and system_prompt == None:
            raise Exception('[PROMPT MANAGER] User prompt and system prompt cannot be empty at the same time')

        print("[API CALL]")
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        result = response.choices[0].message.content

        if self.keeps_cache and cache_key:
            self.cache[cache_key] = result

        self._iteration += 1
        return result

    # Results only stay reproducible if cache is used. Results are not reproducible without the same cache.
    def get_response(self, system_prompt: str = None, user_prompt: str = None, model: str = "gpt-4o", temperature: float = 1.0):
        if self.keeps_cache:
            return self.__get_response_from_cache(system_prompt, user_prompt, model, temperature=temperature)
        else:
            return self.__get_response_from_openai(system_prompt, user_prompt, model, None, temperature=temperature)
