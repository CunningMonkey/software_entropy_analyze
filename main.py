from git import Repo


# create a Repo object
repo = Repo("../neovim")

heads = repo.heads
master = heads.master

commit = repo.commit('master')