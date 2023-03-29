import torch
from datasets import Dataset
import torch.nn.functional as F
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, DataCollatorWithPadding, set_seed, AutoModelForSequenceClassification

from utils import preprocess_rerank_function


SPECIAL_CHAR = ['(', ')', '{', '}', '[', ']', '^', '~', '/', ':', '?', '!']
SPECIAL_CHAR2 = ["'", '"']

set_seed(42)


# Re-rank Inference
class RerankInference:
    def __init__(self, device):
        path = 'models/re-rank'
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
        self.model.to(self.device)
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer, pad_to_multiple_of=None)
        self.max_length = 512

    def inference(self, question, contexts):
        examples = self.convert_dataset_dict(question, contexts)
        inference_dataset = examples.map(
            preprocess_rerank_function,
            batched=True,
            fn_kwargs={"tokenizer": self.tokenizer, "max_length": self.max_length}
        )
        result = self.rerank(inference_dataset)
        return result

    def rerank(self, inputs):
        with torch.no_grad():
            inputs = inputs.remove_columns(["query", "context"])
            test_dataloader = DataLoader(
                inputs, collate_fn=self.data_collator, batch_size=100, shuffle=False
            )

            # Don't forget turn-on evaluation mode.
            self.model.eval()

            # Predictions
            result = []
            for batch in test_dataloader:
                batch = batch.to(self.device)
                outputs = self.model(**batch)[0]
                prob = F.softmax(outputs, dim=1)
                for i in range(len(prob)):
                    positive_prob = round(prob[i][1].item(), 5) * 100
                    pred = "1" if torch.argmax(prob[i]) == 1 else "0"
                    result.append((pred, positive_prob))

            return result
    @staticmethod
    def convert_dataset_dict(question, contexts):
        data = []
        for context in contexts:
            data.append({"query": question, "context": context})
        dataset = Dataset.from_list(data)

        return dataset
