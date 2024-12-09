Agenda::
1. Create a Github repo
2. open anaconda promt: Go to folder path : type "code ."
3. Open terminal in vscode :: create a venv
    conda create -p venv python==3.8 -y
4. 
# To activate this environment, use                                                                                                                                                                                               
#                                                                                                                                                                                                                                 
#     $ conda activate C:\Pum\ML_AI\Udemy\ML_course\Complete-Data-Science-With-Machine-Learning-And-NLP-2024-main\24_EndToEnd_ML_with_Deployment_by_Pum\venv                                                                      
#
# To deactivate an active environment, use
#
#     $ conda deactivate    
5. Create a readme.md file
6. Now initialize the Github
    echo "# machine_learning_pro" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    ## If github is not logged in login first using:: git config --global user.email "you@example.com"
    git branch -M main
    git remote add origin https://github.com/Pum-Pum-Pum-Pum/machine_learning_pro.git
    git push -u origin main
7. Check if the file added to github    