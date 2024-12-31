from settings import *

def import_image(*path, format = "png" , alpha = True):
    full_path = join(*path) + f".{format}"
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _ , file_names in walk(join(*path)):
        for file_name in file_names:

            full_path = join(folder_path, file_name)
            key = file_name.split(".")[0]
            audio_dict[key] = pygame.mixer.Sound(full_path)
            
    return audio_dict


def import_folder(*path):
    frames = []
    for folder_path, _ , file_names in walk(join(*path)):
        for file_name in sorted(file_names, key=lambda file: int(file.split(".")[0])):
            full_path = folder_path + f"\{file_name}"

            frames.append(pygame.image.load(full_path))
    
    return frames