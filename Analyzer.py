from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller import GitRepository
import pandas
import utils
import datetime
import os


class Analyzer:
    def __init__(self, name, path, delta_delta, start_delta, end_delta):
        self.name = name
        self.path = path
        self.delta_delta = delta_delta
        self.start_delta = start_delta
        self.end_delta = end_delta
        gitRepo = GitRepository(path=path)
        commits = gitRepo.get_list_commits()
        self.commits = [commit for commit in commits]
        # self.commits_hash = [commit.hash for commit in commits]
        self.first_date = self.commits[0].committer_date
        self.last_date = self.commits[len(self.commits)-1].committer_date

    def run(self):
        delta = self.start_delta

        while 1:
            print("git path: {}, time delta: {}\n".format(self.path, delta))

            res = self.caculate(delta)

            self.writeToExcel(res, delta)

            delta += self.delta_delta
            if delta > self.end_delta:
                break

    def caculate(self, delta):
        res = []
        commit_time1 = self.first_date
        files_last = []
        while 1:
            commit_time2 = commit_time1 + datetime.timedelta(days=delta)
            metric = CommitsCount(path_to_repo=self.path,
                                  since=commit_time1,
                                  to=commit_time2)
            files_new = metric.count()

            commit_time1 = commit_time2
            entropy = utils.get_entropy(files_new)
            if len(files_last) == 0:
                KL_entropy = 0
            else:
                KL_entropy = utils.get_KL(files_last, files_new)

            files_last = files_new

            res.append((entropy, KL_entropy))

            if commit_time2 > self.last_date:
                break

        return res

    def writeToExcel(self, res, delta, columns=['entropy', 'KL']):
        if not os.path.exists("./{}_res".format(self.name)):
            os.mkdir("./{}_res".format(self.name))
        df = pandas.DataFrame(
            res, columns=['entropy', 'KL'])
        writer = pandas.ExcelWriter(
            './{}_res/time_{}.xlsx'.format(self.name, delta), engine='xlsxwriter')
        df.to_excel(writer, sheet_name='entropy', index=True)
        writer.save()
