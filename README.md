# base-image-aggregator
Given a list a list of repositories with commit SHAs, this will gather and aggregate base images used in the Dockerfiles across the repositories provided. The source URL should link to a plaintext list of git repositorys and their commit SHAs as key value pairs separated by a space, one key value pair per line, each line ending in a "\n" return character. 

## Example Source 
Admittedly not great examples because neither contain Dockerfiles, but it demotrates the expected format.

https://github.com/gavin-dale/base-image-aggregator.git f8d0a9fee8c7889f65cc83180d1d4949f94128da

https://github.com/gavin-dale/tic-tax-tac-toe.git 75721da29d1bf2fd4fb3ae1fa9700332cba7bbac

## Usage
`python main.py <url to source>`

A report will be written to data.json. Each section will contain a link to the repo with the specified commit SHA, a list of all the Dockerfiles and the directories they're in, and the name of the base image within those Dockerfiles.

## Implementation Details
There is two primary entities we're working with here, Repositorys and Reports. A repository is a model of a single git repository containing data like the repo URL, commit SHA, and Dockerfile location details. The Report object contains the details and implementation needed to format and write the data held in the Repository object. main.py pulls it all together by looping through all of the provided sources, then writing the report. 
