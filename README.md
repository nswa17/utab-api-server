# ** Important **

The UTab-api project has moved to [utab-core-js](https://github.com/taulukointipalvelut/utab-core-js).

This repository is not maintenanced.

# UTab API Server

UTab api server provides interfaces to operate UTab.

## Files

 + "ERRORS.md" - Errors and Status Codes
 + "CHANGELOG.md" - Release notes
 + "NEXT.md" - Concrete interface in the next api version
 + "TERMS.md" - Terms
 + "INSTRUCTIONS.md" - Overview and Interfaces for developers

## Documents

Documents for UTab API are available at [here](http://UTab-api-server.readthedocs.io/en/latest/)

## Usage

1. Clone this repository. `git clone https://github.com/taulukointipalvelut/utab-api-server`

2. Install dependencies. `pip install bottle`

3. Move to repository folder. `cd utab-api-server`

4. Run app.py. `python(3) app.py`.

## Attention

1. speaker, institution -> team の順に登録

1. institution -> adjudicator の順に登録

1. トーナメント名に限っては重複不可能. スペースもなし.
