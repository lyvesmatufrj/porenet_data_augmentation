from paraview.simple import *
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt

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

# Definir o número de slices e a direção
n_slices = 10  # Número de slices a serem criados
slice_direction = [0, 0, 1]  # Direção do corte, neste caso ao longo do eixo Z
z_min, z_max = data.GetDataInformation().GetBounds()[4:6]  # Pegando o limite no eixo Z

# Iterar sobre os slices
for i in range(n_slices):
    z_position = z_min + (z_max - z_min) * (i / n_slices)

    # Aplicar Slice
    slice_filter = Slice(Input=data)
    slice_filter.SliceType = 'Plane'
    slice_filter.SliceType.Origin = [0, 0, z_position]
    slice_filter.SliceType.Normal = slice_direction
    slice_filter.UpdatePipeline()

    # Resample to Image
    resample_filter = ResampleToImage(Input=slice_filter)
    resample_filter.SamplingDimensions = [D, D, 1]  # Apenas uma camada no eixo Z
    resample_filter.UpdatePipeline()

    # Obter dados como numpy e salvar como imagem
    voxel_data = servermanager.Fetch(resample_filter)
    data_array = voxel_data.GetPointData().GetArray(array_name)
    if not data_array:
        data_array = voxel_data.GetPointData().GetArray(0)


    # Converter o array de ParaView para um array NumPy de números
    numpy_array = np.array([data_array.GetValue(j) for j in range(data_array.GetNumberOfTuples())])
    numpy_image = numpy_array.reshape((D, D))

    print(numpy_array)

    # # Salvar como PNG sem binarização
    # output_path = output_dir / f"slice_{i:03d}.png"
    # plt.imsave(str(output_path), numpy_image, cmap='gray')
    # print(f"Slice {i+1} salvo em {output_path}")

    

# Finalizar visualização
Hide(data)
