## Intsruction

Instruction to push code to different repository. (Required for hosting and personel contribution)

Clone the main repository from the link 

```bash
git clone git@github.com:UICDBTeaching/cs480-s25-group-09.git
cd cs480-s25-group-09
```

Add 2 new remote respositories 

```bash
# Frontend remote
git remote add frontend git@github.com:ExperimenterX/CoffeHouse-WebApp.git

# Backend remote
git remote add backend git@github.com:ExperimenterX/CoffeHouse-web.git
```

Push frontend and backend to it's own repo.

```bash
git subtree push --prefix=frontend frontend develop
git subtree push --prefix=backend backend develop
```

branch name 'develop' is a required field for subtree push. Change branch name according to development if needed.

Perform normal push to origin remote.
```bash
git push origin
```

Please follow the command steps as mentioned. 