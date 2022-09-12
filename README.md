# TRVE
TRVE is a Data Engineering Project that fetches band names from Metal Archieves Dataset and collects all tracks it can find from Spotify API. Band names, genres, album & track information and track features are merged together in a single dataset. 

Scala file for data extraction, DataExtraction.scala, can be run with `spark-shell` at the moment. It will be turned into its own `.jar`, soon.

## Methods:

DataExtraction.scala provides:

### getMadPlus()

MAD stands for Metal Archieves Dataset, and Plus is for adding song genres to their relative columns.

- [x] Able to read M.A.D. repository files.
- [ ] Path is set with input.
- [ ] Option for auto-download dataset first.

### getRandomTrve()

What does TRVE stands for? 
You won't know unless you call this method and get randomly selected words from band names.
*PS: Band names might be a bit rude & naughty.*

- [x] Able to get Random words in order, as String.
- [ ] Create **words** dataframes by itself.
    - Should be able to select distinct words starting with T, R, V, E.
- [ ] Generate names with other given letters.

`trve kvlt only.`
