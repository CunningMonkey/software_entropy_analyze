from git import Repo


# create a Repo object
repo = Repo("./")

heads = repo.heads
master = heads.master

commit = repo.commit('master')

pass