# NextRecon

NextRecon is a simple Python-based reconnaissance tool designed for bug bounty hunters, security researchers, and penetration testers. It performs passive recon by collecting archived URLs from the Wayback Machine and fetching leaked credentials from the [BreachCollection API](https://breachcollection.com/api_docs/). It also extracts unique GET parameters from the archived URLs for further testing (e.g., fuzzing or injection analysis).

-----

## 🔗 Features

  * **Archived URL Collection**
    Gathers all URLs (optionally including subdomains) from the [Wayback Machine](https://web.archive.org/) for a given domain.

  * **Leaked Credentials Lookup**
    Queries the [BreachCollection API](https://breachcollection.com/) to find associated credential leaks using:

      * Domain name.
      * Email domain.

  * **Parameter Discovery**
    Extracts unique query parameters from collected URLs to help identify potential injection points.

  * **Output Files**

      * `DOMAIN-all_urls.txt`: All archived URLs discovered.
      * `DOMAIN-params.txt`: Unique query parameters extracted.
      * `DOMAIN-leaks.txt`: Credentials found via BreachCollection.

## Installation & Requirements

### Dependencies

  * Python 3.6+
  * Required packages:
      * `requests`
      * `pyyaml`

Install them via pip:

```bash
pip install -r requirements.txt
```

Provide your BreachCollection API key in the `config.yaml` file, so it looks like this:

```yaml
breachcollection_api_key: your_key
```

To get your API key go to [this link](https://breachcollection.com/dashboard/manage-api/) and create a new API KEY (only for Researcher and Enterprise Tiers).

## Usage

```bash
python3 nextrecon.py <domain> [include_subdomains:true/false]
```

Do not include the protocol in the field. Example of correct usage:

```bash
python3 nextrecon.py example.com true
```
