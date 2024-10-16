import os
import zipfile

def create_zip(paths, zip_filename, compression_level=9):
  with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zip_file:
    for path, pathInZip in paths:
      zip_file.write(path, pathInZip)

os.chdir(os.path.dirname(__file__))

paths = (
  ("PMY.py", None),
  ("packToZip.py", None),
  ("modules/myGL.py", None),
  ("modules/myGLclasses.py", None),
  ("modules/rbxmReader.py", None),
  ("modules/rbxmMeshReader.py", None),
  ("modules/rbxmLoader.py", None),
  ("resources/textures.png", None),
  ("resources/avatar.rbxm", None),
  ("resources/skybox_labeled.png", None),
  ("resources/skybox_space.webp", None),

  ("EulerRotators.py", None),
)

zip_filename = "PMY_name.zip"
create_zip(paths, zip_filename, compression_level=9)
print(f"Архив {zip_filename} успешно создан! ;'-}}")
