#! /bin/bash

# print folder contents for debugging
printf "\n\nContents:\n\n"
ls

python3 _scripts/gallery.py

# run cite process
python3 _cite/cite.py

# run web.py to generate initial network graph
python3 web.py

# run jekyll serve in hot-reload mode
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

# rerun gallery script whenever images in images/lab change
watchmedo shell-command \
    --debug-force-polling \
    --recursive \
    --wait \
    --command="python3 _scripts/gallery.py" \
    --patterns="images/lab/*.jpg;images/lab/*.png;images/lab/*.jpeg;images/lab/*.gif;_scripts/gallery.py;_scripts/gallery.js;_includes/gallery.html;_styles/gallery.scss" &

# rerun web.py whenever member files, citations, or config changes
watchmedo shell-command \
    --debug-force-polling \
    --recursive \
    --wait \
    --command="python3 web.py" \
    --patterns="_members/*.md;web.py;_data/citations.yaml;_data/webweb-config.yaml;research/index.md;_styles/webweb.scss;_scripts/webweb.bundle.js;_includes/webweb.html" 
