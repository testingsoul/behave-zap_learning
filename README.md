# CI_testDAST_behave

Learning repository for the `behave-zap` Python library, showing how to combine:
- Behave + Selenium functional automation
- OWASP ZAP DAST execution
- CI-based security feedback with PR annotations

![integration](docs/DAST_flow.png)

## Learning Goals

This repository helps you learn how to:
- run classic BDD tests with Behave
- select the scenarios that drive a DAST run with a Behave tag (`@dast` here, by convention)
- route browser traffic through ZAP proxy
- configure per-feature active-scan targets
- generate JUnit + ZAP reports
- publish security findings in CI pull requests

## Learning Path

1. Learn OWASP ZAP basics
- Official site: https://www.zaproxy.org/
- Getting started docs: https://www.zaproxy.org/getting-started/
- Download ZAP Desktop: https://www.zaproxy.org/download/

2. Learn `behave-zap`
- GitHub project: https://github.com/testingsoul/behave-zap
- Package (PyPI): https://pypi.org/project/behave-zap/

3. Run this repository locally
- install requirements
- run functional scenarios
- start ZAP
- run `@dast` scenarios and inspect reports

4. Understand CI security feedback
- review workflow: `.github/workflows/ci_dast.yml`
- review PR annotation action: https://github.com/testingsoul/zap-annotations

## Requirements

- Python `3.12`
- `pip`
- Docker (required for local ZAP daemon execution in this project)
- Chrome/Chromium runtime compatible with Selenium

## Installation

1. Clone repository
```bash
git clone <your-fork-or-this-repo-url>
cd CI_testDAST_behave
```

2. Create virtual environment and install dependencies
```bash
cd test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Validate Behave is available
```bash
behave --version
```

## Project Structure

- `test/features/`: Gherkin features
- `test/steps/`: step definitions
- `test/pageobjects/`: page objects
- `test/fixtures/`: files uploaded by scenarios (`invoice.pdf` for the complaint feature)
- `test/environment.py`: Behave hooks delegated to `behave-zap` runner
- `test/behave.ini`: Behave defaults — JUnit output is already enabled into `output/`
- `test/conf/properties.cfg`: runtime + DAST configuration, as used by CI
- `test/conf/local-properties.cfg.example`: starting point for local runs
- `test/output/`: generated JUnit and ZAP reports (gitignored)
- `.github/workflows/ci_dast.yml`: CI pipeline for DAST + reports + annotations

## behave-zap In This Repository

`behave-zap` centralizes the integration between Behave, Selenium driver management, and ZAP lifecycle/reporting hooks.

Current integration (`test/environment.py`):
- creates a shared runner using `create_default_runner(...)`
- reads configuration from `conf/properties.cfg`
- delegates all Behave lifecycle hooks (`before_all`, `before_feature`, `before_scenario`, `after_scenario`, `after_feature`, `after_all`) to the runner

Why this matters for learning:
- test glue code stays very small
- DAST behavior is controlled from configuration, not hardcoded in steps
- you can focus on feature and step design while reusing a standard security testing pipeline

## Features and Tags

| Feature file | What it covers | Active-scan targets key |
| --- | --- | --- |
| `login.feature` | valid and invalid login | `targets_login` |
| `create_user.feature` | user registration | `targets_create_user` |
| `product_basket.feature` | search, add, increase, delete basket items | `targets_product_basket` |
| `product_checkout.feature` | checkout with new address and card | `targets_product_checkout` |
| `customer_feedback.feature` | feedback form submission | `targets_customer_feedback` |
| `user_complaint.feature` | complaint with `fixtures/invoice.pdf` upload | `targets_user_complaint` |

Two tags appear in the feature files:

- `@dast` — an ordinary Behave tag, nothing more. `behave-zap` never looks at tags,
  so the name carries no special meaning: `@security`, `@scan` or anything else
  works identically, as long as you pass it to `behave -t`. Tagging the scenarios
  you want included in a DAST run is the whole mechanism — `behave -t @dast` simply
  selects which scenarios execute, and therefore which traffic ZAP observes.
  Whether scanning happens at all is decided by `pscan` / `ascan` and the
  `targets_<feature>` keys in the config.
- `@reuse_driver` — currently has no effect. The runner creates a single Selenium
  driver in `before_all` and closes it in `after_all`, so the browser is shared
  across the whole run either way.

## Quick Start: Local OWASP Juice Shop

The fastest way to try this repository is to run everything against a local
[OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) instance. You only need Docker.

### 1. Start Juice Shop

```bash
docker run --rm -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
```

- `-d` runs it in the background, `--name juice-shop` makes it easy to stop later.
- First launch pulls the image (~1–2 min). The app is ready when
  http://localhost:3000 loads in a browser and returns the Juice Shop home page.

Verify it is up:

```bash
curl -sf http://localhost:3000 >/dev/null && echo "Juice Shop is ready"
```

When you are done, stop it with:

```bash
docker stop juice-shop
```

### 2. Point the tests at the local instance

`test/environment.py` always loads `conf/properties.cfg`. The committed version of
that file is tuned for CI: headless browser, and `dockerized: true` so `behave-zap`
starts ZAP itself. For local work, start from the tracked example instead — it runs
the browser visibly and expects you to control the ZAP daemon:

```bash
cd test
cp conf/properties.cfg conf/properties.cfg.bak      # keep the CI config around
cp conf/local-properties.cfg.example conf/properties.cfg
```

> Tip: `conf/local-*.cfg` is gitignored, so you can also park a personal copy at
> `conf/local-properties.cfg` and copy from there without dirtying `git status`.

### 3. Run the tests

The example config leaves `pscan` and `ascan` enabled, and `behave-zap` connects to
ZAP whenever either is on — **even for an untagged `behave` run**. So either start
ZAP first (see the next section), or turn scanning off for a purely functional run:

```bash
cd test
source venv/bin/activate

# Functional scenarios, no ZAP involved:
# set pscan: false and ascan: false in conf/properties.cfg first
behave

# Everything, with ZAP running
behave -t @dast
```

Without ZAP up and `pscan`/`ascan` still enabled, the run stops in `before_all`
with `Could not reach the ZAP API at http://0.0.0.0:8080`.

## Local Execution with DAST

To scan locally you need a ZAP daemon in addition to Juice Shop. You can let
`behave-zap` manage it, or run it yourself.

1. Start Juice Shop and switch to the local config (see the Quick Start above).

2. Provide a ZAP daemon, either way round:

   **a. Let `behave-zap` do it** — set `dockerized: true` in `[DAST]` and skip to
   step 3. The library starts `zaproxy/zap-stable:2.17.0`, waits for the API, and
   stops the container at the end of the run. This is what CI does.

   **b. Run it yourself** — keep `dockerized: false` (the example default) and start
   the daemon before running Behave. Handy when you want to keep the session open
   and poke at it afterwards:

   ```bash
   docker run -u zap -p 8080:8080 -d zaproxy/zap-stable \
     zap.sh -daemon -host 0.0.0.0 -port 8080 \
     -config api.addrs.addr.name=.* \
     -config api.addrs.addr.regex=true \
     -config api.key=change-me-9203935709
   ```

   The `api.key` must match `api_key` in `[DAST]`.

3. Run DAST-tagged scenarios
```bash
cd test
source venv/bin/activate
behave -t @dast
```

`test/behave.ini` already sets `junit = true` and `junit_directory = output`, so no
extra flags are needed; `--junit --junit-directory output` just restates them.

Artifacts generated:
- JUnit XML, one file per feature: `test/output/TESTS-features.<feature>.xml`
- ZAP reports for the whole run, written once in `after_all`:
  `test/output/zapreport-final.html` and `test/output/zapreport-final.xml`

## DAST Configuration Reference (`test/conf/properties.cfg`)

### `[Driver]`
- `implicitly_wait`: Selenium implicit wait (seconds).
- `explicitly_wait`: explicit wait timeout used by the framework (seconds).
- `headless`: run browser headless (`true`/`false`).

### `[Capabilities]`
- Reserved section for Selenium capabilities if needed.

### `[ChromeArguments]`
Chrome startup arguments passed to the driver, including the browser window size
(`window-size: 1920,1080`) and security/proxy-compatible flags such as:
- `ignore-certificate-errors`
- `allow-insecure-localhost`
- `allow-running-insecure-content`
- `disable-web-security`
- `proxy-bypass-list: <-loopback>`

When DAST is enabled the runner injects `proxy-server` into this section at
startup, pointing Chrome at the ZAP proxy — do not set it by hand.

### `[Test]`
- `url`: base application URL under test.
- `username`, `password`: credentials used by login scenarios.

### `[DAST]`
Keys used in this repository:
- `dockerized`: if `true`, `behave-zap` starts and stops the ZAP container itself;
  if `false`, it expects ZAP to be running already and fails fast when it is not.
- `api_key`: ZAP API key. Must match the key the ZAP daemon was started with.
- `proxy-server`: ZAP host/port the browser proxies through.
- `pscan`: enable/disable passive scan (`true`/`false`).
- `ascan`: enable/disable active scan (`true`/`false`).
- `targets_<feature_name>`: per-feature active-scan target list (comma-separated URLs).
- `exclude_targets`: regex patterns excluded from scanning.
- `session_timeout_seconds`: how long the app session is assumed to last; the runner
  refreshes the browser before it expires while waiting on long scans.
- `session_auth_sync`: mirror the browser's auth headers into ZAP replacer rules, so
  the active scan keeps hitting authenticated endpoints as the logged-in user.

Optional keys `behave-zap` also accepts, with their defaults, if you want to
experiment beyond what this project sets:
- `scan_strength`: `LOW` | `MEDIUM` | `HIGH` | `INSANE` — how many attack variants
  each rule fires (default `HIGH`; unknown values fall back to it).
- `scan_threshold`: `OFF` | `LOW` | `MEDIUM` | `HIGH` | `DEFAULT` — confidence needed
  before a rule raises an alert (default `DEFAULT`).
- `output_dir`: where reports are written (default `output`).
- `zap_port`: ZAP proxy/API port (default `8080`).
- `docker_image`: default `zaproxy/zap-stable:2.17.0`, used when `dockerized: true`.
- `container_name`: default `behave-zap`.
- `docker_network`: default `host`.

Important mapping rule: the key is `targets_` plus the feature **file name** without
its extension, so a renamed feature file silently loses its targets (the run prints
`No active scan targets configured for feature file ...` and skips the active scan).
Current mapping:
- `targets_login` → `test/features/login.feature`
- `targets_create_user` → `test/features/create_user.feature`
- `targets_product_basket` → `test/features/product_basket.feature`
- `targets_product_checkout` → `test/features/product_checkout.feature`
- `targets_customer_feedback` → `test/features/customer_feedback.feature`
- `targets_user_complaint` → `test/features/user_complaint.feature`

## CI Pipeline Details

Workflow file: `.github/workflows/ci_dast.yml`

Triggers: pushes and pull requests targeting `main`.

Main job (`build-and-test`) does:
- checkout code
- setup Python 3.12
- install `test/requirements.txt`
- start OWASP Juice Shop in Docker (`bkimminich/juice-shop` on port 3000)
- poll `http://localhost:3000` until Juice Shop answers (30 tries, 5s apart)
- execute `behave -t @dast --junit --junit-directory output`
- upload acceptance test artifacts (`TESTS-*.xml`, 1 day retention)
- upload ZAP HTML reports (3 day retention)
- on Pull Requests: run `testingsoul/zap-annotations@v1` for `Critical,High,Medium`

There is deliberately no ZAP step: the committed `test/conf/properties.cfg` sets
`dockerized: true`, so `behave-zap` starts and stops the ZAP container itself as part
of the run. Flipping that key to `false` without adding a ZAP step will break CI.

PR annotations project:
- https://github.com/testingsoul/zap-annotations

Required secret for annotations:
- `ACTION_TOKEN` (used as `GITHUB_TOKEN` env for annotation publishing)

Second job (`publish-acceptance-test-results`):
- downloads acceptance test artifacts
- publishes unit test style report using `EnricoMi/publish-unit-test-result-action`

## Additional Documentation

- `behave-zap` library: https://github.com/testingsoul/behave-zap
- PR annotation action: https://github.com/testingsoul/zap-annotations
- OWASP ZAP docs: https://www.zaproxy.org/docs/
- OWASP Juice Shop: https://owasp.org/www-project-juice-shop/
- DAST flow diagram: `docs/DAST_flow.png`
