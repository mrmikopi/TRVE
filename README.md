# TRVE
TRVE is a Data Engineering Project that fetches band names from Metal Archieves Dataset and collects all tracks it can find from Spotify API. Band names, genres, album & track information and track features are merged together in a single dataset. 

Scala file for data extraction, DataExtraction.scala, can be run with `spark-shell` at the moment. It will be turned into its own `.jar`, soon.

## Methods:

### Scala
DataExtraction.scala provides:

#### getMadPlus()

MAD stands for Metal Archieves Dataset, and Plus is for adding song genres to their relative columns.

- [x] Able to read M.A.D. repository files.
- [ ] Path is set with input.
- [ ] Option for auto-download dataset first.

#### getRandomTrve()

What does TRVE stands for? 
You won't know unless you call this method and get randomly selected words from band names.
*PS: Band names might be a bit rude & naughty.*

- [x] Able to get Random words in order, as String.
- [ ] Create **words** dataframes by itself.
    - Should be able to select distinct words starting with T, R, V, E.
- [ ] Generate names with other given letters.

### Python

`spotify_manager.py` provides methods for searching a single artist name and searching an artists albums. It is also capable of creating a mad+ itself. It can search through all artists mentioned in MAD and filter results that is in selected metal genres.

I also tried a little bit of fuzzy string matching, for matching band & album names but gave up on the idea. Uppercasing given names gets it done for now.

- [x] Search single artist
- [x] Search all artists into a csv file & dataframe
- [x] Search an artist's albums
- [ ] Search given album tracks
- [ ] Search given tracks' features

`trve kvlt only.`
