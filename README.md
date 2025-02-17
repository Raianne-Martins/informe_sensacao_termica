# Tá frio ou tá calor?

Essa aplicação tem como o intuito auxiliar o usuário, ao sair para diferentes locais a se preparem para as condições climáticas das cidades que frequentam. 
O usuário que deseja usar, basta atualizar as cidades que deseja juntamento com os dados geográficos no arquivo cities.py.
Ao inves de temperatura (ºC) a aplicação informa a sensação térmica, que está relacionada com temperatura (ºC) e umidade relativa do ar (%). A conversão da API Open-Meteo (que informa a temperatura em Fahrenheit - ºF) está no arquivo app.py.

# Informações
Ao acessar a aplicação, basta selecionar a cidade que deseja a informação. O card com as informações irá aparecer na página, para melhor visualização o background muda de cor dependendo da sensação térmica. `bg-cold` é aplicado quando a sensação térmica é de menos de 15 ºC, `bg-comfortable`  é aplicado quando a sensação térmica é maior de 15ºc e menor que 24ºC, por sua vez `bg-warm` é aplicado quando a sensação térmica é maior que 25ºC e menor que 29ºC e por fim, `bg-hot` é aplicado quando a sensação térmica é maior que 30ºC.

# Modelagem de dados

# Código- Fonte

Este projeto é um *WIP*