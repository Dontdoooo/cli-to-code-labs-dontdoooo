# Network Configuration Renderer Tool

This repository contains a Python-based automation tool that leverages **Jinja2** templates to dynamically generate Cisco IOS switch configurations from multiple structured inventory formats (CSV, JSON, and XML).

## 1. Scenario & Device Selection
* **Device Type:** Cisco IOS L2/L3 Switches.
* **Scenario:** This project automates the generation of standardized base configurations (including Hostnames, Management IPs, Default Gateways, User VLANs, SNMP, and NTP settings) for remote branch offices (e.g., NYC, LAX, and HAN sites) to ensure configuration consistency and eliminate manual CLI deployment errors.

---

## 2. Setup Instructions

Follow these steps to set up the local Python virtual environment and install the required dependencies:

```bash
# 1. Clone the repository
git clone [https://github.com/Dontdoooo/cli-to-code-labs-dontdoooo.git](https://github.com/Dontdoooo/cli-to-code-labs-dontdoooo.git)
cd cli-to-code-labs-dontdoooo

# 2. Create a Python virtual environment named 'venv'
python -m venv venv

# 3. Activate the virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux / Ubuntu VM / macOS:
source venv/bin/activate

# 4. Install required dependencies
pip install -r requirements.txt


# 5. Execution Commands
python config_renderer.py --template device-template.j2 --inventory inventory.csv --format csv