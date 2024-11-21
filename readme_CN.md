**当前 `readme` 分支仅用于说明文档和相关工具。如果要浏览 Triggernometry 代码，可以点击左上角切换其他分支。**  

**[View this page in English](https://github.com/MnFeN/Triggernometry/blob/readme/readme.md)**

**[浏览主仓库 Triggernometry 文档](https://github.com/paissaheavyindustries/Triggernometry)**

本文档是自 Triggernometry v1.1.7.3 版本以来我所修改部分的中文版总结。  

~~ChatGPT 机翻完大致改改，懒得再写一遍中文了x~~

# 新增内容

## 2024/11/10

### 字符串三元表达式
  
![image](https://github.com/user-attachments/assets/58e4e003-8087-472e-8359-59980d7e3d15)

快捷键：`Ctrl+Shift+I`

语法简化。if 后面的部分会自动解析为一个数学表达式，并根据是否非 0 判断真假。

`${if: ${condition} ? trueVal : falseVal}` 按照旧方法只能写作更冗长的表达式，如：  
`${func:ifequal(0, falseVal, trueVal):${numeric:${condition}}}`

### 生成 Debug 触发器

  根据给定的日志行，生成调试日志触发器。

![image](https://github.com/user-attachments/assets/17f2bd46-efc6-4986-94b3-f7112cb44092)

![image](https://github.com/user-attachments/assets/64fb856c-f6b9-4b0b-b8f9-3d6b4dbc1b4f)

### OverlayPlugin 交互模块

可使用原本查询实体的语法查询新的属性，如：

`${_entity[xxx].WeaponId}`

也可使用脚本代码获取：

```csharp
using Triggernometry.PluginBridges;
public static List<BridgeOverlay.OpCombatants> BridgeOverlay.GetCombatants(bool queryStatus)
```

用例：

```csharp
using System.Windows.Forms;
using System.Linq;
using Triggernometry.PluginBridges;

var combatants = BridgeOverlay.GetCombatants(false);

// 例：只能在 OverlayPlugin 中获取的属性:
OpCombatants combatant = combatants.FirstOrDefault(c => c.WeaponId == 4 && c.PosX > 100);
MessageBox.Show(combatant.ID.ToString("X8"));
```

## 2024/5/27

### 表达式

- **字符串函数**

  - `tofullwidth` / `tohalfwidth`

    全半角转换。
    
    `${func:tofullwidth:H1}` = `Ｈ１`
    
    `${func:tohalfwidth:Ｈ１}` = `H1`

  - `toxivchar(combineDigits=false)`

    将字母数字字符转换为相应的 FF14 定义的黑框字符。   
    如果 `combineDigits`为 `true`，则将 10 到 31 之间的数字转换为一个黑框字符。

  - `ord(separator=",")`

    将字符串转换为字符编码序列。
    
    `${func:ord:Test 1}` = `84,101,115,116,32,49`
    
    `${func:ord(-):Test 1}` = `84-101-115-116-32-49`  

  - `chr(joiner=",")`

    `ord`的逆运算。  
    `${func:chr:84,101,115,116,32,49}` = `Test 1`

- **常规表达式**

  - `_triggerpath`
    
    触发器的完整路径。

- **数学函数**

  - L1 和 L∞ 距离函数

    Ln 距离的定义： 
    
    - `distance = (|x - x0| ^ n + |y - y0| ^ n + ...) ^ (1 / n)`

    L2 距离：普通距离（欧几里得距离）  
    L1 距离：曼哈顿距离   
    L∞ 距离：切比雪夫距离  

    表达式写作：

    `l1d(...)` / `manhattandistance(...)`
    
    `l∞d(...)` / `chebyshevdistance(...)`  

    参数：同`distance()`
    
    - 例如 `l1d(x0, y0, x1, y1)` `l1d(x0, y0, z0, x1, y1, z1)`

    如果需要频繁检查两个位置是否靠近，`l1d` 比 `distance` 计算量更小。

### 动作

- **新动作类型：ACT 交互** 

  包括：

  - 开始/结束 ACT 战斗（原本的 “结束战斗” 会自动转换为此动作）

  - 启用/禁用：解析插件注入

  - 启用/禁用：解析插件记录所有网络数据

  SE 可能突然使用某些未被解析为日志行的数据包作为确定机制解法的唯一方式，此时这个功能会很有用。  

  你可以在特定时间控制此选项开关，并使用 `252` = `0xFC` 网络数据包日志行来触发您的触发器。

  ~~比如绝欧 P2 打了好几天才想办法搞出写法的男女组合技~~ 

### UI / 改善用户体验

- **允许按降序排序文件夹**

  相关讨论：https://discord.com/channels/374517624228544512/1237066801876041783

- **允许在非开发者模式下触发触发器**

  有些触发器需要用户手动触发以进行自测。这不应被视为“开发者”级别的使用。   

  许多人提问 “为什么我不能右键触发”，也说明了这一点。

- **在主界面上显示错误日志计数**

  将界面上方的 “遇到了错误” 更改为显示自上次打开错误页面以来遇到的具体错误数量。

  还修复了一个问题：打开此界面一次后，即便后续出现错误，也不会再次显示这个错误提示。

  此外，将日志系统从单一的队列改为以日志级别为键的队列字典，每个日志级别独享一个队列和数量上限，防止像 Info/Verbose 等常规日志覆盖较旧的 Error/Warning 日志中的有用信息。

- **增强表达式文本框中的双击/三击选择**

  - 双击：

    - 点击各种括号 / $ / ¤：

      选中这个括号配对后的完整表达式，这在编写长嵌套表达式找不到配对括号时非常有用；

    - 点击空格：

      选择同一行中相邻的空格；

    - 点击其他字符：

      选择当前“单词”（分词远好于 WinForm 默认逻辑）。

  - 三击：

    - 单行：选择所有文本

    - 多行：选择当前行

- **在状态表单中显示更多命名回调的信息** 

  - 注册者

  - 注册时间

  - 最后调用时间

### 代码 / 脚本

- **注册命名回调**

  新增了 `registrant` 参数：

  ```csharp
  RegisterNamedCallback(string name, CustomCallbackDelegate callback, object o, string registrant) 
  ```

  原函数仍可使用，可自动检测注册者名称。

- **添加 ReadonlyRichTextbox 类，以自定义格式显示文本**

  ```csharp
  public class Triggernometry.CustomControls.ReadonlyRichTextbox : RichTextbox
  ```
  
  该富文本框具有“透明”背景，不允许任何形式的鼠标交互（就像 Label 一样）。

- **提供更多导入信息** 

  - 导入失败时，显示更详细的原因

  - 显示导入的 xml 的插件版本

### 错误修复

详情请查看[链接](https://github.com/paissaheavyindustries/Triggernometry/pull/107)。

### 注意：行为变更

- 换行符

  `⏎` 等效于换行符，而换行符属于空白字符。因此在拆分参数时会 Trim 掉这个字符，除非它被引号包围。

  - 例如：应使用 `listvar.join("⏎")`，而非 `listvar.join(⏎)`。

  另外，换行符也可以在动作中使用，并视为单个字符：

  - 例如，使用下面的表达式来构建列表 `1, 2, 3`  
  （第一个字符是换行符，当在动作中构建变量时作为后续文本的分隔符）：

    ```
    
    1
    2
    3
    ```

    此改动可允许多行输入，在使用大量数据构建变量时更易于阅读。

## 2024/4/7
### 消息框
- 更智能的自动填充：
  - 如果在变量名的文本框中输入了只包含一个或没有`${...}`表达式的字符串，它会被保存到相应的动态变量列表中；
  - 如果任何输入字符串包含单层变量表达式，如`${var:name}`，则`name`会被保存到相应的动态变量列表中；
  - 如果用户在类似`${v:...`之后输入，或在变量名的表达式文本框中输入，它也会检查动态列表中的所有名字。
  - 此功能与所有类型的变量（临时/永久）、文本/图像悬浮窗和命名回调兼容。
- 更改了ActionForm中Enter键的行为：
  - 在单行模式表达式文本框中按Enter键时，会切换到多行模式；
  - 在多行模式中按下时，将直接添加一个换行符，下一行将与上一行具有相同的缩进。

### 文本悬浮窗
- 颜色表达式
  - 为文本悬浮窗的前景色、背景色和轮廓色添加了3个表达式文本框。
  - 颜色表达式与动作描述中的相同，并将显示相应的解析颜色作为文本框的背景色：
    - `aaccff` / `#aaccff`
    - `acf` / `#acf`
    - `192, 0, 18`
  - 这些颜色接受表达式，因此可以根据某些实际值在同一个动作中动态改变颜色，而无需使用只有颜色不同的几个不同动作。（但目前仍然需要执行动作以刷新颜色）
    例如，根据 DSR P6 中两条龙的血量改变文本颜色。
  - 仍然保留了颜色选择器，为用户提供直接选择颜色的方式。

### RealPlugin / 解释器
- 将`RealPlugin.WindowsUtils`类移动到`Triggernometry.Utilities`命名空间，并添加了相应的脚本API安全选项。
- 添加了一个ffxiv进程句柄（具有全部访问权限）：
  ```csharp
    public IntPtr Triggernometry.Realplugin.plug.XivHandle
  ```
  注意：这依然安全，因为所有危险API依然默认受限。它也可以在以后用于读取ACT中不可用或更新太慢的一些实体属性（如坐标）。
- 由于当前脚本环境无法直接访问`System.Text.Json`，添加了两个Json方法：
  ```csharp
    public static string Triggernometry.Interpreter.StaticHelpers.Serialize(object o, bool indent = true);
    public static T Triggernometry.Interpreter.StaticHelpers.Deserialize<T>(string s);
  ```
  
## 2024/3/27
### MathParser
- 添加运算符 `°`，例如，`180° = 3.14159...`  
- 添加函数 `isanglebetween(θ, θ1, θ2)` ，用于判断给定角度 `θ` 是否处于 `θ1` 到 `θ2` 的范围内（按照角度增大的方向，即 FFXIV 坐标系中的逆时针方向）。
  - 输入角度无需标准化到 [-pi, pi]。输出为 0 或 1。  
    `isanglebetween(pi/4, 0, pi/2) = 1`  
    `isanglebetween(pi, pi/2, -pi/2) = 1`  
    `isanglebetween(0, pi/2, -pi/2) = 0`  
  - 例如：判断角色面向在背对机制中是否安全。

### Actions
- 在 `LogMessage` 动作中添加新选项 “添加日志到 ACT 战斗记录”，便于在 ACT 战斗记录中一起浏览正常 ACT 日志和自定义日志。
  - 例如，一个 `1B`（点名标记）日志可以在去除偏移后，以自定义格式添加到战斗记录中，就像是同时生成了一条没有偏移的日志。

### Entity
- 新增实体属性：`subrole` 和 `roleid`（对应下面定义的文本和数值）。
```csharp
public enum RoleType
{ 
    None          = 0,
    Tank          = 8,
    Healer        = 16,
    DPS           = 24,
    Crafter       = 32,
    Gatherer      = 48,
    MainRole      = 56,

    PureHealer    = Healer | 1,
    FlexHealer    = Healer | 2,
    BarrierHealer = Healer | 3,
    StrengthMelee  = DPS | 1,
    DexterityMelee = DPS | 2,
    PhysicalRanged = DPS | 4,
    MagicalRanged  = DPS | 6,
}
```
  
- 对 `_entity` 新增查询模式：`${_entity[key=value].prop}`  
  - 例如，`${_entity[bnpcid=12601].heading}` 可用于查询 BNpcId 为 12601 的实体面向。
  - 返回找到的第一个实体。如果没有找到实体，则返回 NullCombatant 的数据。
  - 例：可以基于某些特征实体的 BNpcId 判断是否处于门神或本体阶段。
  - 如果需要更复杂的查询条件，或查询多个符合条件的实体，可以使用 Table 动作查询所有实体，或直接使用脚本：
    `List<VariableDictionary> Triggernometry.PluginBridges.BridgeFFXIV.GetAllEntities()`

### Interpreter
- 在 Interpreter 中添加了一个静态工具类 `StaticHelpers`，以便于在 class 中使用与 Context 实例无关的方法。
- `TriggernometryHelpers` 的所有方法仍然可用。
- 例：
```csharp
using Triggernometry.Variables;
using static Triggernometry.Interpreter;

class ConfigForm
{
    //...

    public void LoadFromConfig()
    {
        VariableDictionary config = StaticHelpers.GetDictVariable(isPersistent, configName);
        // ...
    }
}
```
  
### 其他
- 按照新增的 `procid` 逻辑，修改了需要特定窗口标题和 `procid` 的动作描述。

- 修复了若干空引用异常，如 `ActionViewer.Actions = null` 导致在 ActionForm 界面点击时偶发错误，以及 `RealPlugin.plug.currentZone = null` 在 FFXIV 未运行时编辑分组区域限制可能引起的错误。

- 由于之前添加了用于测试动作的其他属性，将 `testmode` 属性重命名为 `testByPlaceholder` 以消除歧义。

- 将几个错误命名为 `cbx...` 的复选框重命名为 `chk...`。

- 其他小修改。

## 2023/11/29
- ActionViewer
  - 右键菜单中添加 “复制条件”、“粘贴条件”、“测试动作”

- ActionForm / Action
  - 修复了与模板触发器相关的空引用错误 [null reference bug](https://discord.com/channels/374517624228544512/599935468578144276/1176446751675252736)
  - 动作中发生异常的日志条目现在将包含相应的描述和触发器路径
  - 添加了两个动作：
    - VariableScalar - `Increment`（数值递增）
    - VariableTable - `AppendH`（水平追加表格）
  - 更新了 KeyPress 的帮助文档链接，并根据所选语言选项切换到相应语言的链接
  - 修复了一些表格动作没有设置其变更者和时间的问题，例如 `Resize` 和 `Copy`

- Context
  - `${estorage:xxx}`：检查脚本 Storage 中是否包含键 `xxx`
  - `${_storage[xxx]}`：输出脚本存储中的对象（ToString）
  - `${_configpath}` `${_pluginpath}`：对应的本地文件夹路径
  - 添加了 `${_config[UnsafeUsage]}`;
  - 将 `${_config[API]}` 的结果改为位运算（`0-7`，`Local << 2 | Remote << 1 | Admin`）

- RealPlugin
  - 修复了更新插件后第一次启动时 `cfg.Constants` 中的版本号没有更新，但第二次启动时更新的错误
  - 使具名回调（委托）中的异常在日志中正确显示实际的异常信息
  - 添加了 `static RealPlugin RealPlugin.plug` 以便于引用（单例模式，整个程序中的所有 `RealPlugin` 实例都是同一个）。

- 其他
  - 小改动：
    - 将 `void Context.XxxxxError()` 改为 `Exception Context.XxxxxError()`
    - 将 `I18n.TrlXxxxx()` 改为单一方法 `I18n.Trl("xxxxx")`
    - 将一些 `internal` 改为 `public` 以供脚本使用
    - 翻译修正

## 2023/11/10
### ActionViewer
- 修复了 ActionViewer 中部分按钮有时不能正确启用/禁用的错误；
- 修复了 dgvActions 中双击时偶尔因未选中动作导致的空引用错误；
- 修复了计算触发器总延迟时未忽略禁用的动作的错误；
- 修复了撤销会打乱 `OrderNumber` 的问题，并将撤销时的浅复制改为深复制（可撤销单个动作的修改）；
- 在动作右键菜单中添加了一些快捷设置，以便批量调节异步、延迟、条件等动作属性；
- 粘贴动作后选中粘贴的动作；
- 点击其他位置时取消选中动作；

### ConditionViewer
- 条件右键菜单中添加了展开/折叠全部的选项，并在加载时展开全部条件；
  (https://discord.com/channels/374517624228544512/1154813334835707957)

### ExpressionTextBox
- `MaxLength` 从默认值 `32767` 改为 `1000000`，以便使用脚本；
- 修正了自动补全的 Table 方法 `vlookup()` 中提示的参数名错误；
- 修正了 `MaximumSize` 的计算错误并微调高度；

### ActionForm
- 对变量操作等部分动作添加了内置的文本提示帮助，并整合了 `SendKeys` 等方法的文本提示；
- 修复了 `KeyPress` 动作测试时，文本框显示两秒后执行，但实际并没有相关代码延迟两秒的错误；
- 修复了 `SendKeys` 动作中键盘录制工具输出结果的错误；
  (https://discord.com/channels/374517624228544512/599935468578144276/1152402243245588572)

### LogForm
- 所有级别日志类型已勾选时，自动勾选“全选”

### StateForm
- 微调列宽；
- 修复了具名回调界面无任何内容的错误，`RefreshNamedCallbacks` 函数原本没有任何内容；

### BridgeFFXIV
- 修复了 `NullCombatant` 已定义但从未初始化的错误；
- 将 `ClearCombatant` 中的属性改为空字符串，以免混淆，如 `NullCombatant.x` 为 0 会让人误以为查询到了 `x = 0` 的实体；
- 将 `Jobs` 相关的所有属性加入实体字典；
- 将 `TranslateJob`、`TranslateRole` 函数用 `Entity.cs` 中定义的字典代替；

### Action
- 修复了 `KeyPress`、`SendWindowMessage` 动作描述不支持 `procid` 的问题；
- 新增了字典动作 `GetEntityByName` / `GetEntityById`、表格动作 `GetAllEntities`，以便一次性获取单个或全部实体信息；
- 表格动作 `Resize` 可省略宽高之一以表示该维度不改变；

### Context
- 修复了属性相关的正则中使用贪婪匹配变量名的错误；
- 增加了 `_rowcl[...]` `_colrl[...]` 两个动态变量，根据相应的表头返回对应单元格内容；
- 增加了 `ecallback:...`，用于检测是否存在某个名称的具名回调；
- 修复了表格的 `contain` 和 `ifcontain` 方法被置于字典变量相关代码块中的错误；
- `func:pick():string` 改为使用与分割参数一致的逻辑分割 string，而非根据逗号简单拆分；

### Interpreter
- API 受限时错误信息提示具体 API 名称；
- 脚本运行过程中出错时，捕获 AggregateException 并生成对应的错误信息；
- 增加了字典变量的 SetDictVariable 和 GetDictVariable；
- 对于 SetXXXVariable，提供的变量参数为 null 时删除该变量；

### MathParser
- 增加了运算符 `??`：若前一个参数无法解析为数值，则返回后一个参数，类似于空合并运算符。如：`1 ?? 2 = 1`; `A ?? 2 = 2`；
- 修复了 `roundir` 函数值域的错误；
- 增加了对十六进制，二进制，八进制的直接输入支持，如 `0xFF`, `0b11`, `0o77`；
- 对于待判断的 `${...}` 表达式返回空字符串导致 `==`、`??` 处于 tokens 列表首尾的情况添加了条件判断

### RealPlugin
- 保存配置时校验临时文件最后一行的内容，以尝试修复 ACT 被强制退出时 `StreamWriter.write` 中断导致配置文件末尾残缺的问题；
- 加载配置文件时，若最后一行内容不正确则视为配置损坏，自动加载 `.previous` 文件；
- 修复 `ReadyForOperation` 函数偶发的空引用异常；
- 添加了用于在脚本中根据回调名称添加/删除回调的 `RegisterNamedCallback` 和 `UnregisterNamedCallback` 的重载

## 2023/9
## 数学解析器 (MathParser)
数学解析器的大部分核心内容已经被重写：
### 负号解析：
已修复负号的解析逻辑中的多个错误：
- 原始代码只检查前一个字符是否是数字来确定 `+`/`-` 是符号还是操作符。这个疏忽导致了像 `func(1, -1)` 或 `1 - -1` 这样的含空格的表达式解析错误。
  - 相关：[#87](https://github.com/paissaheavyindustries/Triggernometry/issues/87)  
- 在 `BasicArithmeticalExpression()` 函数中，当应用负号时，只处理了正值，忽略了非正值。这导致像 `-(-1)` 这样的表达式被错误解析为 `-1`。
  - 相关：[Discord](https://discord.com/channels/374517624228544512/1114692015163191316)  
- 原始代码给了负号一个隐藏的优先级，导致计算顺序错误，比如 `-2^2 = 4`（在大多数现代语言中答案应为 -4）。
- 原始代码未能识别函数前的负号，如 `-func(args)` ，导致 `0 = -sin(0)` 这样的表达式中，代码会尝试在 `=` 和 `sin(0)` 之间做减法而出错。
  - 相关：[Discord](https://discord.com/channels/374517624228544512/1114692015163191316)

这些错误已被修复，处理 +/- 符号的全部逻辑已重构并简化。旧版词法分析器和解析器都使用特殊逻辑处理 `+`/`-`；现在，词法分析器仅将其视为正常运算符，而在解析器中用一个简单逻辑即可处理正负号。

### 词法分析逻辑 (Lexer)
- 词法分析器已简化，只专注于当前字符是否属于操作符字符，并将操作符与非操作符拆分。
- 如果解析器无法解析基本表达式，它会抛出一个错误，详细说明哪个操作符在哪个表达式中无法被解析。
- 旧版词法分析器尝试在像 `3abs(0)` 这样的表达式之间添加 `*`，但这种方法逻辑和原理上都不正确：
  - 若不花费额外时间扫描整个函数列表匹配函数名，则不可能区分 `3abs(0)` 中的 `3ab` 和十六进制数字 `3ab`；
  - 代码中当 `a` 前面有 `3` 时，`3` 会作为 token 的开始，并没有机会检查 `a` 前是什么。
- 为了不花费额外时间解析函数名，并未支持此类隐式乘号，数字和函数/常量之间依然需要显式的 `*`。

### 操作符
- 旧版解析器只支持单字符二元左结合运算符。核心逻辑重写后，解析器现在额外支持双字符、一/三元、右结合操作符。
- 已添加以下操作符：
  - `&&` `||` `^^` `!`：逻辑运算 与/或/异或/非。  
  - `%%` `//`：模和整除。注意模是 mod 而非 remainder（与除数同号），整除结果永远向下取整。
  - `√`：根号（一元运算符）
  - `>=` `<=` `!=`：作为别名
  - `==` ：字符串等价于（如 `DD5 == DD5` = `1`），唯一一个操作字符串的运算符
  - `&` `|` `⊕` `~` `<<` `>>`：位运算（如：可以方便地使用单个变量存储并解析多个实体在随机位置出现的状态）
  - `? :`：三元运算符
- 全部运算符按顺序列出:
  - `√` `!` `~`
  - `^` `%` `%%` `/` `//` `*` `-` `+`
  - `<<` `>>`
  - `>` `≥` `>=` `<` `≤` `<=` `==`
  - `=` `≠` `!=`
  - `&` `⊕` `|`
  - `&&` `^^` `||`
  - `?` `:`
  - `(` `)` `,` （不直接处理）
### 精度误差容差
- 容差级别已从 `double.Epsilon` 更改为常数（设为 `δ` =  `1E-9`），以便 Triggernometry 使用。
- 这条规则只适用于涉及（显式或隐式）比较的函数和操作符，如 `=` `>` `>=` `sign` `truncate` 等。
- 这条规则不会降低任何计算精度。
- 在比较过程中，范围在 `x ± δ` 内的值均会被视为 `x`。

### 别名
- 在原始代码中，存在一个别名列表（例如 `atan2` => `arctan2`），但未被使用。
- 由于与 Triggernometry 的需求无关，已删除这些代码行，并直接将别名加入到函数列表中。

### 空格
- 现在解析表达式前会删除全部空格以简化逻辑。这意味着表达式中的任意空格将不会影响结果。
- 副作用：数字字符串函数现在不能在其参数中包含有意义的空格（不过此前并没有此类函数）。

## 参数
- 原始的 `SplitArgument` 函数在遇到不匹配的引号或连续的逗号时生成了错误的 `args` 列表。此外它并不支持换行符。
- 修改后的代码现在使用正则表达式来精确提取位于字符串开始、结束和逗号之间的所有参数。
- 单/双引号外的表达式会被剔除首尾空白；单独的空字符串或空格会返回空列表。
- 例如，(1,2,  3  ,"  4  ",   "5"  , "'", ', ', ) 现在转换为参数列表：
  - `1` `2` `3` `  4  ` `5` `'` `, ` `(空)`.
- 根据解析表达式时的展开逻辑，参数无法包含 `)` `{` `}`。所以添加了以下转义规则：
  + `{` 应该用全角 `｛` 或 `__LB__` 转义； （注：全角字符即中文输入法下的字符）
  + `}` 应该用全角 `｝` 或 `__RB__` 转义；
  + `(` **可以**用全角 `（` 或 `__LP__` 转义；
  + `)` 应该用全角 `）` 或 `__RP__` 转义；
  + `｛` `｝` 应该用 `__FLB__` `__FRB__` 转义；
  + `（` `）` 应该用 `__FLP__` `__FRP__` 转义；

## 索引和切片
### 负索引
- 索引现在支持负值，从后向前计数。
- 涵盖以下内容：`substring`；`lvar`；`tvar`；`tvarrl`；`tvarcl`；以及列表/表格操作中的 `index`/`row`/`column` 索引文本框。
- 之前的索引关键字 "last" 现在重定向到 -1。
- 例如，`${tvar:myTable[2][-3]}` 返回 `2nd` 列和 `-3rd` 行的值。
### 切片 (slice)
- 一个像 `start:end:step` 的切片表达式可以表示从 `start` 开始，每次增加 `step`，并在 `end` 之前结束的一系列索引。
- 此功能与 Python 的切片机制非常相似。
- 所有三个整数都可以省略：`a:b:c` `a:b:` `a::c` `:b:c` `a::` `:b:` `::c` `::` `a:b` `a:` `:b` `:` 
- 索引支持负值；字符串从 0 开始计数，列表/表格从 1 开始计数，与之前的 Triggernometry 功能保持一致。
- **切片**（和索引）可以合并成一个 **切片** 表达式 (slices)，例如：`:5, 7, 8:13:2, 16:` 表示 `(0), 1, 2, 3, 4, 7, 8, 10, 12, 16, 17, (...直到结束)`。
- 切片表达式广泛用于新特性中，在字符串表达式即可实现“伪”高维的列表/表格操作，且无需循环即可简化表达式/动作。
- 注意：“slices” 在函数和方法中被认为是单一参数。如果它包含逗号，需要将切片表达式包含在 `""` 或 `''` 中。

## 自动填充表单 （Autofill，即输入表达式时显示的预选单）
- 修复了一个表单不隐藏的错误，如输入 `tvar:` 后仍然显示 `tvarrl`；
- 添加了更多类型的自动填充：列表/表格/字典的属性；当前临时/永久变量、悬浮窗、常量名；当前触发器中的正则捕获组名；字典键和表格行列查找模式下的表头；
- 代码现在搜索前面的未关闭 `{` 以提供更智能的自动填充建议；(例如，`${lvar:xxx${var:yyy}${index}.` 会匹配到最开始的大括号，显示列表属性)；
- 自动填充表单现在准确出现在其匹配的字符串下方；
- 修复了多行模式下的错误：用 enter 键选择自动填充的同时会额外插入一个换行；
- 增加了自动完成框的高度 (5 → 10) 和宽度 ( → 所有匹配文本的最大长度)；
- 添加了一个去抖计时器：在文本框中的文本更改后开始 200 ms 倒计时，随后触发自动填充逻辑。此倒计时内再次更改文字会重置计时器，以在快速输入或按住删除时避免延迟。
  
## 字典变量  
- 补全了未启用的 VariableDictionary 类，并添加了相应的表达式、方法、动作、变量浏览器。  
- 详见下文。

## 表达式和函数  
注意以下表达式中，`f(a, b, c = 1)` 这种表述意为函数 `f` 接受 `2-3` 个参数，第三个参数若不提供则默认为 `1`。 

### 特殊变量:  
|表达式|描述|  
|:---|:---|  
|`_ETprecise`|提供垂直日的确切分钟。<br />是 `_ffxivtime` (`_ET`) 的更准确版本。|  
|`_idx`|动态表达式。代表当前索引。|  
|`_col`|动态表达式。代表当前列索引。|  
|`_row`|动态表达式。代表当前行索引。|  
|`_col[i]`|动态表达式。代表当前列中行索引 `i` 的值。|  
|`_row[i]`|动态表达式。代表当前行中列索引 `i` 的值。|  
|`_this`|动态表达式。代表当前列表或表格单元的值。|  
|`_key` <br />`_val`|动态表达式。代表当前的键/值。|  
|`_clipboard`|系统剪贴板中当前复制的文本。|  
|`_config[x]`|获取一些会对用户操作或使用触发器的结果造成影响的用户配置。（详见 Autofill 表单）|

关于动态表达式的详细信息，请参阅操作部分。

### 数值常量:  
|表达式|描述|  
|:---|:---|  
|`semitone`|`2^(1/12)`。<br />两个相邻半音之间的频率比率。|  
|`cent`|`2^(1/1200)`。<br />两个相邻音分之间的频率比率。|  
|`ETmin2sec`|`35/12`。<br />艾欧泽亚 1 分钟和现实 1 秒之间的比率。|  

### 数学函数:  
|表达式|描述|示例|  
|:---|:---|:---|  
|`distance()`|现在支持 2 组 _`n`_ 维坐标。<br />当 _`n`_ = `2` 时，与之前的版本行为一致。|`distance(0,0,0, 3,4,12)` = `13`|  
|`projectdistance()`<br />`projectheight()`|射影长度及射影高度，如图。![proj](https://github.com/MnFeN/Triggernometry/assets/85232361/87d24efc-0d67-4d26-946a-81e91d3ba4c2)<br />在涉及直线/射线型 AoE 的计算时很有用。|`projd(0,0, pi/6, -2,0)` = `-1`<br />`projh(0,0, pi/6, -2,0)` = `1.732...`|  
|`angle(x1, y1, x2, y2)`|= `atan2(x2-x1, y2-y1)`|`angle(100, 100, 120, 100)` = `1.57...`|  
|`relangle(θ1, θ2)`|将 `θ1` 作为相对北，返回 `θ2` 的方向，规范至 `[-π, π)` 区间。|`relangle(0, -pi/2)` = `1.57...`|  
|`roundir(θ, ±n, digits = 0)`<br />`roundvec(x, y, ±n, digits = 0)`|将给定方向（`roundir` 以弧度表示；`roundvec` 函数中以向量的分量 dx, dy 表示）与一个 `\|n\|` 等分的圆中的方向匹配，然后返回该方向的索引。<br />`n` 的符号表示两种划分模式：正北本身是等分点，或正点位于两个等分点的中点，如下所示。<br />`digits` 指定舍入的小数位数；负值代表不舍入。<br />![image](https://github.com/paissaheavyindustries/Triggernometry/assets/85232361/b7ab1f13-c5ba-4609-b588-b066d5d9d4e1)<br />例如，用于计算具有多个潜在生成点的实体的方向。可以与 `func:pick(index)` 结合使用，从弧度或坐标输出任何方向为字符串，无需复杂的 `arctan2` 和 `mod` 计算。|`roundir(-1.57,4)`<br /> = `1` (西)<br />`roundvec(8,-6,-4)`<br /> = `3` (东北)|  

### 数学函数（字符串）：
|表达式|描述|示例|
|:---|:---|:---|
|`parsedmg(hex)`|将 `0x15`/`0x16` ACT 日志行中的 16 进制伤害/治疗字符串转换为相应的十进制值。<br />规则：用 `0` 从左侧填充16进制字符串到8位为 `XXXXYYZZ`，然后将 `ZZXXXX` 转换为十进制。|`parsedmg(A00000)` = `160`|
|`freq(note, semitones = 0)`|返回指定音符（使用科学音高表示法，变音符用 `#`、`b`、`x` 表示）加上半音偏移后的频率（Hz）。|`freq(A4)` <br />= `freq(G#4, 1)` <br />= `freq(Bb4, -1)` <br />= `freq(A5, -12)` <br />= `440`|
|`nextETms(XX:XX)` `nextETms(ETminutes)`|提供直到下一次指定的艾欧泽亚时间的现实剩余时间（ms）。|当前 ET 为 `1:00`：<br />`nextETms(2:00)`<br />= `nextETms(02:00.00)`<br />=`nextETms(120)`<br />= `175000` (2 min 55 s)|

### 字符串函数：
|表达式|描述|示例|
|:---|:---|:---|
|`parsedmg`|与数学函数相同。不接受任何参数。|`func:parsedmg:A00000`<br />= `160`|
|`slice(slices = ":")`|接受一个切片表达式作为参数，返回字符串的指定切片。|`func:slice(-3):01234` = `2`<br />`func:slice(1:4):01234` = `123`<br />`func:slice(::-1):01234` = `43210`<br />`func:slice("1,3:"):01234` = `134`|
|`pick(index, separator = ",")`|按指定的分隔符分隔给定字符串。<br />根据索引返回子字符串，从 0 开始。<br />支持负索引。|`func:pick(3):north,west,south,east`<br /> = `east`<br />`func:pick(-1,", "):1, 22, 3, 44, 5`<br /> = `5`|
|`contain(str)`<br />`startwith(str)`<br />`endwith(str)`<br />`equal(str)`|返回 `1` 或 `0`。|`func:contain(23):1234` = `1` <br />`func:endwith(23):1234` = `0`<br />`func:equal(23):1234` = `0`|
|`ifcontain(str, t, f)`<br />`ifstartwith(str, t, f)`<br />`ifendwith(str, t, f)`<br />`ifequal(str, t, f)`|与 `if()` 类似。|`func:ifcontain(23, a, b):1234` = `a` <br />`func:ifendwith(23, a, b):1234` = `b`<br />`func:ifequal(23, a, b):1234` = `b`|
|`indicesof(str, joiner = ",", slices = ":")`|在字符串的指定部分搜索所有索引，然后以 joiner 连接。|`func:indicesof(a):abcbabcba` = `0,4,8`<br />`func:indicesof(a, "-", ::-1):abcbabcba` = `8-4-0`|
|`match(str):regex`|返回 `1` 或 `0`。<br />注意：正则表达式不应包含 `{` `}`。<br />`{` 应使用全宽 `｛` 或 `__LB__` 转义；<br />`}` 应使用全宽 `｝` 或 `__RB__` 转义；<br />`｛` `｝` 应使用 `__FLB__` `__FRB__` 转义。<br />下面两个函数同样适用这些正则规则。|`func:match(404D):404[B-D]` = `1`<br />`func:match(4000A3BF):4.｛7｝` = `1`|
|`capture(str, group):regex`|返回捕获的字符串 `$groupindex` 或 `${groupname}`。如果 `groupindex` = `0`，则返回整个匹配的字符串。<br />如果找不到 `groupname` 或 `groupindex` 超出范围，则返回一个空字符串。<br />遵循前述正则规则。|`func:capture(Player NameGilgamesh, server):.+ .+(?<server>[A-Z].+)`<br />= `Gilgamesh`|
|`ifmatch(str, t, f):regex`|与 `if()` 类似。|`func:ifmatch(404D, a, b):404[B-D]` = `a`|
|`replace(oldStr, newStr = "", isLooped = false)`|在指定字符串中用新字符串替换旧字符串。可以循环替换。|`func:replace(" "):1 2 3`<br />= `123`<br />`func:replace(aa,a):aaaaaa`<br />= `aaa`<br />`func:replace(aa,a,true):aaaaaa`<br />= `a`|
|`repeat(times, joiner = "")`|将字符串重复指定次数，可以添加连接符。|`func:repeat(3):a` = `aaa`<br />`func:repeat(3, +):1` = `1+1+1`|
|`padleft`<br />`padright`<br />`trim`<br />`trimleft`<br />`trimright`  |这些函数在旧版本中只支持字符码的函数，现在可以接受字符本身或其字符码。<br />`0`-`9` 被解释为字符而不是字符码，因为 ASCII 0-9 控制字符几乎不会使用到。<br />输入汉字、全宽字符、CJK 扩展区字符时再不需要用五位的字符码了。|`func:trim(48, 2, a):abcd0320`<br />= `bcd03`<br />`func:padleft(0,8):1ABCD`<br />= `0001ABCD`|  

### 列表变量：
- 本段使用 **`lvar:test` = `1, 2, 3, 4, 5, 6, 7, 8, 9`**（此字符串仅为列表的表示）为例。

|表达式|描述|示例|
|:---|:---|:---|
|`${?lvar:...}`|直接根据由 `,` 分割的表达式构建临时列表，并可使用任何列表属性返回字符串。<br />与分割参数的规则相同，如引号等。<br />构建变量可能稍微慢一些，但运用得当则可以省去多个动作和条件。|`${?lvar:a, b, c, d, e.indexof(c)}` = `3`<br />`${?lvar:a, b, "c,c", d, e[3]}` = `c,c`|
|`sum(slices = ":")`|返回列表（的切片）中的值之和。<br />只有可以解析为 `double` 格式的值才会相加。|`${lvar:test.sum}` = `45`<br />`${lvar:test.sum(1:5)}` = `10`|
|`count(str, slices = ":")`|返回字符串在列表（的切片）中出现的次数。|`${lvar:test.count(3)}` = `1`<br />`${lvar:test.count(a)}` = `0`|
|`join(joiner = ",", slices = ":")`|使用指定的连接符连接列表（的切片）。|`${lvar:test.join}` = `1,2,3,4,5,6,7,8,9`<br />`${lvar:test.join(" ",5::-1)}` = `5 4 3 2 1`|
|`randjoin(joiner = ",", slices = ":")`|与 join() 类似，但在连接之前随机排列所选元素。|`${lvar:test.randjoin}` = `4,9,2,3,5,7,8,1,6`（随机示例）|
|`contain(str, slices = ":")`|如果列表（的切片）包含给定的字符串，则返回 1，否则返回 0。|`...contain(3)` = `1` <br />`...contain(3, 4:)` = `0`|
|`ifcontain(str, trueExpe, falseExpr)`|与 `if()` 类似。如果列表包含该字符串，返回 `trueExpr`；否则，返回 `falseExpr`。|`...ifcontain(3, found, missing)` = `found` <br />`...ifcontain(a, found, missing)` = `missing`|
|`indicesof(str, joiner = ",", slices = ":")`|在列表（的给定切片）中搜索字符串所有出现的位置，并将原索引连接成一个字符串。与字符串函数类似。||
|`max(type = "n", slices = ":")` <br /> `min(type = "n", slices = ":")`|根据 `type` 返回列表（的切片）中的最值：`n` （默认）表示数字，`h` 表示十六进制，`s` 表示字符串。若有无法解析为该类型的字符串则会报错。|`${lvar:test.max}` = `9` <br />`...min(n, 3:)` = `3`|

### 表格变量：
- 本段以如下 **`tvar:test`** 为例：

|11|21|31|41|
|---|---|---|---|
|12|22|32|42|
|13|23|33|43|
|14|24|34|44|

|表达式|描述|示例|
|:---|:---|:---|
|`${?tvar:...}`|直接由 `,` 和 `\|` 分割表达式并构建临时表格。<br />与 `${?lvar:}` 类似。|`${?tvar: a,b | c,d [2][2]}` = `d`|
|`tvardl:` `ptvardl:`|与 `tvarrl:`/`tvarcl:` 类似的双基准查找。<br />返回两个表头所对应的行列处的值。|`${tvardl:test[41][13]}` = `43`|
|`sum(colSlices = ":", rowSlices = ":")`|返回表格（的行列切片）中的值之和。<br />只有可以解析为 `double` 格式的值才会相加。|`${lvar:test.sum}` = `440`<br />`...sum(1, :)` = `11 + 12 + 13 + 14` = `50`|
|`count(str, colSlices = ":", rowSlices = ":")`|返回字符串在表格（的切片行和列）中出现的次数。|`${lvar:test.count(33)}` = `1`<br />`${lvar:test.count(1)}` = `0`|
|`hjoin(joiner1 = ",", joiner2 = "⏎", colSlices = ":", rowSlices = ":")`|使用指定的连接符横向连接表格。|`...hjoin(",", ",", 1:3, 3:)` = `13,23,14,24`<br />`${tvar:test.hjoin}` = `11,21,31,41`<br />`12,22,32,42`<br />`13,23,33,43`<br />`14,24,34,44`|
|`vjoin(joiner1 = ",", joiner2 = "⏎", colSlices = ":", rowSlices = ":")`|使用指定的连接符纵向连接表格。|`${tvar:test.vjoin}` = `11,12,13,14`<br />`21,22,23,24`<br />`31,32,33,34`<br />`41,42,43,44`|
|`hlookup(str, rowIndex, colSlices = ":")`|在给定行中搜索字符串并返回列索引。<br />如果未找到，返回 0。|`...hlookup(13,3)` = `1`<br />`...hlookup(13,3,2:)` = `0`|
|`vlookup(str, colIndex, rowSlices = ":")`|在给定列中搜索字符串并返回列索引。<br />如果未找到，返回 0。|`...vlookup(13,1)` = `3`|  
|`max(type = "n", colSlices = ":", rowSlices = ":")` <br /> `min(type = "n", colSlices = ":", rowSlices = ":")`|与列表方法相同。|略|  

### 字典变量：
- 本部分以 **`dvar:test` = `a=1, b=2, c=3, d=3, e=3`** （这个字符串仅为字典的表现形式）作为示例：

| 表达式 | 描述 | 示例 |
|:---|:---|:---|
|`${?dvar:...}`|直接由 `=` 和 `.` 分割表达式并构建一个临时字典。<br />与 `${?lvar:}` 相似。|`${?dvar: 7CD2=内, 7CD6=外, 7CD7=分散 [7CD2] }` = `内`|
|`sumkeys()` `sum()`|求和所有可以解析为 `double` 格式的键/值。|`${dvar:test.sumkey}` = `0`<br />`${dvar:test.sum}` = `12`|
|`count(value)`|返回字典中给定值的计数。|`...countvalue(3)` = `3`|
|`dvar:` `edvar:`<br />`pdvar:` `epdvar:`|e (存在) / p (永久)。与其他变量相似。| `${epdvar:dictname}`<br />`${dvar:test[e]}` = `3` |
|`length` / `size`|字典中的键数量。| `${dvar:test.size}` = `5` |
|`ekey(key)` `evalue(value)`|检查键/值是否存在于字典中（返回 0/1）。| `${dvar:test.ekey(a)}` = `1`<br />`${dvar:test.evalue(4)}` = `0` |
|`ifekey(key, t, f)`<br />`ifevalue(value, t, f)`|与字符串函数相似（返回字符串 t/f）。| `...ifekey(a, 有, 无)` = `有` |
|`keyof(value)`|按值反向查找键，返回找到的“第一个”键，如果未找到则返回空字符串。| `${dvar:test.keyof(1)}` = `a`<br />`${dvar:test.keyof(4)}` = `` |
|`keysof(value, joiner = ",")`|查找所有与给定值匹配的键，并使用连接符连接。| `...keyof(3)` = `c,d,e`|
|`joinkeys(joiner = ",")`<br />`joinvalues(joiner = ",")`<br />`joinall(kvjoiner = "=", pairjoiner = ",")`|使用连接符合并键/值/或两者。|`...joinkeys(-)` = `a-b-c-d-e`<br />`...joinall` = `a=1,b=2,c=3,d=3,e=3`|
|`max(type = "n")` <br /> `min(type = "n")`<br />`maxkey(type = "n")` <br /> `minkey(type = "n")`|与列表方法相同。|(省略)|

### 职业属性:
- `${_job[XXX].prop}`: 返回指定职业的属性。  
- 属性:
  - role; job; jobid （同 _ffxiventity）
  - isT; isH; isTH; isD; isM; isR; isTM; isHR; isC; isG; isCG; （是否是某个职能，0 or 1。注：M R C G 分别为 近战 远程 生产 采集）  
  - jobCN; jobDE; jobEN; jobFR; jobJP; jobKR; （不同语言中的全名）    
  - jobCN1; jobCN2; jobEN3 (= job); jobJP1 （不同语言中指定长度的缩写）
- `jobXX`, `jobXXn`, `jobid` 可作为 `${_job[XXX].prop}` 中的键 `XXX`，用于指定一个职业。  
- 这些属性也添加到了 `_ffxiventity` 和 `_ffxivparty` 中。
- 例如:   
  - `${_job[Gladiator].jobid}` = `1`;    
  - `${_job[1].jobFR}` = `Gladiateur`;    
  - `${_job[GLA].jobCN1}` = `剑`;    
  - `${_ffxiventity[Gladiator Player].isTM}` = `1`   
  
### 实体属性:  
- 已向 `${_ffxiventity}` 和 `${_ffxivparty}` 添加了多个实体属性:  
  - `bnpcid`, `bnpcnameid`, `ownerid`, `type`, `partytype`, `address`
  - `castid`, `casttime`, `maxcasttime`, `iscasting`  

## 缩写：
- 当处理复杂逻辑时，表达式可能会变得非常长，这可能涉及到多个嵌套的 `${}`。
- 为了改善这一问题，引入以下缩写简化表达式:

|全称|缩写|    
|:---:|:---:|  
|`${numeric:...}` |`${n:...}`|  
|`${string:...}` |`${s:...}`|  
|`${func:...}` |`${f:...}`|  
|`${exvar:...}` | `${ev:}` `${el:}` `${et:}` `${ed:}` |  
|`${(p)var:...}` `${(p)lvar:...}` <br />`${(p)tvar:...}` `${(p)dvar:...}` | `${(p)v:}` `${(p)l:}` <br />`${(p)t:}` `${(p)d:}` |  
|`${?lvar:...}` `${?tvar:...}` `${?dvar:...}` | `${?l:}` `${?t:}` `${?d:}` |  
|`${_loopiterator}`|`${_i}`|
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
|表格：`.width` |`.w`|  
|表格： `.height` |`.h`|  
|表格： `.hlookup()` |`.hl()`|  
|表格： `.vlookup()` |`.vl()`|  
|实体： `.heading` |`.h`|  

## 动作  
### 修复了列表动作 `Insert` 和表格动作 `Resize` 中的错误：  
- 列表变量的原始代码在给定索引超过列表长度时直接插入了 `null` 作为占位符，应使用空白的 `VariableScalar`。
- 这导致了两个问题：解析器无法在表达式中检索这些空值；在变量查看器中双击列表时无法打开且 ACT 报错。
- 与之类似，表格变量的代码添加的空行中，每个空元素实际上被设置为了 `null`：  
  - `vtr.Values.AddRange(new Variable[newWidth]);`  
  - `Rows[i].Values.AddRange(new Variable[newWidth - Rows[i].Values.Count]);`  
  
### 修复了列表方法 `Set` 中的错误：  
- 原始代码在列表中插入的 `VariableScalar` 占位符实际上少了一个。
- 这导致当试图在长度为 `index - 1` 的列表中的给定 `index` 处设置值时无法设置，得到恰好缺少要设置的值的列表。  
  
### 修复了列表方法 `Split` 中的错误：  
- 原始代码忽略了源/目标变量的永久变量选项。  

### 修复了永久变量按钮的问题：  
- 销毁全部变量时，永久变量按钮并未启用，但该选项实际有效。
- 选择此类动作时启用了该按钮。   

### 为列表、表格、字典的 `Set` 动作添加动态表达式支持：
- 列表：`_this` `_idx`
- 表格：`_this` `_row` `_col` `_row[i]` `_col[i]`
- 字典：`_val`

### 更新了列表变量的 `PopFirst` / `PopLast` 动作：  
- `PopFirst` 修改为接受一个可选的 `index` 参数，该参数也支持负值。
- 代码中的动作名称 `PopFirst` 保持不变，为了 XML 兼容性原因保留了 `PopLast`。
- 但是，`PopLast` 的功能现在重定向到 `PopFirst`，其中 index = `-1`。
  
### 添加了 `PopToList` 动作 (set/insert)：  
- 弹出并插入  
  - 从源列表弹出元素并插入到目标列表。
  - 如果未给定目标索引，将被追加到列表的末尾。
  - 注意：这与索引 `-1` 不同，`-1` 在最后两个元素之间插入值
  - 例如：源列表：`1,2,3,4,5`，源索引：`3`，目标列表：`a,b,c,d,e`
    - 目标索引：`3` => `a,b,3,c,d,e`；
    - 目标索引：`-1` => `a,b,c,d,3,e`；
    - 目标索引：` ` => `a,b,c,d,e,3`；
- 弹出并设置  
  - 弹出一个元素并将其设置到目标列表的给定索引处。
  - 两个索引都应给出。
  - 例如，其他条件与上述相同；
    - 目标索引：`3` => `a,b,3,d,e`；
    - 目标索引：`-1` => `a,b,c,d,3`；
- 这些动作实际相当于 `Pop` 和 `Set`/`Insert` 的组合。
- 使用“表达式”输入框作为目标索引输入，描述和标签指令会自动更改。
  
### 为字典变量添加基本动作：  
- `Unset`、`UnsetAll`、`UnsetRegex`  
- `Set`：为键分配一个值。
- `Remove`：若指定的键存在，删除键值对。
- `Merge`：合并字典，保留重复的键。
- `MergeHard`：合并字典，覆盖重复的键。

### 为列表/表格/字典变量新增 `Build` 动作：
- 使用表达式的第一个字符作为分隔符，构建列表变量，其余部分作为输入字符串。对于表格变量，前两个字符用作列/行分隔符。对于字典变量，前两个字符分别作为键值对分隔符和整体对分隔符。
- 允许从给定字符串直接用单个操作创建列表/表格。
- 进一步说，当与 `list.join`、`table.hjoin` 或 `table.vjoin` 结合时，可以从另一个列表的片段或表格的行/列中一步生成列表。
- 例如，表达式 `,1,2,3,4,5,6,7,8,9` 和 `,|11,21,31,41|12,22,32,42|13,23,33,43|14,24,34,44` 可以构建之前的 `lvar:test` 和 `tvar:test`；
`=,a=1,b=2,c=3` 可以构建字典 `a=1, b=2, c=3`。

### 为列表/表格/字典变量新增 `SetAll` 动作：
- 提供了一种灵活的方法为列表/表格/字典变量赋值，类似于 LINQ 表达式中的 `Select()`。
- 遍历整个变量时可以使用下面的动态表达式：
  - 列表变量：`${_this}` `${_idx}`
  - 字典变量：`${_idx}`（当指定了字典长度时）或 `${_key}` `${_val}`
- 对于表格变量，可以使用：`${_this}`, `${_row}`, `${_col}`。
- 例如：
  - 在长度为 9 的列表上使用带有表达式 `${_idx}` 的 SetAll 动作产生带有值 (1-9) 的 `lvar:test`；
  - 然后，在 `lvar:test` 上使用带有表达式 `${_this}^2` 的 SetAll 结果为 `1, 4, 9, ..., 81`。
  - 对于长度为 `5` 的字典，使用键表达式 `${_idx}` 和值表达式 `${_idx}^2` 产生字典 `1:1, 2:4, 3:9, 4:16, 5:25`。
  - 应用键表达式 `${_value}` 和值表达式 `${_key}` 将其反转为 `1:1, 4:2, 9:3, 16:4, 25:5`。

### 为列表/表格/字典变量新增 `Filter` 动作：
- 类似于 LINQ 表达式中的 `Where()` 函数。
- 若动态表达式计算结果为真 (`!= 0`)，过滤列表元素到新列表、表格元素到新列表、表格的行/列到新表格，或字典的键值对到新字典。
- 例如，表达式 `${func:ifequal("", 0, 1):${_this}}` 去除列表空元素；
- `${lvar:listname.indexof(${_this})} = ${_idx}` 在名为 `listname` 的列表中去除列表重复元素；
- 在包含玩家名的列表上使用表达式 `${_ffxiventity[${_this}].distance} > 15 && ${func:ifequal(DPS):${_ffxiventity[${_this}].role}}` 会过滤出距离玩家超过 15 m 的 DPS。

### 为表格变量新增 `SetLine` / `InsertLine` 动作：
- 与列表的 `Build` 动作类似，它根据其第一个字符将表达式分割为列表。根据提供的索引 (row/col)，值列表随后被设置/插入到指定的行/列。计算索引号的逻辑与列表变量的 `Set` / `Insert` 动作类似。
- 例如，对前文的 `lvar:test` 使用 `SetLine` 动作，行索引 `3` ，表达式 `,a,b,c,d,e`，可得：
|11|21|31|41||
|---|---|---|---|---|
|12|22|32|42||
|a|b|c|d|e|
|14|24|34|44||

### 为表格变量新增 `RemoveLine` 动作：
- 此操作从表中删除指定的行/列。
- 例如，从之前的 `lvar:test` 中删除行索引 `3` 结果为：
|11|21|31|41|
|---|---|---|---|
|12|22|32|42|
|14|24|34|44|
  
### 为列表添加 `SortByKeys`，为表格添加 `SortLine`：
- 这些操作基于指定的关键字函数进行排序，对于涉及多条件排序的场景（如绝欧米茄潜能量排序）非常有用。
- 表达式格式：`n+:key1, n-:key2, s+:key3, ...`
  - `n`/`s`：数字/字符串比较
  - `+`/`-`：升序/降序（`+` 是可选的）
  - `key`：对于列表应包括 `${_this}` / `${_idx}`，对于行排序应包括 `${_row}` 或 `${_row[i]}`，对于列排序应包括 `${_col}` 或 `${_col[i]}`。
- 如果关键字函数包含逗号，或以空格开头/结尾，则应将其整体置于引号中，例如`"s+:key", ...` 或 `'s+:key', ...`。例如：
  - `n+:${_this}` `n-:${_this}` `s+:${_this}` `s-:${_this}` 对应之前的四个排序操作。
  - 通过 `n-:${_idx}` 排序会反转列表。
  - 使用表达式 `n-:${f:substring(0):${_this}}, n+:${_idx}%3` 排序列表 `[11, 12, 13, 21, 22, 23, 31, 32, 33]` 会得到 `[33, 31, 32, 23, 21, 22, 13, 11, 12]`。

### 重置名称符合正则的全部类型变量（在标量变量动作中）
- 使用单个动作重置标量、列表、表格、字典变量。
- 永久变量选项依然有效：重置临时（会话）变量不会影响持久变量。
- 在进入新阶段初始化时很有用。

### 复制变量/表达式的值到剪贴板（在标量变量动作中）
- 如果提供了变量名称，其值将直接复制到剪贴板，无需任何解析。
- 如果只提供了一个表达式，它将被解释为一个字符串表达式，然后复制到剪贴板。
- 注：事实上这与标量变量几乎无关。要将标量变量设置到剪贴板，只需在表达式中输入 `${var:name}`（除非剪贴板包含 `${...}` 表达式）。这样设计是为了逻辑上合理地将这个剪贴板操作归入标量变量动作类别，避免创建一个单独的选项卡，进一步拖慢动作表单的加载。

### 中断分组内的全部触发器动作
- 相关 Issue：[#48](https://github.com/paissaheavyindustries/Triggernometry/issues/48)

### 优化动作列表顺序
- 动作、列表动作、表格操作重新排列。
- 此外，用相应的 Enum 枚举值替换了整数硬编码的一些 opTypes。

### Tab 切换选中控件的顺序
- 修改为仅允许在文本框之间切换。
- 修正了部分顺序。

## 表达式文本框
- 添加了 `Color` 表达式类型枚举值，使该文本框显示输入的颜色作为其背景颜色；
- 永久变量选项开启时，相应文本框显示浅蓝色背景；
- 数值或文本表达式包含纯数字/字母的 `${...}` 表达式且无法解析为捕获组或 `_since` 等特殊变量时，文本框显示浅黄色背景警告色；
- 多行模式下从固定高度 100 改为高度限制 100-300，跟随文本行数动态变化。

## 触发器表单 / 动作浏览器
- 在操作描述（和日志消息）中添加了参数，表示变量是否是永久变量，以及表达式是数字/文本类型；
- 如果操作的异步选项未选中，则在描述前添加 `[同]` 前缀；
- 当操作延迟非零且描述文本被覆盖时，添加警告颜色（这通常是在复制和编辑操作时出现的错误，且调试时不容易发现）；
- 在操作描述页面中添加了颜色选项，允许在描述中自定义背景/文本颜色（格式如：`Lavender` / `230,230,250` / `#e6e6fa` / `#eef`）；
- 添加了 `置顶` 和 `置底` 按钮，并允许多选移动；
- 添加了 `撤销` 按钮，以撤销移动/删除操作（基于 Actions 列表状态，对内部单个 Action 元素的修改不会被记录）；
- `添加` 现在会在选定的行下插入操作，而不是将其设置到整个动作列表底部；
- 如果启用了保存后自动执行，`保存` 按钮会变为 `保存并执行`；
- 在底部添加了一个触发器描述标签，显示触发器条件、触发事件源、重新触发选项、顺序执行选项等的一些信息；
- 修改触发器后直接退出时，会弹出消息框确认退出；
- 当点击动作以外的位置时，取消选择动作行。

## 日志表单
- 在日志中添加了更精确的错误信息，例如在表达式展开时哪个表达式引起了错误；
- 添加了两个 `用户` 日志类型 (`消息` < `用户2` < `用户` < `警告`)，程序不应将任何日志输出到该类型；
- 调整了 `warning` / `error` 日志消息颜色为更低饱和度的浅红和浅黄，并为 `custom` 日志添加了浅绿色。
- 改为使用复选框而不是组合框来过滤日志，左键切换勾选，右键单独选中，操作更简便直观：
<p align="center"><img src="https://github.com/MnFeN/Triggernometry/assets/85232361/6d1058cc-2288-4f7d-98f3-3325c4a7e250" width="800"></p>

## 变量查看器 / 编辑器
- 新增对字典变量的支持；
- 允许点击相应的表格头部，排序 8 种类型的变量；
- 在添加列 / 行后，选中的单元格将移至下一个列 / 行；
- 修复了变量状态查看器中某些列宽度无法调整的问题：一些列原本被设置成了 `Fill`，如果该列不是最后一列则列宽调节会被禁止。

## 主界面：
- 当选中本地触发器时，`添加` 按钮不再是未激活状态。此时新建的触发器 / 文件夹会添加到选中触发器的父文件夹，类似于从 xml 粘贴触发器；
- 与之类似，现在允许拖拽元素到触发器上，会将其自动置于触发器的父分组内；
- 在拖拽移动触发器或分组后，自动选中移动的元素。
- 添加快捷键：  
<p align="center"><img src="https://github.com/MnFeN/Triggernometry/assets/85232361/e73a4332-516f-402a-8ffb-89391f6e5446" width="300"></p>

## 其他
### Bug 修复：
- **无参数的 func**：修复了没有参数的字符串函数解析不正确的问题。
  - **Issue**：[#92](https://github.com/paissaheavyindustries/Triggernometry/issues/92)
  - 原始正则表达式错误解析了诸如 `func:length:3*(1+2)` 的表达式，将 `length:3*` 当做了函数名，`1+2` 为括号内的参数。
  - 修改后的正则表达式修复了问题，且可以直接匹配整个表达式，无需后续再次查找 `:` 分割字符串。
  - 微调了正则表达式。

- **高分屏下的动作单选框**：修复了高分辨率屏幕上启用动作的单选框不可见的问题。
  - **Issue**：[#91](https://github.com/paissaheavyindustries/Triggernometry/issues/91)

- **MessageBox 显示**：解决了导致 MessageBox 有时隐藏在活动窗口后面的问题。现在 MessageBox 会始终显示在当前活动窗口之上。

### 增强功能：

- **表达式中的换行**：
  - 增强了对换行的支持，之前与参数分割、代码修剪和正则表达式有冲突。
  - 引入了一个特殊字符 `⏎` 作为在解析过程中的换行符占位符，解析后进行替换。（可以存入输入法，方便输入）
  - 此字符也可直接用于 Triggernometry 表达式，例如，`${func:repeat(5, ⏎):text}`。

- **翻译**：
  - 更新并修订了自版本 1.1.6.0 以来缺失的几百条翻译。
  - 已更新 CN/JP 翻译文件中的键。（注意：FI/FR 文件明显过时，顺序混乱）。
  - 基本补全并修订了中文翻译。

- **触发器触发设置**：
  - 之前的触发器在手动触发时会忽略所有条件检查，但有时我们希望它遵循所有条件。
  - 原本的 `执行` 右键选项改为了  `执行（强制）`，额外添加了 `执行（条件）` 选项。
  - 此外，在 `保存时自动执行` 下方添加了 `自动执行时遵循条件` 设置。

- **测试动作**：添加了一个 `以实时值测试动作` 选项，并在配置中添加了相应的默认设置，以在测试动作时忽略条件。

- **CSV 导出改进**：支持了包含逗号和双引号的表格变量，提供正确的导出文件，而不仅是用 `,` 连接每个单元格。

- **杂项**：
  - 优化了一些重复的代码逻辑
  - 对一些遗漏了本地化设置的 `Parse()` 和 `ToString()` 添加了 `CultureInfo.InvariantCulture` 参数
  - 纠正一些笔误
  - _etc._

## 与旧版本不同的行为
与旧版本相比，除了修复错误和调整用户界面之外，以下行为有所不同：
- **数学解析器 MathParser**：
  - `:` 字符现在是 `? :` 三元运算符的一部分。
  - `^` 运算符现在正确设置为右结合： `2^3^2` = `2^9` = `512` (旧版：`2^3^2` = `8^2` = `64`)。
  - 精度误差容差设置为 `1E-9`（即 `0.1234567890 = 0.1234567899` 被视为真）。
  - 详见前文。

- **输入验证**：一些之前返回默认值 `` 或 `0` 的未定义或无效输入，现在会引发特定的错误消息。

- **蜂鸣音频率**：默认的哔声频率现在不跑调了 (C6, 1046.5 Hz)。

# 已知问题

- **动态变量**: `${_idx}` 等遍历变量时的动态参数并非线程安全，应仅在非异步触发器中使用。
- **数学解析器限制**: 依然不支持共享相同优先级的运算符，在此版本中未修复。（如 `3 % 2 / 4` 应该从左到右解析为 `0.25`，而解析器认为除号优先级更高，会先计算 `2 / 4`。）
- **字典编辑器显示**: 字典变量现在按其固有顺序列出键，而无法点击表头排序。
- **性能**: 很久前开始，加载操作表单明显变慢（约 0.8–2 秒）。这可能是由于操作种类的增加。个人不熟悉 WinForms，不知道能否解决该问题。
- **自动补全**：补全表单中的正则捕获组偶尔在编辑触发器的正则后不更新。重新点击触发器正则文本框可修复。
- 在点击动作时曾出现以下报错，但未曾复现：
```
System.ArgumentOutOfRangeException - Index out of range.
   in System.Collections.ArrayList.get_Item(Int32 index)
   in System.Windows.Forms.DataGridViewSelectedRowCollection.get_Item(Int32 index)
   in Triggernometry.CustomControls.ActionViewer.btnEditAction_Click(Object sender, EventArgs e)
   in Triggernometry.CustomControls.ActionViewer.dgvActions_CellDoubleClick(Object sender, DataGridViewCellEventArgs e)
   in System.Windows.Forms.DataGridView.OnCellDoubleClick(DataGridViewCellEventArgs e)
   in System.Windows.Forms.DataGridView.OnDoubleClick(EventArgs e)
```

## Current / Future To-do List  
Check [https://github.com/MnFeN/Triggernometry/edit/readme/readme.md]  
