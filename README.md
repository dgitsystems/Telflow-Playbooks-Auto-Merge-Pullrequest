# Auto merge my pull requests

A GitHub Action to automatically merge pull requests on my repositories if:

*   I opened the PR
*   if the pr is from the INPUT_GITHUB_PR_AUTHOR specified then it will allow the PR and auto approve then merged it
*   if it is not a pr from the INPUT_GITHUB_PR_AUTHOR then it will comment on the merge and close it



## Usage

Fork this repo, add your own rules in `merge_and_cleanup_branch.py`.

Reference the Action in your `.workflow` file: .github/workflows/dgit-auto-approve.yml

below is the telflow-playbook referance.

```yml

name: Auto approve
on: 
  pull_request:
    types: 
      - opened
      - reopened
    branches: 
      - 'stable/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: dgitsystems/Telflow-Playbooks-Auto-Merge-Pullrequest@development
      env:
        INPUT_GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
        INPUT_GITHUB_PR_AUTHOR: "dgit-ci"
        INPUT_GITHUB_PERSONAL_TOKEN: "${{ secrets.DGIT_CI_TOKEN }}"

```



## Limitations

*   This will only merge pull requests which I opened.
    If you use this Action unmodified, you'll grant me magic PR-merging powers.

*   I'm only using this on repos that have a single test task.
    So it can handle this:

    ![](onetask.png)

    but it gets confused by this:

    ![](multitask.png)

    It will try to merge the pull request as soon as one of those checks completes.
    I only have a single task on each of my repos, so that's fine for me -- something like the `check_suite` trigger is probably more appropriate for larger builds.



## License

MIT.
