# Changelog

## [0.2.0] - Core Backend

### Added
- System-wide liquidity aggregation, chronologically sorted fiat and crypto transaction history, and password-sanitised user lookup for admin panel.
- User registration and login with SHA-256 password hashing, input length validation, and automatic database record population.
- Live USD cryptocurrency pricing via CoinGecko (BTC, ETH, SOL), live fiat exchange rates via ExchangeRate-API, and fiat-to-crypto currency conversion with transaction logging.
- JSON database loading and saving functionality paired with a structured user schema template.
- Cryptocurrency asset transfer logic with self-transfer and negative gas fee validation, ETH gas fee deduction, and dual-sided sender and receiver transaction logging.
- Cryptocurrency asset staking with balance migration to staked holdings and recursive daily compound yield calculation.
- 12-word seed phrase generation and deterministic SHA-256 wallet address derivation.

### Changed
- Split the user database schema into dedicated fiat (balances and transactions) and crypto wallet (address, available assets, staked assets, and transactions) sections.
- Modularised exchange rate fetching into a standalone service and replaced early database prototypes with a portable JSON schema template.

### Security
- Externalized private API keys out of the exchange rate service into an untracked local configuration file backed by an example template.
- Stripped password hashes from user records in admin panel queries prior to UI exposure.

## [0.1.0] - Initial Setup
- Initialised project