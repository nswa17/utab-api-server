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

## Code Names

**version 1.0** - Candle Light

**version 2.0** - Luna Flight

**version 3.0** - Frosty Night

## Future Coming

### UTab api version 2.0 Luna Flight (by 2016/11/20)

**To improve safety**

Planning to support
1. DELETE methods
1. Redundancy of result data
1. Json format checking on server side
1. Simple backing up system
1. Logging

### UTab api version 3.0 (by 2016/12?)

**To have more usability**

Planning to support
1. Authentication
1. Official backup support
1. Multiple chairs
1. Trainees
1. Modify result after finishing rounds
1. Simplify allocation indices

### UTab api version 4.0 (in 2017)

**To improve internal algorithms**

Planning to support
1. Options for selection algorithm
1. New matching algorithm
1. Adding rounds during operation
1. Exchanging order of registration of speakers and teams
1. Mstat

### UTab api future version

1. Modifying result after rounds
1. Speaker based institution
1. Use threading.Lock() only for the same tournament
