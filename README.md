# Emissão de etiquetas de expedição<br/>

## Objetivo:<br/>
Imprimir as etiquetas de expedição consultando Tiny e Intelipost a partir do número da nota fiscal ou número do pedido de venda.<br/>
<br/>

## Arquitetura<br/>
* Python<br/>
* API Miliapp<br/>
* API Tiny V2<br/>
* API Intelipost<br/>
* Excutavel pelo auto-py-to-exe<br/>
<br/>

## Execução do código<br/>
Pelo executável gerado pelo auto-py-to-exe irá abrir uma janela.<br/>
No primeiro campo deve ser selecionado será será inserido um número de pedido ou número de nota fiscal. No segundo campo insira o número e pressione ENTER.<br/>
O programa irá buscar na intelipost a etiqueta e, no caso de motoboy ou ativmob, será criado uma etiqueta com as informações necessárias para esses serviços.<br/>
<br/>
TOKEN_TINY=1aaf26f20d2bb631d7bea7323d2dbf77058b65f3b6fa0ec2ea104c1cb3ea8273
