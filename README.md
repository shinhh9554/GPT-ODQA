# GPT-ODQA
Open AI의 GPT3.5 API를 사용한 ODQA 시스템

## 1. 개요
기존의 ODQA 시스템을 Bing + ChatGPT와 같이 변경하기 위해 OpenAI의 GPT 3.5 API를 사용하였습니다. 그 결과 기존 기계독해 모델을 사용하였을 때보다 재미있는 답변들이 도출되었습니다. 시스템 구조도는 아래 그림과 같습니다.

![odqa+gpt](https://user-images.githubusercontent.com/57481142/228465209-9f6e1bfb-41df-4827-bdaa-31ef547d7932.png)

## 2. 특징
* 검색엔진은 Elasticsearch 7.17 버전을 사용하였습니다.
* 재순위화 모델은 [이 논문](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11225036)에 나온 것을 사용하였습니다.
* Generator는 OpenAI의 GPT3.5 모델 중 gpt-3.5-turbo를 사용하였습니다.
* 시스템 UI는 Streamlit을 사용하여 제작하였습니다.
* [데모 시스템](http://icl.kyonggi.ac.kr:5003)

![ezgif com-video-to-gif-3](https://user-images.githubusercontent.com/57481142/228516536-3b4d91d7-3079-499f-8dd7-ebe9e0d14023.gif)
---
![ezgif com-video-to-gif-2](https://user-images.githubusercontent.com/57481142/228514555-b3cb5fbd-a908-4443-99af-ee48763f3019.gif)


## 3. 기타사항
* 검색엔진에 동의어 및 사용자 정의 사전은 별도로 구축하셔서 Elasticsearch Config에 업로드 하셔야 합니다.
* 검색 대상 데이터는 위키피디아 데이터를 별도로 정제하여 ./context_data/sample.json과 같이 구성하여 업로드하였습니다.
```
    {
      "id": "wiki_0_0",
      "row": {
        "title": "지미 카터",
        "context": "제임스 얼 카터 주니어(1924년 10월 1일 ~ )는 민주당 출신 미국의 제39대 대통령(1977년 ~ 1981년) 이다. 지미 카터는 조지아주 섬터 카운티 플레인스 마을에서 태어났다. 조지아 공과대학교를 졸업하였다. 그 후 해군에 들어가 전함·원자력·잠수함의 승무원으로 일하였다. 1953년 미국 해군 대위로 예편하였고 이후 땅콩·면화 등을 가꿔 많은 돈을 벌었다. 그의 별명이 \"땅콩 농부\" (Peanut Farmer)로 알려졌다. 1962년 조지아주 상원 의원 선거에서 낙선하였으나, 그 선거가 부정선거 였음을 입증하게 되어 당선",
        "author": "",
        "publish": "https://ko.wikipedia.org/wiki?curid=5",
        "date": ""
      }
    },
    {
      "id": "wiki_0_1",
      "row": {
        "title": "지미 카터",
        "context": "조지아주 상원 의원 선거에서 낙선하였으나, 그 선거가 부정선거 였음을 입증하게 되어 당선되고, 1966년 조지아 주지사 선거에 낙선하지만, 1970년 조지아 주지사를 역임했다. 대통령이 되기 전 조지아주 상원의원을 두번 연임했으며, 1971년부터 1975년까지 조지아 지사로 근무했다. 조지아 주지사로 지내면서, 미국에 사는 흑인 등용법을 내세웠다. 1976년 미합중국 제39대 대통령 선거에 민주당 후보로 출마하여 도덕주의 정책으로 내세워서, 많은 지지를 받고 제럴드 포드 대통령을 누르고 당선되었다. 카터 대통령은 에너지 개발을 촉",
        "author": "",
        "publish": "https://ko.wikipedia.org/wiki?curid=5",
        "date": ""
      }
    },
```
* 재순위화 모델은 [여기서]() 다운로드 받을 수 있으며, 모델의 inference 부분은 inference.py 코드를 확인하시면 됩니다.

## 4. Reference
* ### [es-gpt](https://github.com/hunkim/es-gpt)

