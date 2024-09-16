from paraview.simple import *
import os
from pathlib import Path
from PIL import Image

ResetSession()

# Parâmetros
base_path = Path(__file__).parent.parent.parent  # Caminho base do repositório
vtk_file_path = base_path / 'data' / 'vtk' / 'polyhedra_output_-polyhedra-00000000.vtk'
output_dir = base_path / 'data' / 'slices'
D = 100  # Resolução da grade voxelizada
array_name = "Solid"  # Nome do array para ser exportado

# Criar diretório de saída se não existir
output_dir.mkdir(parents=True, exist_ok=True)

# Carregar dados
data = OpenDataFile(str(vtk_file_path))  # Convertendo Pathlib para string
Show(data)
Render()

# Ocultar a visualização das pedras (o objeto original)
Hide(data)

# Definir o número de slices e a direção
n_slices = 10  # Número de slices a serem criados
slice_direction = [0, 0, 1]  # Direção do corte, neste caso ao longo do eixo Z
z_min, z_max = data.GetDataInformation().GetBounds()[4:6]  # Pegando o limite no eixo Z

# Iterar sobre os slices
previous_slice = None  # Para armazenar o slice anterior e remover
for i in range(n_slices):
    z_position = z_min + (z_max - z_min) * (i / n_slices)

    # Remover o slice anterior se houver
    if previous_slice:
        Delete(previous_slice)
        Render()

    # Aplicar novo Slice
    slice_filter = Slice(Input=data)
    slice_filter.SliceType = 'Plane'
    slice_filter.SliceType.Origin = [0, 0, z_position]
    slice_filter.SliceType.Normal = slice_direction
    slice_filter.UpdatePipeline()

    # Resample to Image
    resample_filter = ResampleToImage(Input=slice_filter)
    resample_filter.SamplingDimensions = [D, D, 1]  # Apenas uma camada no eixo Z
    resample_filter.UpdatePipeline()

    # Exibir apenas o novo slice
    #Show(resample_filter)
    Render()

    # Ajustar a câmera para focar no slice atual (fazer o zoom)
    view = GetActiveView()
    view.CameraFocalPoint = [0, 0, z_position]
    view.CameraPosition = [0, 0, z_position + 10]  # Ajusta a posição da câmera para mais próximo
    view.CameraViewUp = [0, 1, 0]  # Direção para cima
    view.ResetCamera()
    Render()

    # Salvar a captura de tela completa
    screenshot_path = output_dir / f"slice_full_{i:03d}.png"
    SaveScreenshot(str(screenshot_path))  # Salva a captura de tela da visualização completa

    # Abrir a imagem salva e recortar com base nas dimensões do ResampleToImage
    with Image.open(screenshot_path) as img:
        # Definindo os limites para o recorte
        left = 100  # Ajuste de acordo com a necessidade
        top = 100   # Ajuste de acordo com a necessidade
        right = left + D  # Usando as dimensões D fornecidas no ResampleToImage
        bottom = top + D

        # Realizando o recorte
        cropped_img = img.crop((left, top, right, bottom))

        # Salvando a imagem recortada
        cropped_img_path = output_dir / f"slice_{i:03d}_cropped.png"
        cropped_img.save(cropped_img_path)
        print(f"Imagem recortada do Slice {i+1} salva em {cropped_img_path}")

    # Armazenar o slice atual para remover no próximo loop
    previous_slice = slice_filter

# Finalizar visualização
Hide(data)
