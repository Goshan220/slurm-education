import difflib
import os
import re
import git
import gitlab


COMMENT_RE = re.compile(r".*?#\s*?TODO:(.*)")


def check_on_todo(row: str):
    matcher = re.search(COMMENT_RE, row)
    if matcher:
        return matcher.group(1).strip()


def get_diff(change_types: list, ahead, stale):
    for change_type in change_types:
        for diff in stale.diff(ahead).iter_change_type(change_type):
            yield diff


def create_discussion(discussion_content, mr, line_no, new_path, old_path):
    mr_diff = mr.diffs.list()[0]
    mr.discussions.create({'body': discussion_content,
                           'position': {
                               'base_sha': mr_diff.base_commit_sha,
                               'start_sha': mr_diff.start_commit_sha,
                               'head_sha': mr_diff.head_commit_sha,
                               'position_type': 'text',
                               'new_line': line_no,
                               'old_path': old_path,
                               'new_path': new_path}
                           })


def create_issue(project, todo, row, mr, line_no, new_path, old_path):
    print(f"create issue started with {todo}")
    for discussion in mr.discussions.list():
        for note in discussion.attributes["notes"]:
            if todo in note["body"] and not note["resolved"]:
                print("Discussion can not be duplicated")
                return

    issue = project.issues.create({'title': todo, 'description': 'Created from TODO comment task'})
    discussion_content = f"[{project.name_with_namespace}]Из TODO была создана задача [{issue.iid}]({project.web_url + '/-/issues/' + str(issue.iid)})\n" \
                         f"```suggestion:-0+0\n{row} [{issue.iid}]\n```"
    create_discussion(discussion_content, mr, line_no, new_path, old_path)


def close_issue(project, todo):
    print(f"close issue started with {todo}")
    for issue in project.issues.list(state="opened"):
        if issue.title == todo:
            print(f"try to close: {todo}")
            issue.state_event = 'close'
            issue.save()
            break


def suggestion_to_remove_todo(project, todo, row, mr, line_no, new_path, old_path):
    for issue in project.issues.list(state="closed"):
        if issue.title == todo:
            print(f"my todo: {todo}, closed issue: {issue}")
            discussion_content = f"[{project.name_with_namespace}]Задача на данный TODO уже закрыта, удалите данный TODO[{issue.iid}]({project.web_url + '/-/issues/' + str(issue.iid)})\n" \
                                 f"```suggestion:-0+0\n{row} [{issue.iid}]\n```"
            create_discussion(discussion_content, mr, line_no, new_path, old_path)


def main():
    gl = gitlab.Gitlab("https://gitlab.slurm.io", os.getenv("MY_CI_JOB_TOKEN"))
    ci_merge_request_iid_var = os.getenv("CI_OPEN_MERGE_REQUESTS").split("!")[1]
    project = gl.projects.get(os.getenv("CI_PROJECT_ID"))
    mr = project.mergerequests.get(ci_merge_request_iid_var)
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)

    origin = repo.remotes.origin

    origin.fetch()

    for diff in get_diff(["A", "M"], repo.head.commit, repo.head.commit.parents[0]):
        stale = "" if diff.a_blob is None else diff.a_blob.data_stream.read().decode("utf-8")
        ahead = "" if diff.b_blob is None else diff.b_blob.data_stream.read().decode("utf-8")

        line_no = 0
        for row in difflib.ndiff(stale.splitlines(), ahead.splitlines()):
            row = row.strip()
            if row == "":
                line_no += 1
            elif row[0] == "-":
                line_no += 1
                todo = check_on_todo(row)
                if todo:
                    close_issue(project, todo)
            elif row[0] == "+":
                line_no += 1
                row = row.strip("+ ")
                todo = check_on_todo(row)
                if todo:
                    create_issue(project, todo, row, mr, line_no, diff.b_path, diff.a_path)

        line_no = 0
        for row in ahead.splitlines():
            line_no += 1
            todo = check_on_todo(row)
            if todo:
                suggestion_to_remove_todo(project, todo, row, mr, line_no, diff.b_path, diff.a_path)


if __name__ == '__main__':
    main()
