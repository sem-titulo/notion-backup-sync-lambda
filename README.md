# notion-backup-sync-lambda
Lambda que faz backup das atividades automaticamente, buscando do notion e salvando no dynamodb

# Como Alterar?

+ Altere sempre o arquivo notion_backup_sync_lambda
+ Ao salvar, zip novamente a função <br/>
    `zip deployment-package.zip notion_backup_sync_lambda.py`<br/>
    `git add . && git commit -m"feat: new feature" && git push` 

+ Caso tenha que instalar novas bibliotecas <br/>
    `cd /packages && pip install --target ./package -r requirements.txt && zip -r ../deployment-package.zip . `

# Tarefas

- [x] Consultar tarefas no notion
- [x] Escrever tarefas no dynamodb
- [x] Automatizar deploy
- [ ] Automatizar download de blibotecas
- [ ] Automatizar zip do pacote
- [ ] Passar variaveis de ambiente 
