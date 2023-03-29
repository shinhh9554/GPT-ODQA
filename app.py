import time
import asyncio

import streamlit as st

from templates import *
from gpt_odqa import GPTOdqa

odqa = GPTOdqa(index_name='odqa')

def main():
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    """, unsafe_allow_html=True)

    # layout my app
    st.title('Open Domain Q&A + GPT')
    search = st.text_input('Enter search question')
    sample = st.selectbox('예시 질문을 선택해주세요.',
                          ('',
                           '국회도서관이 하는 일은 무엇인가?',
                           '코로나 19가 최초로 발생한 국가는?',
                           '대한민국 제16대 대통령 선거에서 당선된 사람은 누구인가?'))

    if search == "" and sample:
        search = sample

    if search:
        # 검색 수행
        es_start = time.time()
        try:
            results = odqa.search(search)
        except:
            results = []
        es_end = time.time()
        es_time = es_end - es_start
        st.write(number_of_results(len(results), es_time),
                 unsafe_allow_html=True)


        st.markdown("### GPT 생성 결과")
        with st.spinner("wait for it"):
            # GPT 결과 box 생성
            st.markdown("---")
            answer_result = st.empty()
            answer_result.info("잠시만 기다려 주세요")

            if len(results) > 0:
                # 검색 결과 정렬
                st.markdown("---")
                st.markdown("### 검색 결과")
                for result in results:
                    st.write(card(title=result[3], context=result[2]), unsafe_allow_html=True)
                context = results[0][2]
                odqa.gpt_answer(search, context, answer_result)
            else:
                context = ""
                odqa.gpt_answer(search, context, answer_result)

if __name__ == '__main__':
    main()