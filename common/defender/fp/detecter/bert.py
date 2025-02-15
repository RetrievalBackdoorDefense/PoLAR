import torch
import os
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from torch.optim import AdamW


class BERTDetecter:
    def __init__(
        self,
        model_name="bert-base-uncased",
        num_labels=2,
        device="cuda:0",
        dropout=0.2,
        output_dir=None,
    ):
        self.device = device
        model_name = "/home/hust-ls/worksapce/RetrievalBackdoor/common/pretrained-model/bert-base-uncased"

        config = BertConfig.from_pretrained(
            model_name,
            num_labels=num_labels,
            hidden_dropout_prob=dropout,
            attention_probs_dropout_prob=dropout,
            output_hidden_states=True,
        )

        self.model = BertForSequenceClassification.from_pretrained(
            model_name, config=config
        )

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels
        )
        self.model.to(self.device)
        self.optimizer = AdamW(self.model.parameters(), lr=5e-5)

        assert output_dir
        self.output_dir = output_dir

        self.valid = False

    def get_valid(self):
        return self.valid

    def train_step(self, inputs, labels):
        inputs = self.tokenizer(
            inputs, return_tensors="pt", padding=True, truncation=True
        )
        labels = torch.tensor(labels).to(self.device)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.model(**inputs, labels=labels)
        loss = outputs.loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.valid = True

        return loss.item()

    def t_SNE(self, features, labels):
        import matplotlib.pyplot as plt
        from sklearn.manifold import TSNE

        if isinstance(features, torch.Tensor):
            features = features.cpu().numpy()

        print(f"features = {features.shape}")
        tsne = TSNE(n_components=2, random_state=42)

        features_2d = tsne.fit_transform(features)

        plt.figure(figsize=(10, 8))
        if labels is not None:
            plt.scatter(
                features_2d[:, 0],
                features_2d[:, 1],
                c=labels,
                cmap="viridis",
                s=50,
                alpha=0.7,
            )
            plt.colorbar(label="Labels")
        else:
            plt.scatter(features_2d[:, 0], features_2d[:, 1], s=50, alpha=0.7)

        plt.grid(True)
        plt.savefig(os.path.join(self.output_dir, "t-SNE.png"), dpi=300)

    def feature(self, inputs):

        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(
                inputs, return_tensors="pt", padding=True, truncation=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs, output_hidden_states=True)
            hidden_states = outputs.hidden_states
            hidden_states = hidden_states[-1][:, 0, :]

        return hidden_states

    def predict(self, inputs):
        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(
                inputs, return_tensors="pt", padding=True, truncation=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1)
        return predictions

    def logits(self, inputs):
        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(
                inputs, return_tensors="pt", padding=True, truncation=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
            logits = outputs.logits
        return logits

    def save(self):
        torch.save(
            self.model.state_dict(), os.path.join(self.output_dir, "detecter.pt")
        )

    def load(self):
        assert os.path.exists(os.path.join(self.output_dir, "detecter.pt"))
        self.model.load_state_dict(
            torch.load(os.path.join(self.output_dir, "detecter.pt"))
        )
        self.valid = True
