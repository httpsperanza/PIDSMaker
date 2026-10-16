# PIDSMaker Setup Changes and Troubleshooting

This document records local setup changes, ground-truth additions, and solutions to issues encountered during installation.

## Environment Creation

The CUDA version specified in the environment YAML file was changed.
The file used to create the environment is `PIDSMaker/scripts/apptainer/environment_modified.yaml`.

## PostgreSQL Startup and Shutdown

Database startup sometimes stalled. In other cases, the database did not shut down cleanly and required recovery on the next startup.

Additional code was appended to `postgres-start.sh` to address these database lifecycle issues.

## Ground Truth

The labels reported in the **PROVFUSION** paper were added in a dedicated directory. These labels build on and update the ground truth from **ORTHRUS** and **Reapr**. A Markdown file documents the added labels.

## Weights & Biases Authentication

### Error

Running `wandb login` and pasting the generated API key resulted in the following error:

```text
wandb: Logging into wandb.ai.
wandb: You can find your API key in your browser here: https://wandb.ai/authorize
wandb: Paste an API key from your profile and hit enter, or press ctrl+c to quit:
wandb: ERROR API key must be 40 characters long, yours was 86
```

### Workaround

Generate an API key, then set it in the terminal environment:

```bash
export WANDB_API_KEY="<YOUR_API>"
```

Replace `<YOUR_API>` with the generated key. Verify authentication in the same terminal:

```bash
wandb login
```

Expected output:

```text
wandb: Currently logged in as: <YOUR DATA>. Use `wandb login --relogin` to force relogin
```

## Makefile and Apptainer Setup

### Error

The full setup failed during the `load-dumps` target with the following error:

```text
Error: unknown command "/cm/local/apps/apptainer/current/bin/apptainer" for "apptainer"

Usage:
  apptainer [global options...] <command>

Run 'apptainer --help' for more detailed usage information.
make: *** [Makefile:49: load-dumps] Error 1
```

### Troubleshooting

Check where the database dump files were downloaded. If they are in the `PIDSMaker/` root directory, move them to:

```text
PIDSMaker/scripts/apptainer/data/
```

The following setting was also added at the beginning of the `Makefile` to explicitly select Bash:

```makefile
SHELL := /bin/bash
```