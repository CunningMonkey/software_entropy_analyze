import Analyzer
import sys
import getopt


def main(argv):
    if len(argv) == 2:
        analyzer = Analyzer.Analyzer(argv[0], argv[1], auto=True)
        analyzer.run()
    elif len(argv) == 3:
        analyzer = Analyzer.Analyzer(
            argv[0], argv[1], auto=False, deltas=argv[2])
    else:
        print("python main.py <project_name> <project_path> <deltas>")
        return


if __name__ == "__main__":
    main(sys.argv[1:])
