
from decouple import config

working_mode = 'dev'  # 2 modes: 'dev', 'prod'


prod_path = config("PROD_PATH")
dev_path = config('DEV_PATH')
env_doc_path=config('PRODUCTION_DOCS_PATH')
dev_full_version_path=config('DEV_FULL_VERSION_PATH')
prod_full_version_path=config('PROD_FULL_VERSION_PATH')

doc_path=''

summary_path = ''
output_path = ''
full_version_summary_path=''
fv_output_path=''

if working_mode == 'dev':
    full_version_summary_path=f'{dev_full_version_path}summary.py'
    fv_output_path=f'{dev_full_version_path}output.txt'

    summary_path = f'{dev_path}summary.py'
    output_path = f'{dev_path}output.txt'
    doc_path=''
else:
    full_version_summary_path=f'{prod_full_version_path}summary.py'
    fv_output_path=f'{prod_full_version_path}output.txt'
    
    summary_path = f'{prod_path}summary.py'
    output_path = f'{prod_path}output.txt'
    doc_path=env_doc_path


