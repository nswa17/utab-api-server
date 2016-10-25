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

3. Move to repository folder. `utab-api-server`

4. Run app.py. `python(3) app.py`.

## Attention

1. 現在api version 2.0 (PDA Official)への対応作業中

1. speaker, institution -> team の順に登録

1. institution -> adjudicator の順に登録

## Code Names

**version 1.0** - Candle Light

**version 2.0** - PDA Official

**version 3.0** - Frosty Night

## Future Coming

### UTab api version 2.0 PDA Official (by 2016/11/20)

In the next UTab-api version, the following features will be available.

1. Support DELETE methods
1. Redundancy of result data
1. Json format checking on server side
1. Simple backup system

### UTab api version 3.0 (by 2016/12?)

1. Authentication
1. New matching algorithm
1. Official backup support
1. 複数chair対応
1. Trainee 対応
1. Modify result after finishing rounds
1. Simplify allocation indices

### UTab api version 4.0 (in 2017)

1. Options for selection algorithm
1. ラウンド数変更対応(増加含め)
1. speaker と team 登録などの順番を交換可能にする
