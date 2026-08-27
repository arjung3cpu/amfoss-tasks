# Task 01 – Git Exercises

## About the Task

For this task, I completed all 23 Git exercises from Git Exercises. The exercises covered basic Git operations as well as more advanced topics such as branching, merging, rebasing, stashing, and editing Git history.

The main thing I learned from this task was that Git is not just about `add`, `commit`, and `push`. A lot of the exercises required me to understand what was happening to the working directory, staging area, branches, and commit history.

## Completion Proof

I completed all 23 exercises successfully.

The screenshot of the final completion page is included in this folder.

## What I Did in Each Exercise

### 1. Push a Commit

I initialized the exercise using:

```bash
git start master
```

I used `git verify` to check whether the exercise was completed correctly and pushed the required commit.

This helped me understand the basic workflow of creating and pushing commits.

### 2. Commit One File

```bash
git add A.txt
git commit -m "Commit A.txt file"
```

Both `A.txt` and `B.txt` were present, but I only wanted `A.txt` in the commit. I used `git add A.txt` so that only that file was staged before committing it.

### 3. Commit One File of Two Already Staged

```bash
git reset A.txt
git commit -m "Commit B.txt file"
```

This time both files were already staged. I used `git reset A.txt` to remove `A.txt` from the staging area, leaving only `B.txt` to be committed.

### 4. Ignore Unwanted Files

I worked with `.gitignore` to prevent unwanted files such as `.exe`, `.o`, `.jar`, and the `libraries` directory from being tracked.

This showed me how useful `.gitignore` is for keeping generated files and unnecessary files out of a repository.

### 5. Chase Branch That Escaped

I moved `chase-branch` to the same commit as the `escaped` branch using Git branch/merge operations.

The important concept here was a **fast-forward merge**, where Git can simply move the branch pointer forward without creating an extra merge commit.

### 6. Resolve a Merge Conflict

```bash
git merge another-piece-of-work
git add equation.txt
git commit --no-edit
```

The two branches had conflicting changes, so I had to resolve the conflict manually and then stage and commit the corrected file.

This was one of the exercises that helped me understand what actually happens during a merge conflict.

### 7. Save Your Work

```bash
git stash
git commit -am "Fix a bug"
git stash pop
```

I used `git stash` to temporarily put my unfinished work aside so that I could fix and commit another change first. After that, `git stash pop` restored my original work.

This helped me understand when stashing is useful in a real development workflow.

### 8. Change Branch History

```bash
git rebase hot-bugfix
```

I used rebase to move the branch history onto the required base and keep the commit history in the expected form.

### 9. Remove an Ignored File

```bash
git rm ignored.txt
git commit -am "Remove the file that should have been ignored"
```

The file had already been tracked before it was added to `.gitignore`, so Git continued tracking it. I used `git rm` to remove it from the repository.

### 10. Change Filename Case

```bash
git mv File.txt file.txt
git commit -am "Lowercase file.txt"
```

I used `git mv` to make Git recognize the filename case change, especially since case handling can behave differently on different operating systems.

### 11. Fix a Typo in the Last Commit

```bash
git commit -a --amend
```

I used `--amend` to modify the most recent commit instead of creating another unnecessary commit.

This showed me how Git can be used to clean up the latest commit before sharing it.

### 12. Change the Commit Date

```bash
git commit --amend --no-edit --date="1987-08-03"
```

I amended the last commit and changed its commit date to the required historical date.

### 13. Fix a Typo in an Older Commit

```bash
git rebase -i HEAD^^
git add file.txt
git rebase --continue
```

Since the problem was in an older commit, `git commit --amend` alone was not enough. I used interactive rebase to go back to that commit, fix it, and continue the history.

### 14. Find a Lost Commit

```bash
git reflog
git reset --hard HEAD@{1}
```

I used `git reflog` to find an earlier state of the repository that was no longer visible in the normal history. I then reset the branch to the required state.

This was one of the most interesting exercises because it showed me that Git often keeps a record of changes even when a commit seems to have disappeared.

### 15. Split the Last Commit

```bash
git reset HEAD^
git add first.txt
git commit -m "First.txt"
git add second.txt
git commit -m "Second.txt"
```

The original commit contained two files, but they were supposed to be separate commits. I reset the commit while keeping the changes and then created two new commits.

### 16. Too Many Commits

```bash
git rebase -i HEAD^^
```

I used interactive rebase to combine multiple small commits into one cleaner commit using the `squash`/`fixup` option.

### 17. Make a File Executable

```bash
git update-index --chmod=+x script.sh
```

This changed the executable permission stored by Git for the shell script.

I learned that Git can track file permission changes, not just file contents.

### 18. Commit Only Part of a File

```bash
git add -p file.txt
```

I used partial staging to select only certain changes from the file for the first commit. The remaining changes were committed separately.

This was useful for understanding how Git can separate different pieces of work even when they are in the same file.

### 19. Pick Specific Features

```bash
git cherry-pick feature-a
git cherry-pick feature-b
git cherry-pick feature-c
```

I used `git cherry-pick` to bring specific commits from different branches into the required branch.

A conflict occurred during the process, which I resolved before continuing.

### 20. Rebase Complex History

```bash
git rebase issue-555 --onto your-master
```

I used `--onto` to move only the required commits onto another branch while leaving unrelated work behind.

### 21. Change the Order of Commits

```bash
git rebase -i HEAD~2
```

I used interactive rebase to change the order of the last two commits.

This helped me understand that Git history can be reorganized when necessary.

### 22. Find Commits That Introduced Swearwords

```bash
git log -Sshit
git rebase -i <found-commit>^
git rebase --continue
```

I used `git log -S` to search the commit history for where the unwanted text was introduced. After finding the relevant commits, I used interactive rebase to edit them.

### 23. Find the Commit That Introduced a Bug

```bash
git bisect start
git bisect bad HEAD
```

I used `git bisect` to search through the commit history and find the first commit that introduced the bug.

The idea behind `git bisect` was interesting because instead of checking every commit one by one, Git performs a binary search between good and bad commits.

## Main Concepts I Learned

### Git

Through these exercises I practiced:

* staging and committing
* branches and merging
* resolving merge conflicts
* `git stash`
* `git reset`
* `git rebase`
* interactive rebase
* `git reflog`
* cherry-picking
* partial staging
* `.gitignore`
* tracking file permissions
* searching commit history
* `git bisect`

### What I learned from the task

Before this task, I mainly thought of Git as something used for uploading code to GitHub. After completing these exercises, I have a much better understanding of how Git actually manages changes and history.

The biggest lessons for me were understanding the difference between the working directory and staging area, and learning that Git history can be modified, investigated, and recovered when something goes wrong.

Some exercises were confusing initially, especially the ones involving rebase and reset, but working through them helped me understand why those commands exist instead of just memorizing their syntax.

## Conclusion

I completed all 23 Git exercises and gained practical experience with both basic and advanced Git workflows.

The task gave me a better understanding of how Git can be used not only to save code, but also to organize work, fix mistakes, investigate history, and maintain a clean development workflow.
