# 1. Contribution Policies

## 2. Issues Policy
If you find a bug or have any suggestions for improving the software, you can create an issue by following the steps below:

1. Choose the type of issue to be created (functionality or bug fix)
2. Write a short title for the issue
3. Fill in the description of the issue following the steps and guidelines of the template that will be shown
4. Fill in additional information if you have it (epic, milestone, etc.)

Both the title and the description of the issue must be written in English and follow its rules of syntax and semantics.

## 3. Branches Policy

### 3.1 Gitflow
Git Flow will be treated as shown in the [image](https://fga-eps-mds.github.io/2020.1-stay-safe-docs/images/gcs/GitFlowDevelopment.png). For a change to reach the master branch (stable branch) the steps below are followed:

1. Every new branch must be made from develop
2. When resolving the proposed issue the new branch should be merged and compared in relation to develop
3. If the PR is approved by the team, the work branch will be deleted and its content integrated to develop
4. The develop will test the integration between recently added features
5. When the team certifies the stability of develop, its content is integrated into the master

### 3.2 Nomenclature Rules
Every new branch created in the Stay Safe repositories must propose to solve a specific issue, the name of the branch must follow the following rules:

1. Contain the issue code provided by GitHub
2. Be short and expressive about the issue to be addressed
3. Words must be separated by an underscore "-"
4. Be written in "lower case"

Example:

    2-crud-user

## 4. Commits Policy
Commits must be atomic (a small contribution to solving a specific problem). The commit message must report what has been done succinctly and directly, in addition, it must be in English, start with a verb and with the first letter capitalized.

Contributions made by more than one person must contain the command "Co-authored-by" to identify all authors involved.

Example contribution made by an author:

    git commit -m "Create user model."

Example of contribution made by more than one author:

    git commit -m "Create user model.

    Co-authored-by: Person <emailgit@email.com>"


## 5. Pull Request Policy
To perform a Pull Request (PR) for the repository it is necessary to follow the steps below.

1. When solving an issue, upload your contributions and create a Pull Request
2. Write a succinct title for the PR
3. Fill in the description of the PR following the steps and guidelines of the template that will be shown
4. Connect the PR with the issue it solves
5. Fill in additional information if you have it (assigns, reviewers, etc.)

For a Pull Request to be approved, the contribution made must:

1. Solve only the specific issue to which you are entitled to deal
2. Respect all acceptance criteria defined in the issue
3. Be described in the English language
4. Have test coverage
5. Pass the continuous integration and the tools it executes
6. Contain effective logic to preserve application performance
7. Contain good programming practices to preserve the quality of the code
8. Do not add any unexpected behavior to the application
