import os
import dotenv


class Ingestor:

    def __init__(self):
        self.file_paths = []


    def extract():
        
        pass

    def open_folder(self, folder_path: str):
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                self.file_paths.append(full_path)

        for file_path in self.file_paths:
            
        
        print(self.file_paths)
