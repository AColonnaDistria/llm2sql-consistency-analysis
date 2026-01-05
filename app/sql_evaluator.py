import pandas as pd
import textdistance
import sqlglot

class SQLEvaluator:
    """PUBLIC"""

    def __init__(self, candidates):
        self.candidates = candidates

    def get_heatmap(self, score_cmp) -> pd.DataFrame:
        index = [f"Query{i}" for i in range(len(self.candidates))]

        matches = pd.DataFrame(0.0, index=index, columns=index)

        for i0 in range(len(self.candidates)):
            index0 = index[i0]
            candidate0 = self.candidates[i0]

            for i1 in range(len(self.candidates)):
                index1 = index[i1]
                candidate1 = self.candidates[i1]
                
                matches.loc[index0, index1] = score_cmp(candidate0, candidate1)

        return matches

    def get_score(self, score_function) -> pd.DataFrame:
        index = [f"Query{i}" for i in range(len(self.candidates))]

        scores = pd.DataFrame(0.0, index=index, columns=["score"])

        for i0 in range(len(self.candidates)):
            index0 = index[i0]
            candidate0 = self.candidates[i0]

            scores.loc[index0, "score"] = score_function(candidate0)

        return scores

class SQLValidityEvaluator(SQLEvaluator):
    """PUBLIC"""

    def __init__(self, candidates):
        super().__init__(candidates)

    def parsable_scores(self) -> pd.DataFrame:
        return self.get_score(self.__parsable_score)

    """PRIVATE"""

    def __parsable_score(self, s1: str) -> float:
        return (1.0 if self.__is_parsable_sql(s1) else 0.0)

    def __is_parsable_sql(self, query: str) -> bool:
        try:
            sqlglot.parse_one(query)
            return True
        except sqlglot.errors.ParseError:
            return False

class SQLSyntaxicEvaluator(SQLEvaluator):
    """PUBLIC"""

    def __init__(self, candidates):
        super().__init__(candidates)

    def exact_matches(self) -> pd.DataFrame:
        return self.get_heatmap(self.__match)

    def levenhstein_normalized(self) -> pd.DataFrame:
        return self.get_heatmap(self.__levenhstein_distance_normalized)

    """PRIVATE"""

    def __match(self, s1: str, s2: str) -> float:
        return 1.0 if (s1 == s2) else 0.0

    def __levenhstein_distance_normalized(self, s1: str, s2: str) -> float:
        words_s1 = s1.split()
        words_s2 = s2.split()

        max_len = max(len(words_s1), len(words_s2))

        return textdistance.levenshtein.distance(words_s1, words_s2) / max_len

class SQLStructuralEvaluator(SQLEvaluator): 
    """PUBLIC"""

    def __init__(self, candidates):
        super().__init__(candidates)

    def exact_matches(self) -> pd.DataFrame:
        return self.get_heatmap(self.__match)

    def levenhstein_normalized(self) -> pd.DataFrame:
        return self.get_heatmap(self.__levenhstein_distance_normalized)

    """PRIVATE"""

    def __ast_to_tokens(self, ast):
        return [
            node.key
            for node in ast.walk()
            if node.key is not None
        ]

    def __match(self, s1: str, s2: str) -> pd.DataFrame:
        norm1 = sqlglot.parse_one(s1).sql(pretty=False)
        norm2 = sqlglot.parse_one(s2).sql(pretty=False)

        return 1.0 if (norm1 == norm2) else 0.0

    def __levenhstein_distance_normalized(self, s1: str, s2: str) -> float:
        ast1 = sqlglot.parse_one(s1)
        ast2 = sqlglot.parse_one(s2)

        t1 = self.__ast_to_tokens(ast1)
        t2 = self.__ast_to_tokens(ast2)

        max_len = max(len(t1), len(t2))

        return textdistance.levenshtein.distance(t1, t2) / max_len
