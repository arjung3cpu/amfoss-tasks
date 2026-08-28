# Task 02 – The Logbook of the Grand Line

## Level 1 – Loguetown Reef

### Objective

Find the genuine Devil Fruit among the many replicas in Loguetown Reef.

### Investigation

I first inspected the files inside the four sectors. The files all looked very similar, so I looked for a property that could distinguish one file from the others.

I used:

```bash
find sector_* -type f -name "devil_fruit_*.txt" -perm -111 -ls
```

This searches for Devil Fruit files that have executable permission.

The command identified only one executable file:

```text
sector_C/devil_fruit_6.txt
```

This matched the clue in the files that the true Devil Fruit still possesses the "freedom to change itself."

### Verification

I inspected the `eat.sh` script to understand how the suspected fruit should be tested:

```bash
cat eat.sh
```

The script showed that executable files are treated differently from the replicas.

I then ran:

```bash
./eat.sh sector_C/devil_fruit_6.txt
```

The fruit awakened and revealed:

```text
ONE_PIECE{GITO_GITO_NO_AWAKENING}
```

### Flag

```text
ONE_PIECE{GITO_GITO_NO_AWAKENING}
```

### Evidence

A screenshot of the `eat.sh` output showing the awakening and flag is saved as evidence for this level.

### Concepts Learned

* Linux file permissions
* Executable permission (`-x`)
* `find` command
* Bash scripts
* File inspection with `cat`
* Using clues from file metadata to investigate a problem


## Level 2 – Water 7

### Investigation

I entered the `Water_7/galley_la_company` directory and found a file named `puffing_tom_blueprints`.

The file initially appeared as unreadable binary data, so I identified its type using `file`. It was a gzip-compressed TAR archive.

I extracted the TAR archive and found:

```text
step1_blueprints.zip

### Historical Investigation

The current Water 7 files contained `PONEGLYPH_FRAGMENT_II`, but `PONEGLYPH_FRAGMENT_I` was not present in the current working files.

I searched the Git history and found Fragment I in commit `ee6f464`.

It was located in:

```text
GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log

## Level 2 – Whiskey Peak

### Investigation

I entered the `Whiskey_Peak` directory and found `feast_manifest.txt`. The visible file did not contain the expected transmission directly, so I investigated the Git branches and found a hidden vault script on the `whiskey_peak_investigation` branch.

I inspected the script without switching branches using:

```bash
git show origin/whiskey_peak_investigation:GrandLine/Whiskey_Peak/.baroque_works_cache/unlock_vault.sh

The script required the awakening signature from Level 1, so I exported:

```bash
export AWAKENING_SIGNATURE='ONE_PIECE{GITO_GITO_NO_AWAKENING}'

## Level 3 – The Wax Labyrinth of Little Garden

### Investigation

The current `Wax_Jungle` directory contained only a `.gitkeep` file, so I investigated the repository history instead of assuming the files were permanently missing.

The Level 3 instructions explained that the genuine report was associated with the Executive Transmission Code recovered at Whiskey Peak.

I searched the historical `little_garden` timeline and found the relevant report:

```text
GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log

### Historical Investigation

The current `Wax_Jungle` directory contained only a `.gitkeep` file, so I investigated the repository history instead of assuming the files were permanently missing.

The Level 3 instructions explained that the genuine report was associated with the Executive Transmission Code recovered at Whiskey Peak.

I searched the historical `little_garden` timeline and found the relevant report:

```text
Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log

The historical report contained:

```text
PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0LkzYqNyBsIS0vbTAtJTcnL"

### Clue

```text
KjY2MjF4bW0LkzYqNyBsIS0vbTAtJTcnL
```

### Concepts Learned

- Git branches
- Git history investigation
- `git show`
- Searching historical repository data
- Recovering information that is no longer present in the working tree

## Level 4 – The Camouflaged Blueprints of Water 7

### Investigation

The Water 7 directory contained a file named `puffing_tom_blueprints` with no useful file extension.

The level gave the clue:

> Names can be changed. True nature cannot.

So instead of trusting the filename, I identified the file type using:

```bash
file puffing_tom_blueprints


## Final Result

After investigating the different timelines and recovering the missing historical information, I restored the final inscription by resolving the merge conflicts in the final repository.

The two conflicting key parts were:

- `TheGrand` + `Line`
- `Remem` + `berS`

Combining them produced the final password:

```text
TheGrandLineRemembers

The final result was:

```text
Timeline Integrity .......... OK
Merge Conflict .............. Resolved
Repository .................. Restored
History ..................... Preserved
```

### Final Flag

```text
FLAG{The_Grand_Line_Remembers_Your_Commit}
```

### Concepts Learned

- Linux terminal commands
- File permissions
- Bash scripting
- Git branches and remote branches
- Git history and historical file recovery
- Archives and nested archives
- Base64 decoding
- SHA-256 verification
- File comparison with `diff`
- Merge conflicts and conflict resolution
- Preserving and reconstructing historical information
