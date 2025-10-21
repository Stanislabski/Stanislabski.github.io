#! /bin/bash

# print folder contents for debugging
printf "\n\nContents:\n\n"
ls

# run cite process
python3 _cite/cite.py

# run web.py to generate initial network graph
python3 web.py

# run jekyll serve in hot-reload mode
# rerun whenever _config.yaml OR webweb.json changes
watchmedo auto-restart \
    --debug-force-polling \
    --patterns="_config.yaml;_data/webweb.json" \
    --signal SIGTERM \
    -- bundle exec jekyll serve --open-url --force_polling --livereload --trace --host=0.0.0.0 \
    | sed "s/LiveReload address.*//g;s/0.0.0.0/localhost/g" &

# rerun cite process whenever _data files change
watchmedo shell-command \
    --debug-force-polling \
    --recursive \
    --wait \
    --command="python3 _cite/cite.py" \
    --patterns="_data/sources*;_data/orcid*;_data/pubmed*;_data/google-scholar*" &

# rerun web.py whenever member files, citations, or config changes
watchmedo shell-command \
    --debug-force-polling \
    --recursive \
    --wait \
    --command="python3 web.py" \
    --patterns="_members/*.md;web.py;_data/citations.yaml;_data/webweb-config.yaml;research/index.md;_styles/webweb.scss;_scripts/webweb.bundle.js;_includes/webweb.html"