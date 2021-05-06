from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller import GitRepository
import pandas
import utils
import datetime
import os
import logging


class Analyzer:
    def __init__(self, name, path, auto, deltas=None):
        self.name = name
        self.path = path
        gitRepo = GitRepository(path=path)
        commits = gitRepo.get_list_commits()
        self.commits = [commit for commit in commits]
        # self.commits_hash = [commit.hash for commit in commits]
        self.first_date = self.commits[0].committer_date
        self.last_date = self.commits[len(self.commits)-1].committer_date
        self.auto = auto
        self.deltas = []
        # self.frequency = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
        self.frequency = [50, 100, 150]
        if auto:
            time_length = self.last_date - self.first_date
            for item in self.frequency:
                self.deltas.append(time_length/item)
        else:
            self.deltas = deltas

        self.logger = logging.getLogger('Analyzer')
        logging.basicConfig(level=logging.CRITICAL,
                            filename='software.log', filemode='w')

    def run(self):

        for i, delta in enumerate(self.deltas):
            self.logger.critical("project name: {}, round:{}, git path: {}, time delta: {}\n".format(
                self.name, i, self.path, delta))
            res = self.caculate(delta, self.frequency[i])

            self.writeToExcel(res, delta)

    def caculate(self, delta, frequency):
        res = []
        commit_time1 = self.first_date
        files_last = []

        for i in range(0, frequency):
            if i % 10 == 0:
                self.logger.critical("now at :{}%{}\n".format(i, frequency))
            commit_time2 = commit_time1 + delta
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

            res.append((commit_time1.strftime('%Y-%m-%d-%H-%M'),
                       commit_time2.strftime('%Y-%m-%d-%H-%M'), entropy, KL_entropy))

            if commit_time2 > self.last_date:
                break

        return res

    def writeToExcel(self, res, delta, columns=['start_time', 'end_time', 'entropy', 'KL']):
        if not os.path.exists("./{}_res".format(self.name)):
            os.mkdir("./{}_res".format(self.name))
        df = pandas.DataFrame(
            res, columns=columns)
        writer = pandas.ExcelWriter(
            './{}_res/time_{}.xlsx'.format(self.name, delta), engine='xlsxwriter')
        df.to_excel(writer, sheet_name='entropy', index=True)
        writer.save()
