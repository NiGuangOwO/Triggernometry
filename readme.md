This document is a summary for my edited parts since Triggernometry v1.1.7.3.  
  
Check the main repo for Triggernometry documentations:  
https://github.com/paissaheavyindustries/Triggernometry  
  
# What's New  
  
## MathParser  
The core of the MathParser had been mainly rewritten:  
### Parsing Minus Signs:  
Several bugs in the parsing logic for minus signs have been fixed:  
- The original code only checked the preceding character to determine if a `+`/`-` was a sign or an operator. This oversight caused incorrect parsing of expressions like `func(1, -1)` or `1 - -1`.
  - Related: [#87](https://github.com/paissaheavyindustries/Triggernometry/issues/87)  
- In the function `BasicArithmeticalExpression()`, only positive values were handled when applying a minus sign, neglecting non-positive values. This led to incorrect parsing of expressions like `-(-1)` into `-1`.
  - Related: [Discord](https://discord.com/channels/374517624228544512/1114692015163191316)  
- The original code gave the minus sign a hidden priority over other operations, leading to errors in the calculation order, such as `-2^2 = 4` (whereas the answer should be -4 in most modern languages).  
- The original code failed to recognize the `-` in `-func(args)` as a minus sign, causing errors in expressions like `0 = -sin(0)`. The code would attempt to apply a minus operation between `=` and `sin(0)`.
  - Related: [Discord](https://discord.com/channels/374517624228544512/1114692015163191316)   

These bugs have been fixed, and the entire logic for handling +/- signs has been rewritten for simplicity. Previously, special logic was used to treat `+`/`-` in both the lexer and the parser. Now, the lexer tokenizes every `+`/`-` without discrimination, leaving simple logic in the parser to handle them correctly.  
### Lexer Logic  
- The lexer has been simplified to focus only on whether the current character is part of an operator. It then separates operators from non-operator characters.  
- If the parser fails to parse a basic expression, it will throw an error detailing which operator in which expression could not be parsed.  
- The earlier lexer tried to add `*` between expressions like `3abs(0)`, but this approach was flawed. Distinguishing between `3a` in `3abs(0)` and the hex number `3ab` is not possible without scanning the entire list of functions to match names. Therefore, explicit `*` between numbers and functions/constants is still required.  
### Operators  
- The parser now supports unary, ternary, and right-associative operators, in addition to the previously supported single-character left-associative binary operators.  
- The following operators have been added:  
  - `&&` `||` `^^` `!`: logical AND / OR / XOR / NOT  
  - `%%` `//`: real `mod` and exact division  
  - `√`: sqrt()  
  - `>=` `<=` `==` `!=`  as aliases
  - `&` `|` `<<` `>>`: bitwise operations (useful for representing the state of multiple entities appearing in random locations using a single variable)  
  - `? :`: ternary operator  
### Precision Error Tolerance  
- The tolerance level has been changed from `double.Epsilon` to a constant (set to 1E-9), making it more suitable for Triggernometry use.  
- This rule only applies to functions and operators involving (explicit or implicit) comparisons, like `=` `>` `>=` `sign` `truncate`, etc.
- Values within the range `x ± tolerance` will be considered equal to `x` during comparisons.  
### Aliases  
- In the original code, a list of aliases (e.g., `atan2` => `arctan2`) existed but was not utilized.
- Those lines of code have been removed due to being incompatible with Triggernometry requirements, and the aliases have been directly incorporated into the list of functions.  
### Spaces  
- Spaces are now stripped from the expression before parsing to simplify the logic.  
- Side effect: Numerical string functions can no longer include meaningful spaces within their arguments (though this type of function was not previously supported).

## Arguments  
- The original `SplitArgument` function generated incorrect `args` lists when encountering unmatched quotes or consecutive commas, and it also failed to consider line breaks.  
- The edited code now employs regular expressions to precisely extract all parameters situated between the string's beginning, end, and commas.  
- Unquoted expressions are trimmed; empty or unquoted whitespaces return an empty list.  
- _e.g._ (1,2,  3  ,"  4  ",   "5"  , "'", ', ', ) now translates to a list with the arguments:  
- `1` `2` `3` `  4  ` `5` `'` `, ` `(empty)`.  
- Arguments should not contain `)` `{` `}` due to the parsing logic in expanding expressions, so the following escape rules apply:  

  + `{` should be escaped with full-width `｛` or `__LB__`;  
  + `}` should be escaped with full-width `｝` or `__RB__`;  
  + `(` can be escaped with full-width `（` or `__LP__`;  
  + `)` should be escaped with full-width `）` or `__RP__`;  
  + `｛` `｝` should be escaped with `__FLB__` `__FRB__`;  
  + `（` `）` should be escaped with `__FLP__` `__FRP__`;  

## Indices and Slices  
### Negative Indices  
- Indices now support negative values, counting backwards.  
- This includes: `substring`; `lvar`; `tvar`; `tvarrl`; `tvarcl`; and the `index`/`row`/`column` text boxes in list/table actions.  
- The previous keyword "last" now redirects to -1.  
- _e.g._ `${tvar:myTable[2][-3]}` returns the value in the `2nd` column and the `-3rd` row.  
### Slices  
- A slice expression like `start:end:step` can represent a series of indices starting from `start`, incrementing by `step` each time, and ending **before** `end`.  
- This functionality closely resembles Python's slicing mechanism.  
- All three integers can be omitted: `a:b:c` `a:b:` `a::c` `:b:c` `a::` `:b:` `::c` `::` `a:b` `a:` `:b` `:`  
- Indices support negative values; strings count from 0 and lists/tables count from 1, maintaining consistency with previous Triggernometry features.  
- **Slices** (and indices) can be combined into a **slices** expression, such as: `":5, 7, 8:13:2, 16:"` represents `(0), 1, 2, 3, 4, 7, 8, 10, 12, 16, 17, (...to the end)`.  
- Slice expressions are now commonly used in new features to combine multiple functions, enable "fake" higher-dimensional list/table operations in string expressions, and also to simplify expressions/actions without using loops.  
- Note: "slices" is considered a single argument in functions and methods. If it contains a comma, enclose the slices expression in `""` or `''`.  

## Autofill  
- Fixed a bug where autofill sometimes remained visible, such as after entering `tvar:` and still showing `tvarrl`;  
- Added more types of autofill: list/table/dict methods; current variable/aura/const names; regex capture groups in the current trigger; dict keys and table lookup headers;  
- The code now searches for the preceding unclosed `{` to provide smarter autofill suggestions; (e.g., `${lvar:xxx${var:yyy}${index}.` will display list properties);  
- The autofill box now appears directly below the matched strings;  
- Fixed a bug where using the enter key to select an autofill suggestion in multi-line mode also inserted a line break;  
- Increased the height (5 → 10) and width (→ max length of suggestions) of the autocomplete box;  
- Added a debounce timer: a 200 ms countdown starts after text changes in the textbox and triggers the autofill logic. Any changes within this countdown reset the timer, preventing lag when typing quickly or holding backspace.  

## Dictionary Variables  
- Finalized the definition of the previously unused VariableDictionary type and added corresponding expressions, methods, and actions.  
- See below for details.  
  
## Expressions and Functions  
### Special Variables:  
|Expression|Description|  
|:---|:---|  
|`_ETprecise`|Provides the exact minutes in the Eorzean day.<br />A more accurate version of `_ffxivtime` (`_ET`).|  
|`_idx`|Dynamic expression. Represents the current index.|  
|`_col`|Dynamic expression. Represents the current column index.|  
|`_row`|Dynamic expression. Represents the current row index.|  
|`_col[i]`|Dynamic expression. Represents the value in the row index `i` and the current column.|  
|`_row[i]`|Dynamic expression. Represents the value in the column index `i` and the current row.|  
|`_this`|Dynamic expression. Represents the value in the current grid.|  
|`_key` <br />`_val`|Dynamic expression. Represents the current key/value.|  
|`_clipboard`|Current copied text in the system clipboard.|  

For details on dynamic expressions, refer to the actions section.

### Numeric Constants:  
|Expression|Description|  
|:---|:---|  
|`semitone`|`2^(1/12)`. <br />The frequency ratio between 2 adjacent semitones.|  
|`cent`|`2^(1/1200)`. <br />The frequency ratio between 2 adjacent cents.|  
|`ETmin2sec`|`35/12`. <br />The ratio between 1 ET minute and 1 real second.|  

### Numeric Functions:  
|Expression|Description|Examples|  
|:---|:---|:---|  
|`distance()`|Now supports 2 sets of _n_-dimensional coordinates.<br />Behaves the same as previous versions when _n_ = 2.|`distance(0,0,0, 3,4,12)` = `13`|  
|`projectdistance()`<br />`projectheight()`|![proj](https://github.com/MnFeN/Triggernometry/assets/85232361/87d24efc-0d67-4d26-946a-81e91d3ba4c2)<br />_e.g._ Useful for calculations involving linear AoE.|`projd(0,0, pi/6, -2,0)` = `-1`<br />`projh(0,0, pi/6, -2,0)` = `1.732...`|  
|`angle(x1, y1, x2, y2)`|= `atan2(x2-x1, y2-y1)`|`angle(100, 100, 120, 100)` = `1.57...`|  
|`relangle(θ1, θ2)`|Considering `θ1` as relative north, it returns the direction of `θ2`. Normalized to `[-π, π)`.|`relangle(0, -pi/2)` = `1.57...`|  
|`roundir(θ, ±n, digits = 0)`<br />`roundvec(x, y, ±n, digits = 0)`|Matches the given direction (in radians for `roundir`; dx/dy offsets for `roundvec`) to a direction in a circle divided into `\|n\|` segments, then returns the index of that direction.<br />The sign of `n` indicates two division modes: north as a segment point or as a boundary between two segments, as shown below.<br />`digits` specifies the number of decimal places for rounding; a negative value means no rounding.<br />![image](https://github.com/paissaheavyindustries/Triggernometry/assets/85232361/b7ab1f13-c5ba-4609-b588-b066d5d9d4e1)<br />_e.g._ Useful for calculating the direction of an entity with multiple potential spawn points. Could be combined with `func:pick(index)` to easily output any direction as a string from radians or coordinates without complex `arctan2` and `mod` calculations.|`roundir(-1.57,4)`<br /> = `1` (West)<br />`roundvec(8,-6,-4)`<br /> = `3` (NE)|  

### Numeric String Functions:  
|Expression|Description|Examples|  
|:---|:---|:---|  
|`parsedmg(hex)`|Converts the given hex string for damage/healing in the `0x15`/`0x16` ACT log lines to the corresponding decimal value.<br />Rule: Padleft the hex string with `0`s to 8 digits as `XXXXYYZZ`, then convert `ZZXXXX` to decimal.|`parsedmg(A00000)` = `160`|  
|`freq(note, semitones = 0)`|Returns the frequency (Hz) of the specified note (using scientific pitch notation, accidentals represented as `#`, `b`, `x`) adjusted by the semitones offset.|`freq(A4)` <br />= `freq(G#4, 1)` <br />= `freq(Bb4, -1)` <br />= `freq(A5, -12)` <br />= `440`|
|`nextETms(XX:XX)` `nextETms(ETminutes)`|Provides the time (ms) remaining until the next specified Eorzean time.|`nextETms(2:00)`<br />= `nextETms(02:00.00)`<br />=`nextETms(120)`<br />= `175000`<br />(assuming the current ET is `1:00`)|

  
### String Functions:  
|Expression|Description|Examples|  
|:---|:---|:---|  
|`parsedmg`|Same as the numeric function. No arguments accepted.|`func:parsedmg:A00000`<br />= `160`|  
|`slice(slices = ":")`|Accepts a "slices expression" as an argument.<br />Returns the specified slice of the string.|`func:slice(-3):01234` = `2`<br />`func:slice(1:4):01234` = `123`<br />`func:slice(::-1):01234` = `43210`<br />`func:slice("1,3:"):01234` = `134`|  
|`pick(index, separator = ",")`|Separates the given string by the specified separator.<br />Returns a substring based on the index, starting from 0.<br />Also supports negative indices.|`func:pick(3):north,west,south,east`<br /> = `east`<br />`func:pick(-1,", "):1, 22, 3, 44, 5`<br /> = `5`|  
|`contain(str)`<br />`startwith(str)`<br />`endwith(str)`<br />`equal(str)`|Returns `1` or `0`.|`func:contain(23):1234` = `1` <br />`func:endwith(23):1234` = `0`<br />`func:equal(23):1234` = `0`|  
|`ifcontain(str, t, f)`<br />`ifstartwith(str, t, f)`<br />`ifendwith(str, t, f)`<br />`ifequal(str, t, f)`|Similar to `if()`.|`func:ifcontain(23, a, b):1234` = `a` <br />`func:ifendwith(23, a, b):1234` = `b`<br />`func:ifequal(23, a, b):1234` = `b`|  
|`indicesof(str, joiner = ",", slices = ":")`|Searches for all indices in the specified slices of the string, then joins them.|`func:indicesof(a):abcbabcba` = `0,4,8`<br />`func:indicesof(a, "-", ::-1):abcbabcba` = `8-4-0`|  
|`match(str):regex`|Returns `1` or `0`.<br />Note: `regex` should not contain `{` `}`.<br />`{` should be escaped with full-width `｛` or `__LB__`;<br />`}` should be escaped with full-width `｝` or `__RB__`;<br />`｛` `｝` must be escaped with `__FLB__` `__FRB__`.<br />Same regex rules apply to the next two functions.|`func:match(404D):404[B-D]` = `1`<br />`func:match(4000A3BF):4.｛7｝` = `1`|  
|`capture(str, group):regex`|Returns the captured string `$groupindex` or `${groupname}`. If `groupindex` = `0`, it returns the entire matched string. <br />If `groupname` isn't found or `groupindex` is out of range, it returns an empty string.<br />Adheres to the previously mentioned regex rules.|`func:capture(Player NameGilgamesh, server):.+ .+(?<server>[A-Z].+)`<br />= `Gilgamesh`|  
|`ifmatch(str, t, f):regex`|Similar to `if()`.|`func:match(404D, a, b):404[B-D]` = `a`|  
|`replace(oldStr, newStr = "", isLooped = 0)`|Replaces one string with another in the specified string.|`func:replace(" "):1 2 3`<br />= `123`<br />`func:replace(aa,a):aaaaaa`<br />= `aaa`<br />`func:replace(aa,a,1):aaaaaa`<br />= `a`| 
|`repeat(times, joiner = "")`|Repeats the string the specified number of times.|`func:repeat(3):a` = `aaa`<br />`func:repeat(3, +):1` = `1+1+1`|  
|`padleft`<br />`padright`<br />`trim`<br />`trimleft`<br />`trimright`  |These functions now accept character arguments either as the character itself or its charcode. <br />`0`-`9` are interpreted as characters rather than charcodes since ASCII 0-9 control characters are rarely used here. <br />Numbers ≥ 10 are seen as charcodes.<br />No need for the 5-digit charcodes of CJK-region characters (including full-width spaces).|`func:trim(48, 2, a):abcd0320`<br />= `bcd03`<br />`func:padleft(0,8):1ABCD`<br />= `0001ABCD`|  

  
### List Variables:  
- This section uses **`lvar:test` = `1, 2, 3, 4, 5, 6, 7, 8, 9`** (this string is only a representation of the list) for demonstration.  

|Expression|Description|Examples|  
|:---|:---|:---|  
|`${?lvar:...}`|Builds a temporary list directly from the expression split by `,`, and uses any properties on it to return a string.<br />Uses the same splitting rule as for splitting arguments.<br />Building a variable might be slightly slower, but it provides a way to combine multiple actions with conditions into a single action. |`${?lvar:a, b, c, d, e.indexof(c)}` = `3`<br />`${?lvar:a, b, "c,c", d, e[3]}` = `c,c`|
|`sum(slices = ":")`|Returns the sum of the values in (the slices of) the list. <br />Only values that can be parsed into the `double` format are summed.|`${lvar:test.sum}` = `45`<br />`${lvar:test.sum(1:5)}` = `10`|  
|`count(str, slices = ":")`|Returns the number of times the string appears in (the slices of) the list.|`${lvar:test.count(3)}` = `1`<br />`${lvar:test.count(a)}` = `0`|  
|`join(joiner = ",", slices = ":")`|Joins (the slices of) the list using the specified joiner.|`${lvar:test.join}` = `1,2,3,4,5,6,7,8,9`<br />`${lvar:test.join(" ",5::-1)}`<br />= `5 4 3 2 1`|  
|`randjoin(joiner = ",", slices = ":")`|Similar to join(), but the selected elements are shuffled before being joined..|`${lvar:test.randjoin}`<br />= `4,9,2,3,5,7,8,1,6`<br />(random example)|  
|`contain(str, slices = ":")`|Returns 1 if (the slices of) the list contains the given string, otherwise 0.|`...contain(3)` = `1` <br />`...contain(3, 4:)` = `0`|  
|`ifcontain(str, trueExpe, falseExpr)`|Similar to `if()`. If the list contains the string, returns `trueExpe`; otherwise, returns `falseExpr`.|`...ifcontain(3, found, missing)` = `found` <br />`...ifcontain(a, found, missing)` = `missing`|  
|`indicesof(str, joiner = ",", slices = ":")`|Searches for all occurrences of the string in the given slices of the list and joins the indices into a string. Similar to the string function.||
|`max(type = "n", slices = ":")` <br /> `min(type = "n", slices = ":")`|Returns the extremum value in (the slices of) the list, depending on the type: `n` for numeric, `h` for hex, `s` for string.|`${lvar:test.max}` = `9` <br />`...min(n, 3:)` = `3`|  

### Table Variables:  
- This section demonstrates using the following **`tvar:test`**:

|11|21|31|41|  
|---|---|---|---|  
|12|22|32|42|  
|13|23|33|43|  
|14|24|34|44|

|Expression|Description|Examples|  
|:---|:---|:---|  
|`${?tvar:...}`|Builds a temporary table directly from the expression split by `,` and `|`.<br />Similar to `${?lvar:}`. |`${?tvar: a,b | c,d [2][2]}` = `d`|
|`tvardl:` `ptvardl:`|Double-based lookup similar to `tvarrl:`/`tvarcl:`. <br />Returns the value identified by the column and row headers.|`${tvardl:test[41][13]}` = `43`|  
|`sum(colSlices = ":", rowSlices = ":")`|Returns the sum of the values in (the sliced rows and columns of) the table. <br />Only values that can be parsed into the `double` format are summed.|`${lvar:test.sum}` = `440`<br />`...sum(1, :)`<br />= `11 + 12 + 13 + 14`<br />= `50`|  
|`count(str, colSlices = ":", rowSlices = ":")`|Returns the number of times the string appears in (the sliced rows and columns of) the table.|`${lvar:test.count(33)}` = `1`<br />`${lvar:test.count(1)}` = `0`|  
|`hjoin(joiner1 = ",", joiner2 = "⏎", colSlices = ":", rowSlices = ":")`|Horizontally joins the table using the specified joiners.|`...hjoin(",", ",", 1:3, 3:)`<br />= `13,23,14,24`<br />`${tvar:test.hjoin}` = <br />`11,21,31,41`<br />`12,22,32,42`<br />`13,23,33,43`<br />`14,24,34,44`|   
|`vjoin(joiner1 = ",", joiner2 = "⏎", colSlices = ":", rowSlices = ":")`|Vertically joins the table using the specified joiners.|`${tvar:test.vjoin}` =  <br />`11,12,13,14`<br />`21,22,23,24`<br />`31,32,33,34`<br />`41,42,43,44`|  
|`hlookup(str, rowIndex, colSlices = ":")`|Searches for the string in the given row and returns the column index.<br /> If not found, returns 0.|`...hlookup(13,3)` = `1`<br />`...hlookup(13,3,2:)` = `0`|  
|`vlookup(str, colIndex, rowSlices = ":")`|Searches for the string in the given column and returns the row index.<br /> If not found, returns 0.|`...vlookup(13,1)` = `3`|  
|`max(type = "n", colSlices = ":", rowSlices = ":")` <br /> `min(type = "n", colSlices = ":", rowSlices = ":")`|Same as the list method.|(omitted)|  
  
### Dict Variables:
- This part uses **`dvar:test` = `a=1, b=2, c=3, d=3, e=3`** (this string is only a representation of the dictionary) to demonstrate:  
|Expression|Description|Examples|
|:---|:---|:---|
|`${?dvar:...}`|Builds a temporary dict directly from the expression split by `=`, `.`.<br />Similar to `${?lvar:}`.|`${?dvar: 7CD2=in, 7CD6=out, 7CD7=spread [7CD2] }` = `in`|
|`sumkeys()` `sum()`|Sum all the keys/values that can be parsed into `double` format.|`${dvar:test.sumkey}` = `0`<br />`${dvar:test.sum}` = `12`|
|`count(value)`|Returns the count of the given value in the dict.|`...countvalue(3)` = `3`|
|`dvar:` `edvar:`<br />`pdvar:` `epdvar:`|e (existing) / p (persist). Similar to other variables.| `${epdvar:dictname}`<br />`${dvar:test[e]}` = `3` |
|`length` / `size`|The number of keys in the dict.| `${dvar:test.size}` = `5` |
|`ekey(key)` `evalue(value)`|Check if the key/value exists in the dict (returns 0/1).| `${dvar:test.ekey(a)}` = `1`<br />`${dvar:test.evalue(4)}` = `0` |
|`ifekey(key, t, f)`<br />`ifevalue(value, t, f)`|Similar to string functions (returns string t/f).| `...ifekey(a, found, missing)` = `found` |
|`keyof(value)`|Reverse lookup by value. Returns the first found key or an empty string if not found.| `${dvar:test.keyof(1)}` = `a`<br />`${dvar:test.keyof(4)}` = `` |
|`keysof(value, joiner = ",")`|Lookup all keys matching the given value and join them with the joiner.| `...keyof(3)` = `c,d,e`|
|`joinkeys(joiner = ",")`<br />`joinvalues(joiner = ",")`<br />`joinall(kvjoiner = "=", pairjoiner = ",")`|Combine the keys/values/both using the joiners.|`...joinkeys(-)` = `a-b-c-d-e`<br />`...joinall` = `a=1,b=2,c=3,d=3,e=3`|
|`max(type = "n")` <br /> `min(type = "n")`<br />`maxkey(type = "n")` <br /> `minkey(type = "n")`|Same as the list methods.|(omitted)|

### Job Properties:
- `${_job[XXX].prop}`: returns the property of the specified job.  
- Properties:  
```  
    role; job; jobid (same as _ffxiventity)  
    isT; isH; isTH; isD; isM; isR; isTM; isHR; isC; isG; isCG; (0 or 1)  
    jobCN; jobDE; jobEN; jobFR; jobJP; jobKR; (full names in different languages)    
    jobCN1; jobCN2; jobEN3 (= job); jobJP1 (abbreviations of varying lengths)  
```  
- `jobXX`, `jobXXn`, `jobid` could be used as the key `XXX` in `${_job[XXX].prop}`.  
- These properties are also included in `_ffxiventity` and `_ffxivparty`.  
- _e.g._   
  - `${_job[Gladiator].jobid}` = `1`;    
  - `${_job[1].jobFR}` = `Gladiateur`;    
  - `${_job[GLA].jobCN1}` = `剑`;    
  - `${_ffxiventity[Gladiator Player].isTM}` = `1`   
  
### Entity Properties:  
- Several entity properties have been added to `${_ffxiventity}` and `${_ffxivparty}`:  
  - `bnpcid`, `bnpcnameid`, `ownerid`, `type`,  
  - `castid`, `casttime`, `maxcasttime`, `iscasting`  
  
## Abbreviations to Enhance User Experience:
- Expressions can become extremely long when working with complex logic, which may involve several nested `${}` instances.
- To alleviate this, several abbreviations have been introduced to shorten these expressions:
|Full|Abbrev.|  
|:---:|:---:|  
|`${numeric:...}` |`${n:...}`|  
|`${string:...}` |`${s:...}`|  
|`${func:...}` |`${f:...}`|  
|`${exvar:...}` | `${ev:}` `${el:}` `${et:}` `${ed:}` |  
|`${(p)var:...}` `${(p)lvar:...}` <br />`${(p)tvar:...}` `${(p)dvar:...}` | `${(p)v:}` `${(p)l:}` <br />`${(p)t:}` `${(p)d:}` |  
|`${?lvar:...}` `${?tvar:...}` `${?dvar:...}` | `${?l:}` `${?t:}` `${?d:}` |  
|`${_ffxiventity[...].prop}` |`${_entity[...].prop}`|  
|`${_ffxivparty[...].prop}` |`${_party[...].prop}`|  
|`${_ffxivplayer}` |`${_me}`|  
|`${_ffxiventity[${_ffxivplayer}].prop}` |`${_me.prop}`|  
|`indexof()` |`i()`|  
|`_ffxivtime` |`_ET`|  
|`pi` |`π`|  
|`distance()` |`d()`|  
|`projectdistance()` |`projd()`|  
|`projectheight()` |`projh()`|  
|`angle()` |`θ()`|  
|`relangle()` |`relθ()`|  
|`.width` |`.w`|  
|`.height` |`.h`|  
|`.hlookup()` |`.hl()`|  
|`.vlookup()` |`.vl()`|  
|`.heading` |`.h`|  
  
## Actions  
### Fixed a bug in the list method `Insert` and table variable `Resize`:  
- The original code for the list variable inserted `null` directly as placeholders when the given index exceeded the length of the list. It should have used a new `VariableScalar` instead.  
- This led to two issues: the parser was unable to retrieve these null values in expressions, and the list couldn't be double-clicked to view in the variable viewer due to an ACT error.  
- Similarly, the code for table variables appended empty rows, setting each grid to `null`:   
  - `vtr.Values.AddRange(new Variable[newWidth]);`  
  - `Rows[i].Values.AddRange(new Variable[newWidth - Rows[i].Values.Count]);`  
  
### Fixed a bug in the list method `Set`:  
- The original code inserted one fewer `VariableScalar` into the list as placeholders.   
- This caused a problem when trying to set a value at a given `index` in a list with length `index - 1`. The result was an appended list that lacked the value to be set.  
  
### Fixed a bug in the list method `Split`:  
- The original code did not adhere to the persistent options of the source/target variables.   
  
### Updated `PopFirst` / `PopLast` actions for list variables:  
- `PopFirst` was modified to accept an optional `index` argument, which also supports negative values.  
- The action name `PopFirst` in the code remained unchanged, and `PopLast` was retained for XML compatibility reasons.
- However, the functionality of `PopLast` now redirects to `PopFirst` with index = `-1`.

### Added `PopToList` actions (set/insert):
- Pop and insert
  - Pops an element from the source list and inserts it into the target list.
  - If the target index was not given, it would be appended to the end of the list.
  - Note: this is not the same as index `-1`, which inserts the value between the last 2 elements
  - _e.g._ source list: `1,2,3,4,5`, source index: `3`, target list: `a,b,c,d,e`
    - target index: `3` => `a,b,3,c,d,e`;
    - target index: `-1` => `a,b,c,d,3,e`;
    - target index: ` ` => `a,b,c,d,e,3`;
- Pop and set
  - Pops a element and set it to the given index in the target list.
  - Both of the indices should be given.
  - _e.g._ other conditions same as above;
    - target index: `3` => `a,b,3,d,e`;
    - target index: `-1` => `a,b,c,d,3`;
- These actions are just combinations of `Pop` and `Set`/`Insert`.
- The `expression` textbox is used as the target index input, and the descriptions and label instructions would be changed automaticlly.
  
### Added basic actions for dict variables:  
- `Unset`, `UnsetAll`, `UnsetRegex`  
- `Set`: Assigns a value to a key.  
- `Remove`: Removes a specified key if it exists.  
- `Merge`: Combines dictionaries but leaves repeated keys unaltered.  
- `MergeHard`: Combines dictionaries and overwrites any repeated keys.  
  
### Added `Build` action for list/table/dict variables:  
- Build a list variable by using the first character of the expression as the separator, with the remainder of the expression as the input string. For table variables, the first two characters serve as the column/row separators. For dict variables, the first two characters act as the key-value pair separator and the overall pairs separator.  
- This allows for the easy creation of lists/tables directly from a given string with a single action.  
- Further, one can generate a list from a slice of another list or a row/column of a table in a single step when combined with `list.join`, `table.hjoin`, or `table.vjoin`.   
- _e.g._ The expressions `,1,2,3,4,5,6,7,8,9` and `,|11,21,31,41|12,22,32,42|13,23,33,43|14,24,34,44` can build the previous `lvar:test` and `tvar:test`;  
`=,a=1,b=2,c=3` can build the dictionary `a=1, b=2, c=3`.  
### Added `SetAll` action for list/table/dict variables:  
- Provides a flexible method to assign values to a list/table/dict variable, similar to the `Select()` in LINQ expressions.  
- The dynamic expressions below can be utilized when traversing the entire variable:  
  - List variables: `${_this}` `${_idx}`  
  - Dict variables: `${_idx}` (when a dict length is specified) or `${_key}` `${_val}`  
- For table variables: `${_this}`, `${_row}`, `${_col}` can be used.
- _e.g._
  - Using the SetAll action with the expression `${_idx}` on a list (length = 9) produces `lvar:test` with values (1-9);  
  - Then, using SetAll with the expression `${_this}^2` on `lvar:test` results in `1, 4, 9, ..., 81`.  
  - For a dictionary of length `5`, using key expression `${_idx}` and value expression `${_idx}^2` produces a dictionary `1:1, 2:4, 3:9, 4:16, 5:25`.
  - Applying the key expression `${_value}` and value expression `${_key}` reverses it to `1:1, 4:2, 9:3, 16:4, 25:5`.  

### Added `Filter` action for list/table/dict variables:  
- This is similar to the `Where()` function in LINQ expressions.  
- Filters elements of a list to a new list, grids of a table to a new list, rows/columns of a table to a new table, or key-value pairs of a dict to a new dict, based on whether the dynamic expression evaluates to true (`!= 0`).  
- For example, the expression `${func:ifequal("", 0, 1):${_this}}` eliminates empty elements;  
- `${lvar:listname.indexof(${_this})} = ${_idx}` removes duplicate elements in the list named `listname`;  
- Using the expression `${_ffxiventity[${_this}].distance} > 15 && ${func:ifequal(DPS):${_ffxiventity[${_this}].role}}` on a list containing player names filters out DPSs located more than 15 m away from the player.  

### Added `SetLine` / `InsertLine` action for table variables:  
- Similar to the `Build` action for lists, it splits the expression into a list based on its first character. Depending on the provided index (row/col), the list of values is then set/inserted into the specified row/col. This counting - - logic is similar to that of the `Set` / `Insert` actions for list variables.  
- _e.g._ Using the SetLine action with a row index of `3` and the expression `,a,b,c,d,e` on the prior `lvar:test` yields:  
|11|21|31|41||  
|---|---|---|---|---|  
|12|22|32|42||  
|a|b|c|d|e|  
|14|24|34|44||  

### Added `RemoveLine` action for table variables:  
- This action removes a specified row/column from a table.  
- For instance, removing row index `3` from the previous `lvar:test` results in:  
|11|21|31|41|  
|---|---|---|---|  
|12|22|32|42|  
|14|24|34|44|  

### Added `SortByKeys` for lists, and `SortLine` for tables:  
- These actions sort based on the specified key expressions, proving useful for scenarios involving multi-criteria sorting, such as in TOP dynamis.  
- Expression format: `n+:key1, n-:key2, s+:key3, ...`  
  - `n`/`s`: numeric/string comparison  
  - `+`/`-`: ascending/descending (the `+` is optional)  
  - `key`: should include `${_this}` / `${_idx}` for lists, `${_row}` or `${_row[i]}` for row sorting, `${_col}` or `${_col[i]}` for column sorting.  
- If an expression contains commas, or starts/ends with spaces, it should be enclosed in quotes, like `"s+:key", ...` or `'s+:key', ...`. _e.g._  
  - `n+:${_this}` `n-:${_this}` `s+:${_this}` `s-:${_this}` correspond to the previous four sorting actions.  
  - Sorting by `n-:${_idx}` reverses the list.  
  - Sorting the list `[11, 12, 13, 21, 22, 23, 31, 32, 33]` with the expression `n-:${f:substring(0):${_this}}, n+:${_idx}%3` produces `[33, 31, 32, 23, 21, 22, 13, 11, 12]`.  

### Unset all types of variables matching the regex (in the scalar variable tabpage)
- This will unset the scalar, list, table, dictionary variables in one step.
- The persistant option is still respected: unsetting the session vars would not affect persistent vars.
- Useful when initiating a raid phase.

### Copy the Value of the Variable/Expression to the Clipboard (in the Scalar Variable Tabpage)
- If the variable name is provided, its value will be copied directly to the clipboard without any parsing.
- If only an expression is provided, it will be interpreted as a string expression and then copied to the clipboard.
- Note: In practice, this doesn't necessarily involve scalar variables. To set a scalar variable to the clipboard, you can simply input `${var:name}` in the expression (unless your clipboard contains `${...}` expressions). I have organized it this way just to logically group this clipboard operation under the scalar variable category, avoiding the creation of a separate tabpage which could further slow down the action form loading.

### Introduced the folder action "Cancel All Actions of Triggers Within Folder"  
- Related issue: [#48](https://github.com/paissaheavyindustries/Triggernometry/issues/48)  

### Refined Actions List  
- Reorganized the actions, list actions, and table actions into a more logical sequence. Additionally, replaced several opTypes that were hardcoded as integers with their corresponding enums.
  
## Trigger Form / Action Viewer  
- Added arguments to represent if the variable is persistent and if the expression is numeric/string in the action descriptions (and also log messages);   
- Added a `[Sync]` prefix to the description if the async option of an action is unchecked;  
- Added a warning color when an action has a non-zero delay and the description text is overridden (this usually happens as a mistake when copying and editing actions, and it is hard to debug);  
- Added color options in the action description page to allow customized bg/text colors in the descriptions;  (format: `Lavender` / `230,230,250` / `#e6e6fa` / `#eef`)  
- Added a `Color` ExpressionType enum to let the textbox show the input as its background color;  
- Added the buttons `Move to top` and `Move to bottom`, and enabled the moving of multiple selected actions;  
- Added the button `Undo` to enable the undo of movement / delete of actions for one step;  
- `Add action` now insert the action under the selected line instead of set it to the bottom;   
- `Save changes` button would change into `Save and Fire` if autofire is enabled;  
- Added a trigger description label on the bottom showing some info about conditions, source, refire options, sequential, etc;  
- Added a message box to confirm quiting without saving the trigger;  
- Deselect the action rows when clicking elsewhere.  

## Log Form
- Added more precise error information in the logs like which expression caused error when expanding expressions;  
- Added a `custom` log type (`info` < `custom` < `warning`) which should contain no log from the program.   
- Adjusted the `warning` / `error` log message colors to be less saturated instead of pure red/yellow, and also added a green color to the `custom` logs.   
- Use checkboxes instead of comboboxes to filter logs, which is much clearer:   
<img src="https://github.com/MnFeN/Triggernometry/assets/85232361/76de6fa8-2596-4ebf-b538-296749bca3d4" width="200">

## Variable State Viewer / Editor
Added support for dictionary variables;  
Added support for sorting the 8 types of variables by clicking their corresponding dgv table headers;
Let the selected grid move to the next column / row after adding a column / row. (not changed for inserting);
Fixed the bug that some columns could not be adjusted in variable state viewer: some columns were set to `Fill`, which forbids the adjustment of its column width if it is not the last column.   

## Others

### Bug Fixes:

- **Func Without Parameters**: Fixed an issue where string functions without arguments weren't parsed correctly.
  - **Related Issue**: [#92](https://github.com/paissaheavyindustries/Triggernometry/issues/92)
  - The original regex misinterpreted expressions like `func:length:3*(1+2)`, which considers `length:3*` as the function name and `1+2` as the argument.  
  - Modifications to the regex now allow it to correctly match the entire expression in a single step.
  - The regular expressions also underwent minor adjustments.

- **Hi-Res Action Checkboxes**: Rectified a bug causing action checkboxes to remain hidden on Hi-Resolution screens.
  - **Related Issue**: [#91](https://github.com/paissaheavyindustries/Triggernometry/issues/91)

- **MessageBox Display**: Addressed an issue causing the MessageBox to sometimes hide behind active windows. Now, MessageBoxes will always appear above the currently active window.

### Enhancements:

- **Linebreaks in Expressions**: 
  - Improved support for linebreaks which previously conflicted with argument splitting, code trimming, and regular expressions.
  - A special character `⏎` was introduced to act as a placeholder for linebreaks during parsing, which is replaced post-parse.
  - This character can also be used directly in Triggernometry expressions, for instance, `${func:repeat(5, ⏎):text}`.

- **Translations**: 
  - Updated and revised several hundereds of missing translations since version 1.1.6.0.
  - Updates have been applied to both CN/JP translation files. (Note: The FI/FR files were notably outdated, with jumbled orderings.)
  - Fully revised CN translations.

- **Trigger Firing Settings**:
  - Previously the triggers would ignore all contidion checks when manually fired, but sometimes we want it to respect all conditions.  
  - Enhanced manual trigger firing to optionally respect conditions through the `Fire (Allow Conditions)` right-click menu option.
  - Also, introduced an `Allow conditions for autofiring` setting for triggers.

- **Testing Actions**: Introduced a `Test action with live values (ignore conditions)` option and a corresponding default configuration setting to bypass conditions during tests.

- **Main UI Enhancements**:
  - Enabled the `Add trigger / folder` buttons when a local trigger is selected, which adds the trigger / folder to the parent folder, just like pasting triggers from xml;
  - Automatically select the trigger/folder after drag and move.

- **CSV Export Improvements**: Enhanced support for table variables that contain commas and double quotes, providing more accurate exports, instead of simply joining together with `,`.

- **Miscellaneous Adjustments**: 
  - Optimized redundant logic patterns.
  - Addressed potential localization issues by ensuring consistent use of `CultureInfo.InvariantCulture`.
  - Corrected typos.
  - _etc._

## Different Behaviours

- **Mathparser Adjustments**:
  - The `:` character is now part of the `? :` ternary operator.
  - The `^` operator is now right-associative.
  - The precision error tolerance is set to `1E-9` (i.e., `0.1234567890 = 0.1234567899` is considered true).
  - Check the previous section for details.

- **Input Validation**: Some of the undefined or invalid inputs, which previously returned default values `` or `0`, now raise specific error messages.

- **Beep Frequency**: The default beep frequency is now in-tune (C6, 1046.5 Hz).

## Known Issues

- **Dynamic Variables**: Variables like `${_idx}` aren't thread-safe and should be used exclusively with synchronous actions.
- **Math Parser Limitations**: Doesn't support operators sharing the same priority level and not fixed in this version.
- **Dictionary Editor Display**: Dictionary variables now list keys in their intrinsic order instead of a sorted manner.
- **Performance**: Loading the action form has been notably slow (~0.8-2 s) from long time ago, possibly due to the expanded variety of actions. I am not familiar with WinForms and I am wondering if it could be fixed.
- An error was once reported upon clicking the action, but it could not be reproduced.

```
System.ArgumentOutOfRangeException - Index out of range.
   in System.Collections.ArrayList.get_Item(Int32 index)
   in System.Windows.Forms.DataGridViewSelectedRowCollection.get_Item(Int32 index)
   in Triggernometry.CustomControls.ActionViewer.btnEditAction_Click(Object sender, EventArgs e)
   in Triggernometry.CustomControls.ActionViewer.dgvActions_CellDoubleClick(Object sender, DataGridViewCellEventArgs e)
   in System.Windows.Forms.DataGridView.OnCellDoubleClick(DataGridViewCellEventArgs e)
   in System.Windows.Forms.DataGridView.OnDoubleClick(EventArgs e)
```

## Current To-do List  
- [x] Clipboard
- [x] UnsetRegex for all types of var
- [x] Pop to list
- [ ] review


## Future
- [ ] More intelligent autofill: close the brackets, move the cursor, and refresh the autofill form.  
- [ ] Dictionary Variable Editor (Sort)  
- [ ] Show the count of errors and warnings  
- [x] combobox row height (written but not used: the customized drawing caused the loading time changed from 1 s to 3 s)  
- [ ] Figure out a way to apply rotation matrix
- [ ] Add customized exceptions to the math functions (need to tolerate with testmode and the exptextbox bgcolor logic).
- [ ] `_color[x][y]`
- [ ] global font settings
