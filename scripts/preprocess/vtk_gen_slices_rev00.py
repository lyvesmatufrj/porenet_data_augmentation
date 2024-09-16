import vtk
import numpy as np
import os 
from pathlib import Path
import vtkmodules

def load_vtk_file(file_path):
    # Leitura do arquivo VTK
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()

    return reader.GetOutput()

def apply_slice(vtk_data, slice_position):
    # Filtro para aplicar o slice
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(vtk_data)
    reslice.SetOutputDimensionality(2)
    
    # Definir a posição do slice (por exemplo, no eixo Z)
    matrix = vtk.vtkMatrix4x4()
    matrix.Identity()
    matrix.SetElement(2, 3, slice_position)  # Mover o plano do slice para a posição desejada no eixo Z
    reslice.SetResliceAxes(matrix)
    
    reslice.Update()

    return reslice.GetOutput()

def vtk_to_numpy(vtk_data):
    # Converte o resultado do slice VTK para numpy array
    dims = vtk_data.GetDimensions()
    vtk_array = vtk_data.GetPointData().GetScalars()
    numpy_array = vtkmodules.util.numpy_support.vtk_to_numpy(vtk_array)
    
    return numpy_array.reshape(dims[1], dims[0])  # Reshape de acordo com as dimensões do slice

def save_numpy_array(array, file_path):
    # Salvar o array numpy em arquivo para uso posterior
    np.save(file_path, array)

if __name__ == "__main__":

    # Parâmetros
    base_path = Path(__file__).parent.parent.parent  # Caminho base do repositório
    file_path = base_path / 'data' / 'vtk' / 'polyhedra_output_-polyhedra-00000000.vtk'

    # Exemplo de uso
    slice_position = 50  # Definir a posição do slice no eixo Z
    output_array_path = base_path / 'data' / 'slices'

    # Carregar o arquivo VTK
    vtk_data = load_vtk_file(file_path)

    # Aplicar o slice
    slice_data = apply_slice(vtk_data, slice_position)

    # Converter para numpy
    slice_array = vtk_to_numpy(slice_data)

    # Salvar o array numpy
    save_numpy_array(slice_array, output_array_path)

    print(f"Array salvo em {output_array_path}")