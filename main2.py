from pydriller.metrics.process.lines_count import LinesCount


metric = LinesCount(path_to_repo="./",
                    from_commit='HEAD~1',
                    to_commit='HEAD')

added_count = metric.count_added()
added_max = metric.max_added()
added_avg = metric.avg_added()
print('Total lines added per file: {}'.format(added_count))
print('Maximum lines added per file: {}'.format(added_max))
print('Average lines added per file: {}'.format(added_avg))
