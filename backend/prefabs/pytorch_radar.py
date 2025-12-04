from breeze import NodeType, formatting
import numpy as np
import kagglehub
import shutil
import os
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import torch
import plotly.express as px
from tqdm import tqdm


@NodeType(tags=["kaggle"])
def download_kaggle_dataset():
    path = kagglehub.dataset_download("iroldan/real-doppler-raddar-database")
    output_dir = shutil.copytree(
        f"{path}/data", "backend/data_radar/.kaggle", dirs_exist_ok=True
    )
    return output_dir


@NodeType(tags=["kaggle"])
def load_dataset(dataset_dir: str):
    data_per_label = []
    labels_per_label = []
    for label in os.listdir(dataset_dir):
        data_to_stack = []
        for data_folder in os.listdir(f"{dataset_dir}/{label}"):
            for csv_name in os.listdir(f"{dataset_dir}/{label}/{data_folder}"):
                csv_data = pd.read_csv(
                    f"{dataset_dir}/{label}/{data_folder}/{csv_name}"
                ).to_numpy()
                data_to_stack.append(csv_data)

        label_data = np.stack(data_to_stack)
        # comment below
        # label_data.fill(ord(label[0]))
        data_per_label.append(label_data)

        labels_arr = np.full(label_data.shape[0], label)
        labels_per_label.append(labels_arr)

    # concatenate collected arrays per label
    X = np.concatenate(data_per_label, axis=0)
    y = np.concatenate(labels_per_label, axis=0)

    p = np.random.permutation(X.shape[0])
    X = X[p]
    y = y[p]

    return X, y


class DopplerRadarDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray, mode: str, test_ratio: float):
        assert X.shape[0] == y.shape[0], "invalid shape"

        split_idx = int(y.shape[0] * test_ratio)
        labels = np.unique(y)

        label_to_idx = {label: i for i, label in enumerate(labels)}
        y_idx = np.vectorize(lambda v: label_to_idx[v])(y).astype(np.int64)

        if mode == "test":
            self.X: torch.Tensor = torch.tensor(X[:split_idx], dtype=torch.float32)
            self.y: torch.Tensor = torch.tensor(y_idx[:split_idx], dtype=torch.long)
        elif mode == "train":
            self.X: torch.Tensor = torch.tensor(X[split_idx:], dtype=torch.float32)
            self.y: torch.Tensor = torch.tensor(y_idx[split_idx:], dtype=torch.long)

    def __len__(self) -> int:
        return self.y.shape[0]

    def __getitem__(self, idx: int):
        return self.X[idx], self.y[idx]


class DopplerRadarClassifier(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.flatten = torch.nn.Flatten()
        self.normalize = torch.nn.LayerNorm(10 * 61)
        self.layer1 = torch.nn.Linear(10 * 61, 256)
        self.dropout = torch.nn.Dropout()
        self.relu1 = torch.nn.ReLU()
        self.layer2 = torch.nn.Linear(256, 64)
        self.relu2 = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout()
        self.layer3 = torch.nn.Linear(64, 3)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x: torch.Tensor):
        x = x.type(torch.float32)

        flattened = self.flatten(x)
        normalized = self.normalize(flattened)
        layer_1_output = self.relu1(self.layer1(normalized))
        dropped = self.dropout(layer_1_output)
        layer_2_output = self.relu2(self.layer2(dropped))
        layer_3_output = self.layer3(layer_2_output)
        return layer_3_output


@NodeType(tags=["pytorch"])
def create_train_dataset(data: tuple, test_ratio: float):
    X, y = data
    return DopplerRadarDataset(
        X,
        y,
        mode="train",
        test_ratio=test_ratio,
    )


@NodeType(tags=["pytorch"])
def create_test_dataset(data: tuple, test_ratio: float):
    X, y = data
    return DopplerRadarDataset(
        X,
        y,
        mode="test",
        test_ratio=test_ratio,
    )


@NodeType(tags=["pytorch"])
def set_test_ratio(test_ratio: float) -> float:
    return test_ratio


@NodeType(tags=["pytorch"])
def create_model() -> DopplerRadarClassifier:
    return DopplerRadarClassifier()


@NodeType(tags=["pytorch"])
def create_loss_fn():
    return torch.nn.CrossEntropyLoss()


@NodeType(tags=["builtin"])
def select_by_index(collection, idx: int):
    return collection[idx]


@NodeType(tags=["pytorch"])
def training_loop(
    model: torch.nn.Module,
    epochs: int,
    train_dataset: torch.utils.data.Dataset,
    test_dataset: torch.utils.data.Dataset,
    batch_size: int,
    loss_fn,
):
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()

    for epoch in range(epochs):
        epoch_loss = 0

        for inputs, labels in tqdm(
            DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        ):
            optimizer.zero_grad()
            pred_labels = model(inputs)
            loss = loss_fn(pred_labels, labels)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        mean_train_loss = epoch_loss / (len(train_dataset) // batch_size)
        if epoch % 2 == 0:
            with torch.no_grad():
                test_loss = 0
                total_correct = 0
                for inputs, labels in DataLoader(
                    test_dataset, batch_size, shuffle=True
                ):
                    pred_labels = model(inputs)

                    test_loss += loss_fn(pred_labels, labels).item()

                    total_correct += sum(labels == pred_labels.argmax(axis=1))

                mean_test_loss = test_loss / (len(test_dataset) // batch_size)
                test_accuracy = total_correct / len(test_dataset)

            print(
                f"Epoch {epoch} with loss: {mean_train_loss:.3f} and val loss {mean_test_loss:.3f} with accuracy {test_accuracy:.3f}"
            )
        else:
            print(f"Epoch {epoch} with loss: {mean_train_loss}")

    return model


@NodeType(tags=["plotly"])
def doppler_display(data_tuple):
    data, label = data_tuple
    return px.imshow(data, title=str(label))


@NodeType(tags=["pytorch"])
def check_model_accuracy(model, test_dataset):
    with torch.no_grad():
        total_correct = 0
        for inputs, labels in DataLoader(test_dataset, 64, shuffle=True):
            pred_labels = model(inputs)
            total_correct += sum(labels == pred_labels.argmax(axis=1))
        return total_correct / len(test_dataset)


formatting.add_display_format(
    np.ndarray,
    lambda x: f"np.ndarray(shape={x.shape}, dtype={x.dtype})",
)
formatting.add_tag_color_mapping("kaggle", "#4c36c7")
formatting.add_tag_color_mapping("pytorch", "#f5742f")
