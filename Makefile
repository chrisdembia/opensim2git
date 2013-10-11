
#http://stackoverflow.com/questions/3009738/what-does-this-svn2git-error-mean/4434188#4434188

#http://stackoverflow.com/questions/1216733/remove-a-directory-permanently-from-git

#http://stackoverflow.com/questions/359424/detach-subdirectory-into-separate-git-repository

#http://gitorious.org/svn2git/svn2git/source/539de0386876ed470f2ae6be90a98421493b3c90:samples

#http://git-scm.com/book/en/Git-and-Other-Systems-Migrating-to-Git

#http://git-scm.com/book/en/Git-and-Other-Systems-Migrating-to-Git

#git filter-branch --prune-empty --subdirectory-filter Vendors/CFSQP master
#rm -rf .git/refs/original/ && git reflog expire --all &&  git gc --aggressive --prune=now
#git reflog expire --all --expire-unreachable=0
#git repack -A -d
#git prune

# authors
# convert
# branches -> tags
# line endings
# update authors

rebase:
	svn2git --rebase --verbose &>> svn2git_log.txt
opensim2git:
	svn2git https://simtk.org/svn/opensim --trunk Trunk --tags Tags --branches Branches \
		--authors authors.txt --verbose --metadata &>> svn2git_log.txt

clearhistory:
	git log --pretty=format:'' | wc -l
	git filter-branch --tree-filter 'rm -rf Vendors/CFSQP' -- --all
	git log --pretty=format:'' | wc -l

removebackup:
	rm -rf .git/refs/original/ && git reflog expire --all &&  git gc --aggressive --prune=now
	git reflog expire --all --expire-unreachable=0
	git repack -A -d
	git prune

removegui:
	git log --pretty=format:'' | wc -l
	git filter-branch -f --tree-filter 'rm -rf Gui' -- --all
	git log --pretty-format:'' | wc -l
