import argparse
import os
from pathlib import Path
from typing import List
import yaml
import json


class Manifest:
    """
    Data model for human readable manifest files.
    """
    intents: List[str] = []

    def __init__(self, intents: List[str]):
        self.intents = intents


class HumanIntent:
    """
    Data model for human readable intent files.
    """
    name: str
    sentences: List[str]

    def __init__(self, name: str, sentences: List[str]):
        self.name = name
        self.sentences = sentences

    def __repr__(self):
        return "{name}{sentences}".format(name=self.name, sentences=self.sentences)


class FilesReader:
    """
    Read the human readable intents from the input folder. Each intent file should have this format :
    <INTENT_NAME>.yaml and contains the list of sentences in the yaml format.
    """
    _data_folder: str
    _manifest: Manifest

    def __init__(self, data_folder: str, manifest_file: str):
        self._data_folder = data_folder
        self._manifest = FilesReader.read_manifest(manifest_file)

    @staticmethod
    def read_manifest(file) -> Manifest:
        """
        Load manifest file
        :param file:
        :return:
        """
        document = yaml.load(file, Loader=yaml.FullLoader)
        return Manifest(document["intents"])

    def _build_path(self, file) -> str:
        return Path(self._data_folder) / file.name

    def read_intent(self, file) -> HumanIntent:
        with open(self._build_path(file)) as f:
            sentences = yaml.load(f, Loader=yaml.FullLoader)
            return HumanIntent(
                name=os.path.splitext(file.name)[0],
                sentences=sentences
            )

    def read_intents(self):
        intents = []
        for f in os.scandir(self._data_folder):
            intent = self.read_intent(f)
            if f.is_file() and intent.name in self._manifest.intents:
                intents.append(intent)
            else:
                del intent
        return intents


class CerebroEntity:
    """
    Data model for cerebro backend's entities.
    """
    start: int
    end: int
    name: str

    def __init__(self, start: int, end: int, name: str):
        self.start = start
        self.end = end
        self.name = name


class CerebroDataModelEntry:
    """
    Data model entry for cerebro backend's models.
    """
    text: str
    categories: List[str]
    entities: List[CerebroEntity]

    def __init__(self, text: str, categories: List[str], entities: List[CerebroEntity]):
        self.text = text
        self.categories = categories
        self.entities = entities


class CerebroDataModel(List[CerebroDataModelEntry]):
    """
    Data model for cerebro backend's models.
    """
    pass


class CerebroFactory:
    def __init__(self):
        pass

    @staticmethod
    def build_entry(name: str, sentence: str) -> CerebroDataModelEntry:
        return CerebroDataModelEntry(
            text=sentence,
            categories=[name],
            entities=[]  # TODO: Read entities from xml
        )

    @staticmethod
    def build_data_model(intents: List[HumanIntent]) -> CerebroDataModel:
        """
        Generate the Cerebro backend's model, from the intents parsed.
        :return:
        """
        model = CerebroDataModel()

        for intent in intents:
            for sentence in intent.sentences:
                model.append(CerebroFactory.build_entry(intent.name, sentence))

        return model


def main(data_folder, manifest_file, output_file):
    # Read human readable intent's files which are in the manifest.
    intent_builder = FilesReader(data_folder, manifest_file)
    intents = intent_builder.read_intents()

    # Generate the data model for the Cerebro's backend from these intents, and print it into the output file.
    data_model = CerebroFactory.build_data_model(intents)
    json.dump(data_model, output_file, default=lambda o: o.__dict__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build Cerebro model.')
    parser.add_argument('--data', metavar='DATA_FOLDER', type=str,
                        help='The data folder containing intent files in the format <INTENT_NAME>.yaml.')
    parser.add_argument('--manifest', metavar='MANIFEST_FILE', type=argparse.FileType('r'),
                        help='The manifest containing the list of intents that we want to take from data folder.')
    parser.add_argument('--output', metavar='OUTPUT_FILE', type=argparse.FileType('w'),
                        help='The json output file where the model will be placed')

    args = parser.parse_args()

    main(
        manifest_file=args.manifest,
        data_folder=args.data,
        output_file=args.output
    )
