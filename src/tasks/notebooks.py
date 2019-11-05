import os
from pathlib import Path


def export_user_analysis():

    main_abs_path = str(Path(__name__).parent.absolute())
    print(main_abs_path)
    os.chdir(main_abs_path)

    s = "jupyter nbconvert --execute --to html notebooks/analysis_mail_users.ipynb --output-dir notebooks/exports/"
    os.system(s)
