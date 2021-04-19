import datetime
from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller import GitRepository
import utils
import pandas


getRepo = GitRepository(path="./tiedot")
commits = getRepo.get_list_commits()


commits = [commit for commit in commits]
commits_hash = [commit.hash for commit in commits]

commmits_count = len(commits_hash)

first_date = commits[0].committer_date
last_date = commits[commmits_count-1].committer_date


# by commit counts
delta = 10
while 1:
    print("commits delta: {}\n".format(delta))
    res = []
    files_last = []
    for i in range(0, commmits_count-delta, delta):
        metric = CommitsCount(path_to_repo='./tiedot',
                              from_commit=commits_hash[i],
                              to_commit=commits_hash[i+delta])

        files = metric.count()
        entropy = utils.get_entropy(files)
        if i == 0:
            KL_entropy = 0
        else:
            KL_entropy = utils.get_KL(files_last, files)
        files_last = files
        # commits_msges = []
        dmm_unit_size = 0
        dmm_unit_complexity = 0
        dmm_unit_interfacing = 0
        for k in range(i, i+delta):
            if k > len(commits):
                break
            # commits_msges.append(commits[k].msg)
            dmm_unit_size += commits[k].dmm_unit_size if commits[k].dmm_unit_size is not None else 0.5
            dmm_unit_complexity += commits[k].dmm_unit_complexity if commits[k].dmm_unit_complexity is not None else 0.5
            dmm_unit_interfacing += commits[k].dmm_unit_interfacing if commits[k].dmm_unit_interfacing is not None else 0.5

        res.append((entropy, KL_entropy, dmm_unit_size,
                    dmm_unit_complexity, dmm_unit_interfacing))

    df = pandas.DataFrame(
        res, columns=['entropy', 'KL', 'dmm_size', 'dmm_complexity', 'dmm_interfacing'])
    writer = pandas.ExcelWriter(
        'commit_{}.xlsx'.format(delta), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='entropy', index=True)
    writer.save()

    delta += 10
    if delta > 100:
        break

# by time length
# commit_time1 = first_date
# time_delta = 10
# while 1:

#     print("time delta: {}\n".format(time_delta))
#     entropies = []
#     commit_time1 = first_date
#     while 1:
#         commit_time2 = commit_time1 + datetime.timedelta(days=time_delta)
#         if commit_time2 > last_date:
#             break
#         metric = CommitsCount(path_to_repo='../vim',
#                               since=commit_time1,
#                               to=commit_time2)
#         files = metric.count()

#         commit_time1 = commit_time2

#         # print('Entropy: {}\n'.format(utils.get_entropy(files)))

#         entropies.append(utils.get_entropy(files))

#     df = pandas.DataFrame(entropies)
#     writer = pandas.ExcelWriter(
#         'time_{}.xlsx'.format(time_delta), engine='xlsxwriter')
#     df.to_excel(writer, sheet_name='entropy', index=True)
#     writer.save()

#     time_delta += 10
#     if time_delta > 60:
#         break
