# Relate Python Lab dev container.
# One container, no services. Everything the lessons need is Python and one package.
FROM mcr.microsoft.com/devcontainers/python:3.3.3-3.13-bookworm

# The non-root user the base image ships with. Students work as this user.
ARG USERNAME=vscode
RUN id "${USERNAME}" >/dev/null 2>&1 \
    || { echo "User '${USERNAME}' is missing from the base image. Update USERNAME in the Dockerfile and remoteUser in devcontainer.json." >&2; exit 1; }

# relate-db, pandas and pyarrow, pinned to exact versions and checked by hash.
# They go into the image's own Python, so `python` works with no setup.
COPY requirements.txt /usr/local/share/relate-lab/requirements.txt
RUN python -m pip install --no-cache-dir --require-hashes -r /usr/local/share/relate-lab/requirements.txt \
    && python -c "import relate, pandas, pyarrow; print('relate-db', relate.__version__)"

# Helper commands and the recorded lesson checks that lab-check --full replays.
COPY bin/ /usr/local/bin/
COPY lesson-checks.json /usr/local/share/relate-lab/lesson-checks.json
RUN chmod 0755 /usr/local/bin/lab-check /usr/local/bin/lab-reset /usr/local/bin/lab-seed

# The message a student sees in their first terminal.
COPY first-run-notice.txt /usr/local/etc/vscode-dev-containers/first-run-notice.txt
