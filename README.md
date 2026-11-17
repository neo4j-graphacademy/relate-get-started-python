# Relate Python Lab: Get Started with Relate in Python

This is the hands-on environment for the course **Get Started with Relate in Python**. It runs in your browser. You install nothing on your own computer.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/neo4j-graphacademy/relate-get-started-python?quickstart=1)

The lessons are at [COURSE_URL](https://graphacademy.neo4j.com/courses/relate-get-started-python). Keep them open in one tab and this Codespace in another.

## What you need

A GitHub account. That is all.

Codespaces is free up to a monthly quota on personal accounts. This lab uses the smallest machine (2 cores). The course takes under an hour.

## Start the lab

1. Click **Open in GitHub Codespaces** above, then **Create codespace** (or **Resume** if you have one already).
2. Wait for the editor to load. The first start takes a minute or two.
3. Look at the terminal at the bottom of the window. It opens in the `lab` folder. If you see no terminal, press `` Ctrl+` `` or pick **Terminal > New Terminal** from the menu.
4. Run the check:

   ```bash
   lab-check
   ```

   Every line should say `ok`. Now start Lesson 1.

## Run the lesson code

The lessons give you two kinds of code.

**Commands** go in the terminal. Copy and paste them as written.

**Scripts** start with "Save this as `name.py`". Create the file from the terminal:

```bash
code demo.py
```

The file opens in the editor. Paste the code and save with `Ctrl+S` (`Cmd+S` on a Mac). Then run it in the terminal with `python demo.py`.

Always run scripts from the terminal. The lessons use paths like `./team.rl` and `./import`, and those are relative to the folder your terminal is in.

A few things are different here from a laptop:

| Lesson | What to know in this lab |
| --- | --- |
| 1. Install Relate for Python | `relate-db` is already installed, along with pandas and PyArrow. You can skip the four setup commands and go straight to the version check. You can also run them: they are safe. They make a virtual environment with the newest `relate-db` in it. The Windows note does not apply. |
| 2. Run Your First Query | Type `python` to open the prompt and `exit()` to leave it. |
| 3. Seed Data From Different Sources | Both `pip install` commands in the collapsibles are optional here. The packages are already installed, unless you made your own virtual environment in Lesson 1. |
| 4. Write and Read Data | Needs the `team.rl` from Lesson 3. Skipped it? Run `lab-seed 4`. |
| 5. Load a Graph From Two Sources | Asks for an empty directory. Run `mkdir -p "$LAB_DIR/challenge" && cd "$LAB_DIR/challenge"`. |
| 6. Write and Read With an Agent | Stay in the Challenge 5 folder. Skipped the challenge? Run `lab-seed 6`. Using an agent is optional. See below. |
| 7. Add Data, Then Ask Questions | Stay in the same folder. Skipped ahead? Run `lab-seed 7`. |

If you made a virtual environment in Lesson 1, it is only active in the terminal where you ran `source .venv/bin/activate`. A new terminal uses the preinstalled packages. Both work.

## Find your files

Open the **Explorer** (the top icon in the left bar) and expand `lab`. Your scripts and CSV files show up there. Click one to edit it.

Files ending in `.rl` are databases. Do not open them in the editor. Read them with Python.

## Use an agent (optional)

Lessons 6 and 7 can use an AI coding agent. You can finish both without one. Lesson 7 gives a "Solution without an agent" for that step.

The command in Lesson 6 that copies the Relate skill into `.claude/skills` works here with no agent installed. To have an agent use it, install an agent you already have an account for, the way its own docs describe, and start it in the folder that holds `team.rl`.

Nothing in this lab needs an API key.

## Check that things work

```bash
lab-check          # Python, the relate package and the lab folder
lab-check --full   # replays every lesson and challenge in a scratch folder
```

`lab-check --full` does not touch your files. This lab runs no servers and opens no ports, so there is nothing else to start or watch.

## Start over

| You want to | Run |
| --- | --- |
| Empty the lab folder | `lab-reset` |
| Empty it without the question | `lab-reset -y` |
| Leave your own virtual environment | `deactivate` |
| Rebuild the whole environment | Press `F1`, type **Codespaces: Rebuild Container**, press Enter |

After `lab-reset`, run `deactivate 2>/dev/null; cd "$LAB_DIR"` so your terminal is in a folder that still exists.

## Fix common problems

| You see | Do this |
| --- | --- |
| `ModuleNotFoundError: No module named 'relate'` | You are in a virtual environment without the package. Run `pip install relate-db`, or run `deactivate` to use the preinstalled one. |
| `ModuleNotFoundError: No module named 'pandas'` | Same cause. Run `pip install pandas pyarrow`, or `deactivate`. |
| `storage locked` | Another terminal has that database open, usually at a `python` prompt. Go there and type `exit()`. |
| `database not found` | The `.rl` file is not in this folder. Run `ls` and `pwd`. Then `cd` to the right folder, or run `lab-seed 4`, `lab-seed 6` or `lab-seed 7`. |
| `LOAD CSV file unavailable` | Set `os.environ["RELATE_LOAD_CSV_DIR"] = "./import"` before `relate.connect()`, and run the script from the folder that holds `import`. |
| `LOAD CSV invalid configuration` | The `import` folder does not exist here. Run `mkdir -p import` and create the CSV file again. |
| `IndentationError` at the `>>>` prompt | Only paste the short, unindented snippets at the prompt. Code under "Save this as" belongs in a file. |
| The prompt shows `...` and waits | Python wants the rest of a statement. Press Enter on an empty line, or `Ctrl+C` to cancel. |
| You cannot leave the Python prompt | Type `exit()` and press Enter. |
| A `CREATE` script doubled your data | `CREATE` always adds. Delete the `.rl` file and run the script once, or use `MERGE`. |
| The terminal opened somewhere else | Run `cd "$LAB_DIR"`. |
| Paste does nothing in the terminal | Your browser asks for clipboard permission the first time. Allow it, then paste again. |

## Stop or delete your Codespace

A Codespace stops by itself after 30 minutes without activity. Your files stay.

To stop it now, click **Codespaces** in the bottom-left corner and pick **Stop Current Codespace**.

When you finish the course, delete it so it stops using your storage quota. Go to [github.com/codespaces](https://github.com/codespaces), click the `...` next to the Codespace, and pick **Delete**. Deleting removes everything in the `lab` folder.
