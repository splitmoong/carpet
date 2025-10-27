import os

from embedding.embedder import Embedder


class Ingestor:

    def __init__(self):
        self.file_paths = []
        self.embedder = Embedder()

    def extract(self):

        pass

    def open_folder(self, folder_path: str):

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                self.file_paths.append(full_path)

        for file_path in self.file_paths:
            self.embedder.embed(file_path)
            pass

        print(self.file_paths)
