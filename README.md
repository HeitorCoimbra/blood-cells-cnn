
# Web app de classificador CNN
## Aplicação web feita em Flask para teste de funcionalidade de CNN para classificação de células sanguíneas

### Instalação
Utilizando o pip em qualquer uma das duas pastas principais (cada projeto tem requirementes diferentes, a webapp, ou o notebook de treinamento da rede):

```pip install -r requirements.txt``` 

### Utilização
Para rodar a aplicação web basta rodar o código do arquivo deploy.py na pasta flask-app:

```
cd flask_app
python deploy.py
```

A aplicação estará localizada em localhost:5000, onde pode ser feito o upload de uma imagem e retornará a tabela de probabilidades de classificação.

Dentro da pasta "valid" há uma série de imagens que pertencem à seção de teste do [dataset utilizado](https://www.kaggle.com/paultimothymooney/blood-cells) para treinamento da rede.

### Arquitetura da rede
A rede é uma simples rede neural convolucional com duas camadas de convoluções 3x3 e duas camadas lineares, sendo uma a camada de saída softmax. Para o input, as imagens de entrada sofrem um resize para o tamanho (80x60) para reduzir a quantidade de parâmetros. 

```
model = Sequential()
model.add(Conv2D(32, (3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss=categorical_crossentropy,
              optimizer=Adam(),
              metrics=['accuracy']) 
```

Além disso, uma camada de Dropout segue a ultima camada convolucional, e mais uma segue a primeira camada linear de modo a regularizar a rede e mitigar efeitos de overfitting na base de treino.

Por fim, a loss utilizada foi a entropia cruzada categórica e o backpropagation e otimização foram feitos com o algoritmo Adam, ambos métodos considerados consistentes no estado da arte de deep learning.

### Treinamento da rede
A rede foi treinada em uma [base de dados](https://www.kaggle.com/paultimothymooney/blood-cells) de imagens 640x480 de celulas sanguíneas pertencentes a uma de quatro categorias: Monócitos, Neutrófilos, Linfócitos e Eosinófilos. A diferença visual principal entre essas categorias é a fisiologia do núcleo da célula, que varia em quantidade e formato.

A base oferece dois conjuntos de dados, um é o conjunto de fotos de microscopia reais, e o segundo é um conjunto que passou por data augmentation, ou seja, transformações sutis nas imagens originais de modo a mitigar o desequilíbrio de classes e aumentar a base total de fotos. O conjunto que foi utilizado no projeto foi o de imagens aumentadas, de modo a aumentar a robustez do modelo e regularizar os resultados.

A acurácia final alcançada foi de 83.2% e outras métricas de avaliação foram:

|| Precisão  | Recall | F1-Score |
|---|-------|------|------|
|Neutrófilos| 0.64  | 0.77 | 0.70 |
|Eosinófilos| 0.72  | 0.74 | 0.73 |
|Monócitos| 0.96  | 0.76 | 0.85 |
|Linfócitos| 0.97  | 0.95 | 0.96 |

Alguns gráficos dos resultados e do treinamento:

![Imgur](https://i.imgur.com/VDngu5B.png)

![Imgur](https://i.imgur.com/oFTwSgI.png)
