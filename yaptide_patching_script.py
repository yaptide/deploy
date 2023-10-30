# use bash script to get all PR patches from github
# install gh cli tool before running this script
# run `gh auth login` before running this script
import subprocess
import json

from pathlib import Path
from tqdm import tqdm
from zipfile import ZipFile


def main():
    base_dir = Path(__file__).resolve().parent
    patches_dir = base_dir / "patches"
    patches_dir.mkdir(exist_ok=True)

    for repo_name in ["ui", "yaptide", "converter"]:
        repo = f"yaptide/{repo_name}"
        # get all PRs with EuroHPC label and closed state
        output = subprocess.check_output(
            f"gh pr --repo {repo} list --label EuroHPC --state all --json number --limit 10000", shell=True, text=True)
        # read json file
        data = json.loads(output)
        print(f"Number of patches for {repo} repo: {len(data)}")

        # get patches for each PR
        for i, PR in enumerate(tqdm(data, desc=f"Getting patches for {repo_name} repo", unit="patch")):
            patch = subprocess.check_output(
                f'gh pr --repo {repo} diff {PR["number"]} --patch', shell=True, text=True)

            with open(patches_dir / f'patch_{repo_name}_{PR["number"]}.patch', 'w') as f:
                f.write(patch)

    zip_file = base_dir / "patches.zip"
    with ZipFile(zip_file, 'w') as zip_obj:
        for file in patches_dir.iterdir():
            zip_obj.write(file)


if __name__ == "__main__":
    main()
