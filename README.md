# Tá frio ou tá calor?

Essa aplicação tem como o intuito auxiliar o usuário, ao sair para diferentes locais a se preparem para as condições climáticas das cidades que frequentam. 
O usuário que deseja usar, basta atualizar as cidades que deseja juntamento com os dados geográficos no arquivo cities.py.
Ao inves de temperatura (ºC) a aplicação informa a sensação térmica, que está relacionada com temperatura (ºC) e umidade relativa do ar (%). A conversão da API Open-Meteo (que informa a temperatura em Fahrenheit - ºF) está no arquivo app.py.

# Informações
Ao acessar a aplicação, basta selecionar a cidade que deseja a informação. O card com as informações irá aparecer na página, para melhor visualização o background muda de cor dependendo da sensação térmica. `bg-cold` é aplicado quando a sensação térmica é de menos de 15 ºC, `bg-comfortable`  é aplicado quando a sensação térmica é maior de 15ºc e menor que 24ºC, por sua vez `bg-warm` é aplicado quando a sensação térmica é maior que 25ºC e menor que 29ºC e por fim, `bg-hot` é aplicado quando a sensação térmica é maior que 30ºC.

# Modelagem de dados

![informe_clima_1](https://github.com/user-attachments/assets/2f0a5a2d-66d1-4df8-8e57-04ef7816f88b)

# Como utilizar

1. Clone o repositório:

```bash

git clone https://github.com/Raianne-Martins/informe_sensacao_termica.git
```

2. Acesse a pasta do arquivo:

```bash

cd src
```

3. Crie um ambiente virtual na pasta do projeto :

```bash
python -m venv venv
```

 Para ativar no Windows <br>
```bash
venv\Scripts\activate
```

Para ativar no MacOS e Linux <br>
```bash
source venv/bin/activate
```

4. Instale o Flask:
```bash
pip install flask
```

5. Instalar as dependências:
```bash
pip install -r requirements.txt
```

6. Rode o flask:
```bash
flask run
```

Após terminar de usar a aplicação, desative o ambiente. <br>

7. Desativar o venv:
   
```bash
deactivate
```
# Código- Fonte

<li><a href="README.md"> Código Fonte</a></li>

<li>Este projeto é um WIP </li>
