import json

import torch
import openai

from utils import get_score
from es import ElasticSearch
from inference import RerankInference


class GPTOdqa:
    def __init__(self, index_name):
        self.index_name = index_name

        # device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # model
        self.model_engine = "gpt-3.5-turbo"
        self.api_key = ""
        openai.api_key = self.api_key

        # elasticsearch
        self.es = ElasticSearch()

        # re-rank
        self.re_rank = RerankInference(device=device)

    def search(self, query):
        # 검색 결과
        results = self.es.search(self.index_name, question=query)

        # context 집합
        context_list = [result[1] for result in results]

        # re_rank 확률
        re_rank_scores = self.re_rank.inference(query, context_list)

        # 취합 및 통합 점수 계산
        results = [[query] + result + [get_score(result[-1], re_rank_scores[idx][-1])]
                  for idx, result in enumerate(results) if re_rank_scores[idx][0] == '1']

        return results

    def gpt_answer(self, query, context, st):
        if context:
            prompt = f"{context}\n\n 위 내용을 바탕으로 \"{query}\" 이 질문에 대한 답을 찾아줘."
        else:
            prompt = f"{query}"

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user',
                 'content': f'{prompt}'}
            ],
            temperature=0,
            stream=True  # again, we set stream=True
        )

        collected_chunks = []
        collected_messages = []
        for chunk in response:
            collected_chunks.append(chunk)
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)
            messages = ''.join([m.get('content', '') for m in collected_messages])
            messages.replace("\n", "")
            st.markdown(f'{messages}')
