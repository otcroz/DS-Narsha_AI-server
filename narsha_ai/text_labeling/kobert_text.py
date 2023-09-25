import torch
from torch import nn
import gluonnlp as nlp
from transformers import BertModel
from torch.utils.data import Dataset
import numpy as np
from kobert_tokenizer import KoBERTTokenizer
from tqdm import tqdm, tqdm_notebook
import torch.nn.functional as F

max_len = 64
batch_size = 64
test_model = ""
tokenizer = ""
vocab = ""

def load_pretrain_bert():
    global test_model, tokenizer, vocab
    bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
    test_model = BERTClassifier(bertmodel, dr_rate=0.5)
    test_model.load_state_dict(torch.load('./models/bert_model_parameter.pt', map_location=torch.device('cpu')))
    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')


def kobert_classify(input):
    check_data = [input, '0']
    check_data_another = [check_data]

    another_test = BERTDataset(check_data_another, 0, 1, tokenizer, vocab, max_len, True, False)
    input_dataloder = torch.utils.data.DataLoader(another_test, batch_size=64, num_workers=4)

    test_model.eval()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(input_dataloder):
        out = test_model(token_ids.long(), valid_length, segment_ids.long())
        tensor_logits = out
        tensor_logits = tensor_logits.detach().numpy()

        return np.argmax(tensor_logits)

def kobert_classify_lime(input, text_count):

    another_test = BERTDataset(input, 0, 1, tokenizer, vocab, max_len, True, False)
    input_dataloder = torch.utils.data.DataLoader(another_test, batch_size=text_count, num_workers=4)

    test_model.eval()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(input_dataloder):
        out = test_model(token_ids.long(), valid_length, segment_ids.long())
        tensor_logits = out
        probas = F.sigmoid(tensor_logits).detach().numpy()  # tensor to numpy

        return probas


class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=2,
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len,
                 pad, pair):
        transform = BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len,vocab=vocab, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))


class BERTSentenceTransform:
    def __init__(self, tokenizer, max_seq_length,vocab, pad=True, pair=True):
        self._tokenizer = tokenizer
        self._max_seq_length = max_seq_length
        self._pad = pad
        self._pair = pair
        self._vocab = vocab

    def __call__(self, line):
        # convert to unicode
        text_a = line[0]
        if self._pair:
            assert len(line) == 2
            text_b = line[1]

        tokens_a = self._tokenizer.tokenize(text_a)
        tokens_b = None

        if self._pair:
            tokens_b = self._tokenizer(text_b)

        if tokens_b:
            self._truncate_seq_pair(tokens_a, tokens_b,
                                    self._max_seq_length - 3)
        else:
            if len(tokens_a) > self._max_seq_length - 2:
                tokens_a = tokens_a[0:(self._max_seq_length - 2)]

        vocab = self._vocab
        tokens = []
        tokens.append(vocab.cls_token)
        tokens.extend(tokens_a)
        tokens.append(vocab.sep_token)
        segment_ids = [0] * len(tokens)

        if tokens_b:
            tokens.extend(tokens_b)
            tokens.append(vocab.sep_token)
            segment_ids.extend([1] * (len(tokens) - len(segment_ids)))

        input_ids = self._tokenizer.convert_tokens_to_ids(tokens)

        # The valid length of sentences. Only real  tokens are attended to.
        valid_length = len(input_ids)

        if self._pad:
            # Zero-pad up to the sequence length.
            padding_length = self._max_seq_length - valid_length
            # use padding tokens for the rest
            input_ids.extend([vocab[vocab.padding_token]] * padding_length)
            segment_ids.extend([0] * padding_length)

        return np.array(input_ids, dtype='int32'), np.array(valid_length, dtype='int32'),\
            np.array(segment_ids, dtype='int32')