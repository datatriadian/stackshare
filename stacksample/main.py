from pathlib import Path
from typing import Optional

import pandas as pd
from typer import Option, Typer

from stacksample.console import console
from stacksample.loader import load_all
from stacksample.training import combine_and_format_data, train_model

app = Typer()
_DEFAULT_ENCODING = "ISO8859-1"


@app.command()
def view_labels(
    answers_file_path: Path = Option(
        Path("data/Answers.csv"), help="The path to the answers file. Default = data/Answers.csv"
    ),
    answers_file_encoding: str = Option(
        _DEFAULT_ENCODING, help=f"The encoding of the answers file. Default = {_DEFAULT_ENCODING}"
    ),
    questions_file_path: Path = Option(
        Path("data/Questions.csv"),
        help="The path to the quesions file. Default = data/Questions.csv",
    ),
    questions_file_encoding: str = Option(
        _DEFAULT_ENCODING, help=f"The encoding of the questions file. Default = {_DEFAULT_ENCODING}"
    ),
    tags_file_path: Path = Option(
        Path("data/Tags.csv"), help="The path to the tags file. Default = data/Tags.csv"
    ),
    tags_file_encoding: str = Option(
        _DEFAULT_ENCODING, help=f"The encoding of the tags file. Default = {_DEFAULT_ENCODING}"
    ),
    remove_html_tags: bool = Option(
        False, help="If this flag is set HTML tags will be removed. Default = False"
    ),
    remove_line_breaks: bool = Option(
        False, help="If this flag is set line breaks will be removed. Default = False"
    ),
    minimum_labels: Optional[int] = Option(
        None, help="Only keep labels with the specified number of samples. Default = None"
    ),
    reduce_number_of_samples: Optional[int] = Option(
        None,
        help="If set this will be the maximum number of records used for testing and training. Default = None",
    ),
    random_state: Optional[int] = Option(
        None, help="Random state to use for reproducability. Default = None"
    ),
    crop_sentences: Optional[int] = Option(
        None, help="Crop sentences to a maximum number of characters. Default = None"
    ),
    exclude_title: bool = Option(
        False, help="If this flag is set the title column in will be excluded. Default = False"
    ),
    exclude_answers: bool = Option(
        False, help="If this flag is set the answers will be excluded. Default = False"
    ),
) -> None:
    with console.status("Loading data..."):
        answers, questions, tags = load_all(
            answers_file=answers_file_path,
            answers_encoding=answers_file_encoding,
            questions_file=questions_file_path,
            questions_encoding=questions_file_encoding,
            tags_file=tags_file_path,
            tags_encoding=tags_file_encoding,
        )

    with console.status("Preparing data..."):
        df = combine_and_format_data(
            answers=answers,
            questions=questions,
            tags=tags,
            remove_html_tags=remove_html_tags,
            remove_line_breaks=remove_line_breaks,
            minimum_labels=minimum_labels,
            reduce_number_of_samples=reduce_number_of_samples,
            crop_sentences=crop_sentences,
            random_state=random_state,
            exclude_answers=exclude_answers,
            exclude_title=exclude_title,
        )

    pd.set_option("display.max_rows", df.shape[0] + 1)
    console.print(df.groupby("tag").size())


@app.command()
def train(
    answers_file_path: Path = Option(
        Path("data/Answers.csv"), help="The path to the answers file. Default = data/Answers.csv"
    ),
    answers_file_encoding: str = Option(
        _DEFAULT_ENCODING, help=f"The encoding of the answers file. Default = {_DEFAULT_ENCODING}"
    ),
    questions_file_path: Path = Option(
        Path("data/Questions.csv"),
        help="The path to the quesions file. Default = data/Questions.csv",
    ),
    questions_file_encoding: str = Option(
        _DEFAULT_ENCODING, help=f"The encoding of the questions file. Default = {_DEFAULT_ENCODING}"
    ),
    tags_file_path: Path = Option(
        Path("data/Tags.csv"), help="The path to the tags file. Default = data/Tags.csv"
    ),
    tags_file_encoding: str = Option(
        _DEFAULT_ENCODING, help=f"The encoding of the tags file. Default = {_DEFAULT_ENCODING}"
    ),
    remove_html_tags: bool = Option(
        False, help="If this flag is set HTML tags will be removed. Default = False"
    ),
    remove_line_breaks: bool = Option(
        False, help="If this flag is set line breaks will be removed. Default = False"
    ),
    reduce_number_of_samples: Optional[int] = Option(
        None,
        help="If set this will be the maximum number of records used for testing and training. Default = None",
    ),
    test_size: float = Option(
        0.2,
        help="The percentage of data to be used for training as a float. Default = 0.2",
    ),
    random_state: Optional[int] = Option(
        None, help="Random state to use for reproducability. Default = None"
    ),
    minimum_labels: Optional[int] = Option(
        None, help="Only keep labels with the specified number of samples. Default = None"
    ),
    crop_sentences: Optional[int] = Option(
        None, help="Crop sentences to a maximum number of characters. Default = None"
    ),
    exclude_title: bool = Option(
        False, help="If this flag is set the title column in will be excluded. Default = False"
    ),
    exclude_answers: bool = Option(
        False, help="If this flag is set the answers will be excluded. Default = False"
    ),
    balance_train_data: bool = Option(
        False,
        help="If this flag is set oversampling will be preformed on the train data. Default = False",
    ),
    c_value: float = Option(1.0, "-c", help="Sets the C value for the SVM. Default = 1.0"),
) -> None:
    with console.status("Loading data..."):
        answers, questions, tags = load_all(
            answers_file=answers_file_path,
            answers_encoding=answers_file_encoding,
            questions_file=questions_file_path,
            questions_encoding=questions_file_encoding,
            tags_file=tags_file_path,
            tags_encoding=tags_file_encoding,
        )

    with console.status("Preparing data..."):
        df = combine_and_format_data(
            answers=answers,
            questions=questions,
            tags=tags,
            remove_html_tags=remove_html_tags,
            remove_line_breaks=remove_line_breaks,
            minimum_labels=minimum_labels,
            reduce_number_of_samples=reduce_number_of_samples,
            crop_sentences=crop_sentences,
            random_state=random_state,
            exclude_answers=exclude_answers,
            exclude_title=exclude_title,
        )

    with console.status("Training..."):
        train_model(
            df,
            test_size=test_size,
            random_state=random_state,
            balance_train_dataset=balance_train_data,
            c_value=c_value,
        )


if __name__ == "__main__":
    app()
