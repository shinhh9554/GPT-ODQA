def preprocess_rerank_function(examples, tokenizer, max_length):
    inputs = tokenizer(
        examples['query'],
        examples["context"],
        max_length=max_length,
        truncation="only_second",
        return_token_type_ids=True,  # roberta모델을 사용할 경우 False, bert를 사용할 경우 True로 표기해야합니다.
        padding="max_length",
    )
    return inputs


def get_score(el_score, re_score, el_p=0.5, re_p=0.5):
    final_score = el_score * el_p + re_score * re_p
    return final_score

if __name__ == '__main__':
    a = 1
    b = 2
    print(a+b)