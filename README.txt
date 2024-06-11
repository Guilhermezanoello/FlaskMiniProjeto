ANTES DE TUDO COMEÇAR!!!

1.Realize o download de todos os ficheiros!

2.Praparação do Script.ps1 para vosso Habiente:

    Alterar a variavél, com o conteúdo do caminho onde salvares a pasta images:

    $caminhoImagens="C:/Users/guilh/Desktop/images" # Troque aqui pelo seu caminho

 2.1.Configuração GitHub;
    Nota: - Caso pretenda utilizar esta aplicação web, terá de fazer a alteração dos respetivos nomes das funcionalidades
	  - Alterar o URL de acesso do repositório do GitHub (Credenciais de autenticação) 


    Salve o Script.ps1 com suas respetivas altrerações e pode correr dentro do PowerShell com o comando .\Script.ps1

3.Vá até o seu portal da AZURE em sua base de dados Cosmo DB e copie a PRIMARY KEY que é a chave do seu ENDPOINT.

    Substitua a KEY no FlaskMiniProjeto nos ficheiro app.py e quiz.py respetivas com a sua PRIMARY KEY.

    Substitua a KEY no FinalizeQuizFunction no ficheiro function_app.py com a sua PRIMARY KEY.

4.Abra pasta FinalizeQuizFunction utilize o Visual Studio Code, instale a extensão Azure Tools(instale todas)
    Acesse a barra lateral com o Icone do Azure deves realizar o login dentro da extensão.
    Localize no Workspace o seu Local Project e realize o Deploy
