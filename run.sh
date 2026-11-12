#!/usr/bin/env bash
# Single entry point for every check in this repository.
#
# Each arm below is the exact command CI runs; the workflow in
# .github/workflows/docs.yml calls this script and holds no second copy.
# There are no lint, type, or unit-test arms: the repository ships documentation
# and metadata, and this script plus check_docs.py is its whole executable surface.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"

usage() {
  cat <<'USAGE'
usage: ./run.sh ARM

Offline arms (default Python with PyYAML; no network, no install):
  docs       relative links + YAML/CFF metadata + documentation-index coverage
  links      only the relative-link check
  metadata   only the YAML parse and CITATION.cff key check
  index      only the documentation-index coverage check

Network arms (need the pinned parser; run ./run.sh setup first):
  gnn        parse and type-check gnn/learner_perception_model.md against the pin
  setup      install .github/requirements-gate.txt and the pinned GNN parser

Convenience:
  all        docs, then gnn
  measure    refresh docs/arm-runtimes.md; add --check to verify it instead
  help       this text

CI runs `./run.sh setup`, then `./run.sh docs`, then `./run.sh gnn`.
USAGE
}

case "${1:-help}" in
  docs)     exec "$PYTHON" .github/scripts/check_docs.py ;;
  links)    exec "$PYTHON" .github/scripts/check_docs.py --only links ;;
  metadata) exec "$PYTHON" .github/scripts/check_docs.py --only metadata ;;
  index)    exec "$PYTHON" .github/scripts/check_docs.py --only index ;;
  gnn)      exec "$PYTHON" .github/scripts/check_gnn.py ;;
  setup)    exec "$PYTHON" .github/scripts/setup_gate.py ;;
  all)
    "$PYTHON" .github/scripts/check_docs.py
    exec "$PYTHON" .github/scripts/check_gnn.py
    ;;
  measure)
    shift
    exec "$PYTHON" .github/scripts/measure_arms.py "$@"
    ;;
  help | -h | --help)
    usage
    ;;
  *)
    echo "unknown arm: ${1}" >&2
    usage >&2
    exit 2
    ;;
esac
