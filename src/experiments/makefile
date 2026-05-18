# src/experiments/makefile -- per-experiment targets.
#
# Invoked from the repo root either via:
#   make experiments              (runs every target in EXPERIMENTS, slow)
#   make -C src/experiments exp_NN_<name>
#
# Add a new experiment by:
#   1. dropping exp_NN_<name>.py and exp_NN_<name>.md alongside this file
#   2. appending the target name to EXPERIMENTS
#   3. adding a target rule below

RELATIVE_PATH := ../../
include $(RELATIVE_PATH)common.mak

# The dcl-generator-zoo v0.1 has no runtime experiments; all PASS
# rows in audit_table.tex are evidenced by sympy verification scripts
# under src/utilities/.  This list is intentionally empty.
EXPERIMENTS :=

.PHONY: all $(EXPERIMENTS)

all: $(EXPERIMENTS)

# --- Individual experiments (add here as Phase~2+ lands) --------------------
