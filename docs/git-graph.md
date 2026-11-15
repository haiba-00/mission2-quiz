# 실제 Git 그래프

```text
> git log --oneline --graph --all
* 710ad26 Docs: verify change from cloned checkout
* f4549d9 Docs: explain setup JSON schema design validation and Python fundamentals
* b0ebdba Test: cover CLI persistence invalid input recovery and safe interruption
* 69a5153 Fix: save complete state and exit cleanly on EOF or Ctrl+C
* d1887dd Feat: track percentage best score and distinguish unplayed state
* 4a495ab Feat: display registered quiz list and handle empty collection
* 77b536e Feat: register validated questions and immediately persist additions
* ce70d7b Feat: load and atomically save UTF-8 root state with recovery
*   7f0503d Merge: integrate quiz play feature into main
|\  
| * dc70708 Feat: implement complete quiz round on feature branch
|/  
* 0c0b5cc Refactor: separate QuizGame state and menu responsibilities
* d052d04 Feat: author five developer tools and Python quizzes
* 9efd7ba Feat: model Quiz with four choices and answer validation
* 3b16900 Feat: implement validated console menu and exit flow
* b0e54a4 Feat: validate numeric ranges and nonempty text input
* e9f8b07 Chore: initialize isolated mission2 quiz repository

> git rev-list --count main
16
```
