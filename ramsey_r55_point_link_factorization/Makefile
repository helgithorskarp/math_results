PYTHON ?= python3

.PHONY: check clean

check:
	$(PYTHON) -B controls.py
	$(PYTHON) -B -O controls.py
	$(PYTHON) -B check_target.py
	$(PYTHON) -B check_calibration.py
	$(PYTHON) -B verify_physical.py
	sha256sum -c SHA256SUMS

clean:
	find . -type d -name __pycache__ -prune -exec rm -r {} +
