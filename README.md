# **LOG REDO/UNDO**

Universidade Federal da Fronteira Sul - Campus Chapecó

Ciência da Computação - Banco de Dados II – 2023.1

Prof. Guilherme Dal Bianco

Acadêmico: **João Bussolotto**


---


## **Mecanismo de Log Undo/Redo**




---


Objetivo: implementar o mecanismo de log Redo/Undo sem checkpoint usando o SGBD 
<br>
*Funcionamento:* 
O código, que poderá utilizar qualquer linguagem de programação, deverá ser capaz de ler o arquivo de log (entradaLog) e o arquivo de Metadado e validar as informações no banco de dados através do modelo REDO/UNDO. <br>
O código receberá como entrada o arquivo de metadados (dados salvos) e os dados da tabela que irá operar no banco de dados. 









## 📋 **Descrição:**

Dado um *Arquivo de Metadados (json)*, como:
```javascript
{  
    "INITIAL": {
        "A": [20,20],
        "B": [55,30]
    }
}
```

O programa deve ser capaz de criar e preencher uma *tabela do banco de dados* como segue:

|  ID  |  A  |  B  |
|------|-----|-----|
|  01  |  20 |  55 |
|  02  |  20 |  30 |


Após isso, o programa deve ler o *arquivo de log* que segue o formato:

><transação, “id da tupla”, ”coluna”, “valor antigo”, “valor novo”>.

```html
<start T1>
<T1,1, A,20,500>
<start T2>
<commit T1>
<T2,2, B,20,50>
	<start T3>
<start T4>
<commit T2>
<T4,1, B,55,100>

```
