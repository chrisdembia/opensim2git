
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

kdesvn2git:
	# Should be able to get svn-all-fast-export from apt-get.
	# TODO remove --max-rev flag; it's there temporarily so that this doesn't
	# end with a FATAL signal. Might still end with a FATAL anyway...
	svn-all-fast-export --rules opensim2git.rules --debug-rules --add-metadata --identity-map authors.txt --stats --max-rev 7500 svn/ > kdesvn2git_log.txt 2>&1
