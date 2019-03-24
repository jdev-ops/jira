import argparse
import json
import services
import pprint

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Jira utilities')

    parser.add_argument(
        '-a',
        '--act',
        type=str,
        default='null',
        help='collect issues without owner')

    parser.add_argument(
        '-d',
        '--des',
        default=1,
        type=str,
        dest='number',
        help='get issue description')

    args = parser.parse_args()
    file_name = "issues.json"
    if args.act == "i":
        issues = services.get_all_issues()
        open(file_name, "w").write(json.dumps(issues))
        keys = ['pn', 's']
        issues = {
            ikey: {key: issues[ikey][key]
                   for key in keys}
            for ikey in issues.keys()
        }
        for index, issue in issues.items():
            pprint.pprint((index, issue))

    elif args.act == "d":
        issues = json.loads(open(file_name).read())
        print(issues[args.number]["d"])
