from git import Repo


# create a Repo object
repo = Repo("./")

heads = repo.heads
master = heads.master

commit = repo.commit('master')
diff = commit.diff('HEAD~1')

for diff_item in diff.iter_change_type('M'):
    print("A blob:\n{}".format(diff_item.a_blob.data_stream.read().decode('utf-8')))
    print("B blob:\n{}".format(diff_item.b_blob.data_stream.read().decode('utf-8')))

pass
