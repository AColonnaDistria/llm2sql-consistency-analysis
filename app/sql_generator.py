import pandas as pd
from prompt_manager import OpenaiPromptManager

class MySQLGenerator:
    def __init__(self, system_prompt=None, seed=0, temperature=1.0, keeps_cache=True):
        if system_prompt == None:
            system_prompt = """
You are an expert MySQL Data Engineer. Your goal is to convert natural language questions into valid, efficient MySQL SQL queries based on a provided database schema.

### INSTRUCTIONS:
1. **Dialect:** Use standard MySQL syntax.
2. **Schema Compliance:** Use ONLY the table and column names provided in the schema below. Do not hallucinate tables or columns.
3. **Output Format:**
   - Output **ONLY** the raw SQL code.
   - Do **NOT** use Markdown blocks (e.g., ```sql).
   - Do **NOT** include explanations, comments, or conversational text (e.g., "Here is the query").
   - The output must be directly executable by a MySQL driver.

### SCHEMA:
{schema}
"""
        self.seed = seed
        self.temperature = temperature
        self.keeps_cache = keeps_cache

        self.system_prompt = system_prompt
        self.prompt_manager = OpenaiPromptManager(
            seed=seed,
            keeps_cache=keeps_cache
        )

    def generate_query(self, user_prompt: str = None, schema: str = None, sys_prompt = None) -> str:
        try:
            if sys_prompt is None:
                sys_prompt = self.system_prompt.format(schema = schema)
            else:
                sys_prompt = sys_prompt.format(schema = schema)
            
            query = self.prompt_manager.get_response(
                system_prompt = sys_prompt, 
                user_prompt = user_prompt,
                temperature = self.temperature,
                model = "gpt-4o-mini"
            )

            # Normalize the query
            query = query.replace('```sql', '').replace('```mysql', '').replace('```', '').strip()

            return query
        except Exception as e:
            print(f"[GENERATOR ERROR]: {e}")
            return None

    """Generate a SQL dataframe corresponding to the prompt"""
    def generate_queries(self, user_prompt: str, schema: str, size: int = 1) -> pd.DataFrame:
        try:
            sys_prompt = self.system_prompt.format(schema = schema)
            responses = []

            for i in range(size):
                query = self.generate_query(
                    user_prompt=user_prompt, 
                    schema=schema,
                    sys_prompt=sys_prompt
                )

                responses.append({
                    "user_prompt": user_prompt,
                    "schema": schema,
                    "temperature": self.temperature,
                    "query": query
                })

            return pd.DataFrame(responses)
        except Exception as e:
            print(f"[GENERATOR ERROR]: {e}")
            return None