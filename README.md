# Aplicação de Envoltrória Convexa

Em um espaço euclidiano, uma região convexa é uma região onde, para cada par de pontos dentro da região, cada ponto no segmento de reta que une o par também está dentro da região. De forma geral, em geometria convexa, um conjunto convexo é um subconjunto de um espaço afim que é fechado sob combinações convexas.
O limite de um conjunto convexo é sempre uma curva convexa. A interseção de todos os conjuntos convexos contendo um determinado subconjunto A do espaço euclidiano é chamada de invólucro convexo ou envoltória convexa de A. Assim, a Envoltória Convexa é o menor conjunto convexo contendo A.

## Dependências

* **numpy 1.16.3**
* **opencv-python 4.1**
* **scikit-learn 0.22.2**



## Definição da Envoltória Convexa

A ideia básica é definir um imagem limiar de uma mão (e as informações externas de contorno). Usando um pouco de matemática, é possível calcular o centro da mão em relação ao ângulo dos pontos externos para inferir a contagem de dedos. A definição da Envoltória Convexa será realizada pela função **cv2.convexHull()**
Você pode encontrar mais informações sobre esta função na documentação do opencv disponível [aqui](https://docs.opencv.org/2.4/doc/tutorials/imgproc/shapedescriptors/hull/hull.html)

## Artigo medium

Além das referências, elaborei um artigo no medium.

[Segmentação com Envoltória Convexa e OpenCV](https://medium.com/@toni_esteves/segmenta%C3%A7%C3%A3o-com-envolt%C3%B3ria-convexa-e-opencv-118ef7138238)


![alt text](https://cdn-images-1.medium.com/max/720/1*l6f1ASymT-1uET0CK1oUQA.gif)


## Referências

* https://books.google.com.br/books/about/Finite_Mathematics.html?id=EwhQCgAAQBAJ&redir_esc=y

* https://books.google.com.br/books/about/Linear_Programming_Duality.html?id=w10OBwAAQBAJ&redir_esc=y

* https://medium.com/r/?url=https%3A%2F%2Fwww.semanticscholar.org%2Fpaper%2FVisualizing-Eye-Tracking-Convex-Hull-Areas%253A-A-Pilot-Sears-Alruwaythi%2F1fd1f735e9a8f27892268a6fd219bc5e39d66758

* https://en.wikipedia.org/wiki/Convex_hull

* https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/

* https://www.sciencedirect.com/topics/computer-science/convex-hull