import os

ROOT_CONCURRENCY = 4 ## Processes to be spawned over the first folder you provide.
EXCLUDE_ROOT=[] ## Names to be excluded from indexing and organization on from the root folder
WORK_DIR="/home/xshell/extra_data/tmp/" ## Output folder
INDEX_PATH = os.path.join(WORK_DIR, "index") ## Index folder
PROJECTNAMES=["int_net", "inet", "L2L3Forwarder", "Rehtse"] # Software project names. This stops recursion.
SW_PROJECTS_OUTPUT = "projects" ## The output for directories listed @ PROJECTNAMES
BANNED_MIMES = [ ## Mimetype blacklist
    "application/java-archive",
    "application/vnd.debian.binary-package"
]
