#!/usr/bin/env bash
# Single entry point for every check in this repository.
#
# Each arm below is the exact command CI runs; the workflow in
# .github/workflows/docs.yml calls this script and holds no second copy.
# The `tests` arm is hermetic: it stubs the pinned parser, so it runs on a bare
# interpreter before provisioning and covers the gate scripts themselves.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"

usage() {
  cat <<'USAGE'
usage: ./run.sh ARM

Offline arms (default Python; no network, no install; `docs` needs PyYAML):
  docs       relative links + YAML/CFF metadata + documentation-index coverage
  links      only the relative-link check
  metadata   only the YAML parse and CITATION.cff key check
  index      only the documentation-index coverage check
  tests      hermetic unit tests for the gate scripts; needs no wheel

Network arms (need the pinned parser; run ./run.sh setup first):
  gnn        parse and type-check gnn/learner_perception_model.md against the pin
  setup      install .github/requirements-gate.txt and the pinned GNN parser

Convenience:
  all        docs, tests, then gnn
  measure    refresh docs/arm-runtimes.md; add --check to verify it instead
  help       this text

CI runs `./run.sh setup`, then `./run.sh docs`, then `./run.sh tests`, then
`./run.sh gnn`.
USAGE
}

case "${1:-help}" in
  docs)     exec "$PYTHON" .github/scripts/check_docs.py ;;
  links)    exec "$PYTHON" .github/scripts/check_docs.py --only links ;;
  metadata) exec "$PYTHON" .github/scripts/check_docs.py --only metadata ;;
  index)    exec "$PYTHON" .github/scripts/check_docs.py --only index ;;
  tests)    exec "$PYTHON" -m unittest discover -s .github/scripts/tests -v ;;
  gnn)      exec "$PYTHON" .github/scripts/check_gnn.py ;;
  setup)    exec "$PYTHON" .github/scripts/setup_gate.py ;;
  all)
    "$PYTHON" .github/scripts/check_docs.py
    "$PYTHON" -m unittest discover -s .github/scripts/tests -v
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
