# Porenet Data Augmentation

Este repositório contém o pipeline completo para gerar e processar meios porosos simulados, visando o aumento de dados (*data augmentation*) para utilização na rede neural **Porenet**. O projeto integra simulações de meios porosos geradas no YADE, processa cortes (slices) utilizando o ParaView e, em seguida, utiliza o OpenCV para produzir versões binarizadas dos meios porosos, que são submetidos a técnicas de aumento de dados.

## Estrutura do Repositório

- **data/**
  - `vtk/`: Contém os arquivos de simulação em formato `.vtk` gerados pelo YADE.
  - `slices/`: Slices exportados do ParaView em formato de imagem.
  - `binarized/`: Imagens binarizadas dos slices, prontas para serem utilizadas no *data augmentation*.
  
- **scripts/**
  - `preprocess/`: Scripts Python para leitura dos arquivos `.vtk` e exportação de slices no ParaView.
  - `binarization/`: Scripts para binarização dos slices utilizando OpenCV.
  - `augmentation/`: Scripts de aumento de dados aplicados às imagens binarizadas.

- **notebooks/**: Notebooks Jupyter para visualização e testes de processamento.
  
- **logs/**: Contém logs de execução e registros importantes do processo.

- **results/**
  - `final_slices/`: Slices finais, aumentados e binarizados, prontos para treinamento na Porenet.

## Fluxo de Trabalho

1. **Simulações no YADE**: Geração de simulações de meios porosos em formato `.vtk`.
2. **Slices no ParaView**: Importação e aplicação de cortes nas simulações para exportação das imagens.
3. **Processamento com OpenCV**: Binarização das imagens exportadas para preparar os meios porosos.
4. **Data Augmentation**: Aumento de dados com técnicas como rotação, translação e variações geométricas.
5. **Integração com Porenet**: As imagens processadas são usadas para treinar e validar a rede neural Porenet.

## Requisitos

- **YADE**: Para simular os meios porosos.
- **ParaView**: Para visualizar e exportar os cortes das simulações.
- **Python 3.x**: Para o processamento de imagens e aumento de dados.
  - **OpenCV**: Biblioteca usada para a binarização das imagens.
  - **NumPy**: Manipulação de arrays de dados.
  - **Matplotlib** (opcional): Para visualização dos dados.

## Como Usar

1. Realize as simulações no YADE e exporte os arquivos `.vtk`.
2. Utilize o ParaView para gerar slices e salve-os na pasta `data/slices/`.
3. Execute os scripts de binarização no diretório `scripts/binarization/` para processar os slices.
4. Use os scripts de *data augmentation* para expandir o conjunto de dados.
5. As imagens processadas estarão prontas para serem utilizadas no treinamento da Porenet.
