# Getting Started
- Install Git (you probably have already)

- You will likely have to setup Git with your GitHub account, you can do that using a "Personal Access Token".

    🛑 Make sure that you have access to the repo, the repo is private, you need to be added by email!
- To get the code on your machine, you can clone either through Visual Studio Code (VSC): ``` File > New Window > Clone from Git```, or use the terminal:
    ```
    git clone git@github.com:kacikgoez/ProcessDiscovery.git
    ```
    or

    ```
    git clone https://github.com/kacikgoez/ProcessDiscovery.git
    ```

# Branches

- If you want to make changes, you can either create your own feature branch or edit someone elses. Most of the time,
you will create your own branch. To do that, you will have to follow the naming convention. You will need the Trello ticket ID (every ticket contains one) to create a branch for that specific issue / ticket. If you want to make a minor change that is not part of a ticket, like a small bug fix, you can set the ID to "MYBUGFIX" or anything else, the fake ID just needs to be 8 characters long, otherwise it will not be accepted and not pass the tests.

    - 🟡 **Syntax**: ```{"feature" or "fix"}/ID-{trello-id}-{whatever you want}```

    - 🟡 **Examples**: ```feature/ID-44da314b-hello-world, fix/ID-51a3319b-something-that-makes-sense```

- To create a feature branch, use the ```checkout``` command. This will create a branch and switch directly into the new branch.

        git checkout -b {name of new branch that follow the convention above}

- To switch between branches, use the above command without "-b".

        git checkout {name of branch}

- To list the existing branches on your machine, run the command below. The green one is your active branch that you are currently in.

        git branch

# Adding changes

## Commits

🟡 For commits, I recommend using VSC. You should open a terminal as well (```Terminal > New Terminal```)

You can now write some code, add files and delete them. Make sure before you commit your changes, you are in the right feature branch. Now to add the changes to your local repository.

On the far left bar, VSC has ```Source Control```, it shows the changes you made and it allows you to commit the changes. Write a message of what you did, and commit your changes uisng VSC's UI tool. 

🛑 The changes are so far only locally saved, do not push the changes yet!

## Rebasing & Pushing
- Before you push a change to the remote feature branch, you should ```rebase``` your branch. To do this, you need to get the most recent version of the ```main``` branch. 

```
git checkout main
git pull
git checkout {your feature branch name}
```

- Now that you have the most recent version, you can do an interactive rebase using:

```
git rebase -i origin/main
```

- After you run `git rebase -i origin/main`, it will open up an editor in your terminal.

<<<<<<< HEAD
<<<<<<< HEAD
 🟡 On my machine (Mac), the editor is set to `Vim` by default, which is a more "difficult" editor with different modes. You can setup to VSC for a visual editor: ```git config --global core.editor code```. For this you might need to install the "code" command, to do this, press ```Ctrl+Shift+P```, which opens the command palette, and type "install code", click on the option "Shell Command: Install ..." that appears.
=======
 🟡 On my machine (Mac), the editor is set to `Vim` by default, which is a more "difficult" editor with different modes. You can setup to VSC for a visual editor: ```git config --global core.editor code```
>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
 🟡 On my machine (Mac), the editor is set to `Vim` by default, which is a more "difficult" editor with different modes. You can setup to VSC for a visual editor: ```git config --global core.editor code```. For this you might need to install the "code" command, to do this, press ```Ctrl+Shift+P```, which opens the command palette, and type "install code", click on the option "Shell Command: Install ..." that appears.
>>>>>>> 7e18e45 (Feature: ID-hGqw1FNt: add dashboard customization)

- The editor in the terminal will list all the commits that you have locally different from the main branch. You can now `drop`, `reword` and `squash` (and do a bunch other stuff) by changing the word `pick` to one of the commands listed.

- After you save the file, depending on the commands you used, it will reopen another file in your terminal editor and will ask you to do some changes (like changing or picking the commit message).
 
🛑 Unless you are working on the branch with someone else, make sure the list only contains your own commits! It can happen that someone deleted an old commit from `main`, but it is still present in your local feature branch, which would push the old deleted commit again! Use `drop` on the commits of others listed there.

- Now that you have done the ```rebase```, you can push the changes through. Make sure you force push:
```
git push -f
```


# Merging

If you are finished & happy with the changes, you can create a go to your feature branch and create a `Pull Request` on Github.com to add your new changes to the main branch. 
