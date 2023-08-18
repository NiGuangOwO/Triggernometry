This document is a summary for my edited parts.

Check the main repo for Triggernometry documentations:
https://github.com/paissaheavyindustries/Triggernometry

# What's New

## MathParser
### Fixed the MathParser bugs about parsing minus signs: 
There were several bugs in the parsing logic about minus signs: 
1. The original code only examines the previous character to determine if a `+`/`-` is a positive/negative sign or a plus/minus sign. This ignores the signs before a space, so expressions like `func(1, -1)` or `1 - -1` were wrongly parsed. (Related: [#87](https://github.com/paissaheavyindustries/Triggernometry/issues/87))  
2. When the function `BasicArithmeticalExpression()` is applying a minus sign to a number, there was only a condition for positive values, and non-positive values were not treated. This caused expressions like `-(-1)` parsed into `-1`. (Related: [Discord](https://discord.com/channels/374517624228544512/1114692015163191316))  
3. The original code treats the minus sign as a special sign, which gives it a hidden priorty than any other operations. This caused wrong calculation order in some of the calculations, like `-2^2 = 4` (in most of the modern languages, the answer is -4).
4. The original code could not treat the `-` in `-func(args)` as a minus sign. This caused a program error in expressions like `0 = -sin(0)`. The code would try to apply a minus operation between `=` and `sin(0)`. (Related: [Discord](https://discord.com/channels/374517624228544512/1114692015163191316))  

The whole logic about +/- signs was rewritten to a much simpler version and the bugs were fixed.
### Fixed a condition check typo when parsing parenthesis.  
`char.IsDigit(...) || char.IsLetter(...)` was typed as `char.IsDigit(...) || char.IsDigit(...)`, which ignored the letter check when adding `*` before `(`.  
### Fixed a bug that mathparser not respecting alias.  
In the code, there was a list of aliases (like `atan2` => `arctan2`), but that part of code was actually not used. The unused codes were commented out, and the aliases were added directly into the list of functions.

## Arguments 
The original `SplitArgument` function resulted in incorrect `args` list when encountering unmatched quote or consecutive commas, and also did not respect linebreaks.    
The editted code now utilizes regular expressions to accurately extract all parameters located between the string's beginning, end, and commas.   
Unquoted expressions are trimmed; empty or unquoted whitespaces returns an empty list.  
_e.g._ (1,2,  3  ,"  4  ",   "5"  , "'", ', ', ) is now parsed into a list with the arguments:   
`1` `2` `3` `  4  ` `5` `'` `, ` `(empty)​`.  

## Indices and Slices
### Negative Indices
Indices now support negative values (counting backwards).  
Including: `substring`; `lvar`; `tvar`; `tvarrl`; `tvarcl`; the `index`/`row`/`column` textboxes of the list/table actions.  
The previous keyword "last" is redirected to -1.  
_e.g._ `${tvar:myTable[2][-3]}` gives the value in the `2nd` column and the `-3rd` row.  
### Slices
A slice expression like `start:end:step` could represent a series of indices starting from `start`, adding `step` every time, and ending **before** `end`.  
This expression works nearly the same as in Python, but the indices count from 1 for list / tables to keep consistent with previous Triggernometry features.  
**Slice** (and index) could combine to a **slices** expression, like: `":5, 7, 8:13:2, 16:"` means `1, 2, 3, 4, 7, 8, 10, 12, 16, 17, (...to the end)`  
Slices expressions are used in several new features (should use "" or '' to cover the expression if it contains comma).  

## Autofill
Fixed the bug that sometimes autofill is not hidden (like after entering `tvar:` and still showing `tvarrl`);  
Sorted and added several types of autofill, including list/table properties (also tried to get the list of var names and const keys but did not work, hope it could be fixed);  
The code will now find the previous unclosed `{` to give more precise autofill results;  
Increased the height and width of the autocomplete form.  

## Expressions and Functions
### Special Variables:
|Expression|Description|
|:---|:---|
|`_ETprecise`|Gives the precise minutes in the eorzean day.<br />The accurate version of `_ffxivtime` (`_ET`).|
|`_index`|Only available in the list action SetAll and SortByKey. <br />Represents the current index.|
|`_col`|Only available in the table action SetAll and SortCols. <br />Represents the current column index.|
|`_row`|Only available in the table action SetAll and SortRows. <br />Represents the current row index.|
|`_this`|Only available in the action SetAll (list/table) and SortByKey (list). <br />Represents the value in the current grid.|

### Numeric Constants:
|Expression|Description|
|:---|:---|
|`semitone`|`2^(1/12)`. <br />The frequency ratio between 2 adjacent semitones.|
|`cent`|`2^(1/1200)`. <br />The frequency ratio between 2 adjacent cents.|
|`ETmin2sec`|`35/12`. <br />The ratio between 1 ET minute and 1 real second.|

### Numeric Functions:
|Expression|Description|Examples|
|:---|:---|:---|
|`distance()`|Now supports 2 sets of _n_-dimensional coords.<br />Behaves the same as the previous version when _n_ = 2. |`distance(0,0,0, 3,4,12)` = `13`|
|`projectdistance()`<br />`projectheight()`|![proj](https://github.com/MnFeN/Triggernometry/assets/85232361/87d24efc-0d67-4d26-946a-81e91d3ba4c2)<br />_e.g._ Useful when doing calculations about linear AoE.|`projd(0,0, pi/6, -2,0)` = `-1`<br />`projh(0,0, pi/6, -2,0)` = `1.732...`|
|`angle(x1, y1, x2, y2)`|= `atan2(x2-x1, y2-y1)`|`angle(100, 100, 120, 100)` = `1.57...`|
|`relangle(θ1, θ2)`|Considering `θ1` as rel north, the direction of `θ2`. Normalized to `[-π, π)`.|`relangle(0, -pi/2)` = `1.732...`|
|`roundir(θ, ±n, digits = 0)`<br />`roundvec(x, y, ±n, digits = 0)`|Match the given direction (radian in `roundir`; dx/dy offsets in `roundvec`) to the direction in a circle divided into `\|n\|` segments, and returns the index of the direction.<br />The sign of `n` indicates 2 division modes: north is the segment point or the border of 2 segments, as shown below.<br />`digits` represents the number of decimal places for rounding; a negative value means no rounding.<br />![image](https://github.com/paissaheavyindustries/Triggernometry/assets/85232361/b7ab1f13-c5ba-4609-b588-b066d5d9d4e1)<br />_e.g._ Useful when calculating the direction of an entity with several possible spawnpoints. <br />Could combine with `func:pick(index)` and easily output any direction as a string from a radian / coordinate without complicated `arctan2` and `mod` calculations.|`roundir(-1.57,4)` = `1` (West)<br />`roundvec(8,-6,-4)` = `3` (NE)|

### Numeric String Functions:
|Expression|Description|Examples|
|:---|:---|:---|
|`parsedmg(hex)`|Parse the given hexstr damage/healing value in the `0x15`/`0x16` ACT loglines to the corresponding decimal value. <br />Rule: padleft the hexstr with `0` to 8 digits like `XXXXYYZZ`, then convert `ZZXXXX` to decimal.|`parsedmg(A00000)` = `160`|
|`freq(note, semitones = 0)`|returns the freq (Hz) of the given note + semitones offset.|`freq(A4)` <br />= `freq(G#4, 1)` <br />= `freq(Bb4, -1)` <br />= `freq(A5, -12)` <br />= `440`|

### String Functions:
|Expression|Description|Examples|
|:---|:---|:---|
|`parsedmg`|Same as numeric function. No arguments accepted.|`func:parsedmg:A00000`<br />= `160`|
|`slice(slices = "::")`|Accepts a slices expression as an argument.<br />Returns the slice of the string.|`func:slice(-3):01234` = `2`<br />`func:slice(1:4):01234` = `123`<br />`func:slice(::-1):01234` = `43210`<br />`func:slice("1,3:"):01234` = `134`|
|`pick(index, separator = ",")`|Separates the given string by the given separator.<br />Returns substring with the index counting from 0.<br />Also supports negative values.  |`func:pick(3):north,west,south,east`<br /> = `east`<br />`func:pick(-1,", "):1, 22, 3, 44, 5`<br /> = `5`|
|`replace(oldStr, newStr = "", isLooped = 0)`|Replace one string to another string in the given string.|`func:replace(" "):1 2 3`<br />= `123`<br />`func:replace(aa,a):aaaaaa`<br />= `aaa`<br />`func:replace(aa,a,1):aaaaaa`<br />= `a`|
|`repeat(times, joiner = "")`|Repeat the string with the given times.|`func:repeat(3):a` = `aaa`<br />`func:repeat(3, +):1` = `1+1+1`|
|`nextETms(XX:XX.xx)`<br />`nextETms(minutes)`|Returns the time (ms) left to the next given Eorzean time.|`nextETms(1:00)`<br />= `nextETms(60)`<br />= `175000`<br />(when current ET is `0:00`)|
|`padleft`<br />`padright`<br />`trim`<br />`trimleft`<br />`trimright`  |These functions now also accepts character arguments given as the character itself instead of only by its charcode.  <br />`0`-`9` would be considered as characters instead of charcodes since nobody would use those ASCII 0-9 control characters in these functions. <br />Numbers ≥ 10 are considered as charcodes.<br />No need for those 5-digit charcodes of CJK-region characters. (even full-width spaces) |`func:trim(48, 2, a):abcd0320`<br />= `bcd03`<br />`func:padleft(0,8):1ABCD`<br />= `0001ABCD`|

### List Variables:
This part uses the following **`lvar:test`** to demonstrate:  
|1|2|3|4|5|6|7|8|9|
|---|---|---|---|---|---|---|---|---|

|Expression|Description|Examples|
|:---|:---|:---|
|`sum(slices = "::")`|Returns the sum of (the slices of) the list. <br /> Only the values which could be parsed into `double` would be summed.|`${lvar:test.sum}` = `45`<br />`${lvar:test.sum(1:5)}` = `10`|
|`count(str, slices = "::")`|Returns the repeated times of the string in (the slices of) the list.|`${lvar:test.count(3)}` = `1`<br />`${lvar:test.count(a)}` = `0`|
|`join(joiner = ",", slices = "::"`)|Connects (the slices of) the list with the joiner.|`${lvar:test.join}`<br />= `1,2,3,4,5,6,7,8,9`<br />`${lvar:test.join(" ",5::-1)}`<br />= `5 4 3 2 1`|
|`randjoin(joiner = ",", slices = "::"`|Similar to join(), but the selected elements are shuffled before connected.|`${lvar:test.randjoin}`<br />= `4,9,2,3,5,7,8,1,6`<br />(random example)|

### Table Variables:
This part uses the following **`tvar:test`** to demonstrate:  
|11|21|31|41|
|---|---|---|---|
|12|22|32|42|
|13|23|33|43|
|14|24|34|44|

|Expression|Description|Examples|
|:---|:---|:---|
|`tvardl:` `ptvardl:`|Double-based lookup similar to `tvarrl:`/`tvarcl:` <br />Returns the value located by the column and row headers.|`${tvardl:test[41][13]}` = `43`|
|`hjoin(joiner1 = ",", joiner2 = "⏎", colSlices = "::", rowSlices = "::")`|Horizontally connects the table with the joiners.|`${tvar:test.hjoin(",",",",1:2,3:4)}`<br />= `13,23,14,24`<br />`${tvar:test.hjoin}` = <br />`11,21,31,41`<br />`12,22,32,42`<br />`13,23,33,43`<br />`14,24,34,44`|
|`vjoin(joiner1 = ",", joiner2 = "⏎", colSlices = "::", rowSlices = "::")`|Vertically connects the table with the joiners.|`${tvar:test.vjoin}` = <br />`11,12,13,14`<br />`21,22,23,24`<br />`31,32,33,34`<br />`41,42,43,44`|
|`hlookup(str, rowIndex, colSlices = "::")`|Looks for the string in the given row index and returns the column index.<br />Returns 0 if not found.|`${tvardl:test.hlookup(13,3)}` = `1`<br />`${tvardl:test.hlookup(13,3,2:)}` = `0`|
|`vlookup(str, rowIndex, colSlices = "::")`|Looks for the string in the given column index and returns the row index.<br />Returns 0 if not found.|`${tvardl:test.vlookup(13,1)}` = `3`|

### Job Properties:
`${_job[jobid].prop}`: returns the property of the given jobid. 
`${_job[XXX].prop}`: returns the property of the given job (3-letter abbrev). 
Properties: 
```
    role; (same as _ffxiventity)
    isT; isH; isTH; isD; isM; isR; isC; isG; isCG; (0 or 1)  
    jobCN; jobDE; jobEN; jobFR; jobJP; jobKR; (full names in different languages)  
    jobCN1; jobCN2; jobEN3; jobJP1 (abbrevations of different lengths)
```
These properties are also added to `_ffxiventity` and `_ffxivparty`.
_e.g._ `${_job[1].isT}` = `1`; `${_ffxiventity[Paladin Player].jobEN}` = `Paladin`

## Abbrevations for improving user experience:
|Full|Abbrev.|
|:---:|:---:|
|`${numeric:...}` |`${n:...}`| 
|`${string:...}` |`${s:...}`| 
|`${func:...}` |`${f:...}`| 
|`${_ffxiventity[...].prop}` |`${_entity[...].prop}`|
|`${_ffxivparty[...].prop}` |`${_party[...].prop}`| 
|`${_ffxivplayer}` |`${_me}`|
|`${_ffxiventity[${_ffxivplayer}].prop}` |`${_me.prop}`|
|`indexof()` |`i()`|
|`lastindexof()` |`li()`|
|`_ffxivtime` |`_ET`|
|`pi` |`π`|
|`distance()` |`d()`|
|`projectdistance()` |`projd()`|
|`projectheight()` |`projh()`|
|`angle()` |`θ()`|
|`relangle()` |`relθ()`|
|`sumslice()` |`sum()`|
|`joinslice()` |`join()`|
|`width` |`w`|
|`height` |`h`|
|`hlookup()` |`hl()`|
|`vlookup()` |`vl()`|

## Actions
### Fixed a bug in the list method `Insert`:
The original code inserted `null` as placeholders when the given index is longer than the length of the list (should use new `VariableScalar` instead).  
The parser could not get these null values in expressions; it also caused the list could not be double-clicked to view in the variable viewer (showing error from ACT).   

### Fixed a bug in the list method `Set`:
The original code inserted 1 less empty `VariableScalar` into the list as placeholders.    
It caused the program trying to set the value at the given `index` into the list with the length `index - 1` and failed.  

### Fixed a bug in the list method `Split`:  
The original code did not respect the persistent options of the source / target variables.   

### Added `Build` action for list/table variables:  
Build a list variable using the first 1 character of the expression as the separator, and the remained part as the given string. For table variable, using the first 2 characters as the col / row separator.    
Easily generates a list/table directly from a given string in a single action.  
Could also generate a list from the slice of another list or a row/column of a table in a single action, if combined with `list.join`, `table.hjoin`, `table.vjoin`.   
_e.g._ The expressions `,1,2,3,4,5,6,7,8,9` and `,|11,21,31,41|12,22,32,42|13,23,33,43|14,24,34,44` can build the previous `lvar:test` and `tvar:test`.  

### Added `SetAll` action for list/table variables:  
Set all elements in the list/table variable to the given value.  
`${_this}`, `${_index}` can be used in list variables;   
`${_this}`, `${_row}`, `${_col}` can be used in table variables.  
_e.g._ Applying the SetAll action with the expressions `${_index}` on a list (length = 9) can give the previous `lvar:test`.  

### Added `SetLine` / `InsertLine` action for table variables:  
Similar to the `Build` action for list variables, the expression is splitted into a list by its first character.  
Depending on which index (row/col) was given, the list of values would be set/inserted to the given row/col.  
The counting logic is the same as the `Set` / `Insert` actions of list variables.  
_e.g._ Applying the SetLine action with row index = `3` and expression = `,a,b,c,d,e` on the previous `lvar:test` gives:  
|11|21|31|41||
|---|---|---|---|---|
|12|22|32|42||
|a|b|c|d|e|
|14|24|34|44||

### Added `RemoveLine` action for table variables:  
Remove the row/column of the table.  
_e.g._ Removing row index = `3` from the previous `lvar:test` gives:  
|11|21|31|41|
|---|---|---|---|
|12|22|32|42|
|14|24|34|44|

### Added `SortByKeys` for lists, `SortRows` `SortCols` for tables:  
Using the given expressions as the sorting keys to sort the list / rows / columns.  
Expression format: `n+:key1, n-:key2, s+:key3, ...`  
`n`/`s`: numeric/string comparison  
`+`/`-`: ascending/descending (`+` could be omitted)  
`key`: should include `${_this}` / `${_index}` for lists, `${_row}` for row sorting, `${_col}` for column sorting.  
If the raw expression contains commas, or starts or ends with spaces, it should be quoted like `"s+:key", ...` or `'s+:key', ...`.  
_e.g._ Sorting the list `[11, 12, 13, 21, 22, 23, 31, 32, 33]` with the expression `n-:${f:substring(0):${_this}}, n+:${_index}%3` gives `[33, 31, 32, 23, 21, 22, 13, 11, 12]`.

### Added the folder action "Cancel the Actions of All Triggers In Folder"
Related issue: [#48](https://github.com/paissaheavyindustries/Triggernometry/issues/48)

### Sorted Actions
The actions, list actions and table actions were sorted to be more reasonable.

## Others
### Fixed the bug about string functions with no arguments:
Related issue: [#92](https://github.com/paissaheavyindustries/Triggernometry/issues/92)  
The original regex for string function could not parse `func:length:3*(1+2)` correctly, which considers `length:3*` as the function name and `1+2` as the argument.  
The regex was editted to solve this issue; it could now also match the whole expression in one step instead of parsing the `funcval` by searching the index of `:` later.  
(also some other small edits to the regexes)  
### Added support for linebreaks in expressions
Previously the linebreaks do not fully tolerate with splitting arguments, codes which contain trimming, and also regexes.  
A special character `⏎` was used as a placeholder for all linebreaks when parsing expressions, then replaced back after parsed.  
This character could also be used in expressions directly in Triggernometry, _e.g._ `${func:repeat(5, ⏎):text}`
### Improved Exception Messages
The exceptions in context.cs were unified, _e.g._ all argcount errors were combined by adding a function name placeholder to distinguish them.  
Also added more precise information like which expression caused error.  
### Improved CSV Export
Added support for table variables containing commas and double quotes. (Previously the grids were simply joint together with `,`)

## To-do List
- [ ] I18n (new / previous parts)    
