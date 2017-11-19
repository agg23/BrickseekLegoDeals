# BrickseekLegoDeals

Searches for the specified Walmart (or Target, or any other retail store supported by Brickseek) SKU, and compares it to the Brickset database, pulling image data, MSRP, and part count. Sends an email of the best deals to the specified email address.

## Usage

Update `bricksetApiKey` and `useragent` in `deals.py` to the pertinent values.

To build the deals list, run:

`python3 deals.py [from email] [from email Gmail password] [to email]`

If you request more than ~60 SKUs, you will run into Brickseek's DDoS protection. The script will detect this, and prompt you for `cf_clearance` and `cfduid` cookies. These can be obtained by solving the captcha via a standard web browser, then copying the cookies (for example, from the "Application" section of Chrome Web Inspector) into the prompts.