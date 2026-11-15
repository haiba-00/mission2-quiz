# 실제 clone / push / pull 실습
```text
> git clone https://github.com/haiba-00/mission2-quiz.git mission2-clone
Cloning into '<CLONE_DIRECTORY>'...
> git add README.md
> git commit -m "Docs: verify change from cloned checkout"
[main 710ad26] Docs: verify change from cloned checkout
 1 file changed, 2 insertions(+)
> git push
To https://github.com/haiba-00/mission2-quiz.git
   f4549d9..710ad26  main -> main
> git pull --ff-only
From https://github.com/haiba-00/mission2-quiz
   f4549d9..710ad26  main       -> origin/main
Updating f4549d9..710ad26
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
> README clone verification line
복제·동기화 실습: 별도 clone 작업 폴더에서 이 문장을 추가하고 원본에서 pull로 반영했다.
```
