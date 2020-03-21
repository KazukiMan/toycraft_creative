版本号： 20200321 (ver 2.0.1 for develop)

# 玩具国Minecraft建设省 - 玩具国计划2.0

### 注意这是玩具国计划2.0，新版本和老版本并不兼容

欢迎新成员！

这是玩具国计划2.0的官方GitHub，这里将会提供完整的游戏安装及游玩说明。


### 地图下载
[点击下载]()

（我穷，等过段时间有钱了租个廉价的长期VPS再放地图吧）


### 服务器专享建筑 mod 项目地址
[点击进入： Toycraft: A real city simulator for minecraft creative.](https://github.com/KazukiMan/toycraft)

（建设中，诚招合作伙伴，<b>会用鼠标</b>就可以参与项目的！）




### 加入本服务器代表你遵守如下规则
0. 熊孩子滚粗！！！

1. 请<b>在西北(-2850 -1050)至东南(1650 5250)的范围内建筑</b>，腐竹会定期清理超过限度外的地图，如果被误删后果自负

2. 请在点(-2850 -1050)至(1650 5250)之间进行旅行，请不要<b>随意传送、过分跑图</b>，后台维护一旦查出即刻封号逐出

3. 本服限制但不禁止高频红石电路，请在下线时自行关闭，一旦发现忘记关闭的酌情逐出

4. 请不要滥用mod造成区块卡顿，如有区块卡顿的问题将会删除对应区块




### 第一步：下载游戏文件

请下载并解压下述文件

[点击下载游戏文件](https://github.com/KazukiMan/toycraft_creative/archive/2.0.1.zip)

### 第二步：安装java环境

Windows 用户： [点击下载](https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241536_1f5b5a70bf22433b84d0e960903adac8)

MacOS 用户： [点击下载](https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241527_1f5b5a70bf22433b84d0e960903adac8)

Linux x64： [点击下载](https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241526_1f5b5a70bf22433b84d0e960903adac8)

Linux x64 RPM： [点击下载](https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241525_1f5b5a70bf22433b84d0e960903adac8)

（备用）Java Downloads for All Operating Systems： [点击进入](https://www.java.com/en/download/manual.jsp)

（在你的下载没有出现问题时请勿使用备用项，如果有问题请直接联系腐竹）



### 第三步：安装游戏关联

Windows 用户打开 HMCL-3.2.136.exe ，Unix 用户请打开 HMCL-3.2.136.jar ，打开错误或无法打开请跳回第二步重新安装java，或检查java环境是否安装正常


没有购买过游戏的选择offline模式添加用户名，点击右下角play即可

购买过游戏的可以选择Mojang模式登陆用户，点击右下角play打开游戏


### 第四步：添加白名单

<b>1.0版本老玩家请直接略过本条</b>

在第一次加入游戏时，由于用户没有被加入白名单所以需要联系腐竹加入白名单

因为要得到ssid和用户名，请玩家在联系腐竹之前务必要登陆一次游戏并且被挡才行


### 第五部：注册

为了保障账号和服务器的安全，以及考虑到部分小伙伴有开直播的可能，服务器在初次登陆时需要使用

`/register 密码 重复密码 `

进行注册

以后每次登录需使用

`/login 密码`

（这样即使知道了用户也无法进入服务器，因为还有密码挡着）

（请务必在输入密码时黑屏处理以保证安全）

（当前版本的注册仍然存在bug，将会在下一版本修复）


### 更新说明（老版本）
#### 20190929
1. 添加了凿子mod

2. 重组了GitHub项目，创建了懒人包

#### 20191003
1. 修正了journeymap的加载错误

2. 添加了精简包分支

3. 添加了升级包分支

#### 20191022
1. 修正了worldedit插件复制箱子、漏斗等容器时会发生的错误

【注意】本次版本更新不需要玩家调整mod

#### 20191029
1. 添加了皮肤插件，现在可以带着皮肤登陆服务器了，使用/skin可以进一步调整皮肤

【注意】本次版本更新不需要玩家调整mod

#### 20191111更新

1. 添加了登录插件，初次登录需使用 
`/register 密码 重复密码 `
进行注册

以后每次登录需使用
`/login 密码`


#### 20191118更新(REAL Anniversary Version)

本次更新需要老玩家（20191111/20191029/20191022/20191003/20190929版本）下载升级包

安装方法：升级包下载后删除 .minecraft/mods 然后将解压后的文件全部放到 .minecraft/ 文件夹下，遇到重复选择「替换」即可

* macOS用户请不要删除CocoaInput，不然会造成输入法bug

* macOS用户若安装了CocoaInput请务必在每次打开游戏时点击屏幕，需要有一个鼠标的识别保证输入法正常

0. 移除了creeper可能引发接龙的bug(x)，移除了可能出现Herobrine的要素（x）

1. 添加了chiselsandbits（凿子和组件）到客户端和服务端，现在可以更加精细化的处理建筑的局部了

2. 添加了WorldeditCUI到客户端中（如果过分占用性能可以选择关闭，不影响worldedit使用和服务器登录）

* WorldeditCUI是worldedit的一个辅助mod，能够实现在建筑过程中可视化选区的目的，但是由于线条太过暴力，所以效果并不是特别理想，在此特别建议<b>在按键设置中设置关闭显示按键和重新选区按键</b>

3. 更新了客户端的小地图及标记点，部分地区水下的地势图。对于混沌府、神宫山地区、天城工业园等地区的标记进行了大规模的补充和添加，本次上传的记录点约350个

4. 更新了客户端的worldedit，以保证和服务器一致减少bug可能性

5. 修正了GitHub项目，添加了二次登录说明于各分支的readme文件

6. 移除了CocoaInput的小众mod，如果有macOS输入法问题的请联系腐竹

7. 常规清理了大量多余的区块，回档了团子城北部部分损坏地图，后发现回档后效果不理想又前进到了新的版本

8. 添加了地图的下载，由于GitHub对于大文件支持不好，所以放在了这里: https://www.stlaplace.com/toy_craft.zip

#### 20191206更新
本次更新不需要玩家安装任何更新包。

0. 移除了creeper可能引发接龙的bug(x)，移除了可能出现Herobrine的要素（x）

1. 添加了服务器的快速传送

2. 修正了小地图插件信标过多的问题，将默认信标的处理方式改为了关闭



#### 20200219更新
需要安装更新包

0. 移除了creeper可能引发接龙的bug(x)，移除了可能出现Herobrine的要素（x）

1. 追加了一个植物类mod和其引导mod，现在有更多的方块可以进行木建筑的建设了

2. 追加了小地图的地点，现在的坐标点约有470个了

3. 删除了地图中超过界限的范围

4. 修正了readme中Java下载地址的问题


### 更新说明（2.0）
#### 20200321更新

警告：本版本不与之前所有版本兼容，需重新下载懒人包

0. 移除了creeper可能引发接龙的bug(x)，移除了可能出现Herobrine的要素（x）；

1. 将游戏整体版本从原来的 Minecraft 1.10.2 迁移至了 Minecraft 1.12.2 并针对模组做了调整；

2. 删除了砍树插件，砍树请直接使用 worldedit 替换；

3. 部分重写了 bamboomod （竹 mod ）并将其迁移到了 1.12.2 ；

4. 添加了我服专属 mod （当前为 DEMO 版） toycraft ，该 mod 后续将会持续更新（目前该 mod 的使用将会有效解决团子市夜天宫地区夜天门/朱雀门的卡顿问题）；

5. 将以下 mod 更新到了 1.12.2 版本： Chisel, chiselsandbits, CocoaInput, CTM, furniture, industrialcraft, journeymap, shetiphiancore, terraqueous, TofuCraftReload, worldedit, WorldEdit+CUI 并将服务器皮肤、登陆和传送的 mod 更新到了1.12.2；

6. 重构了 GitHub 项目，由于历史原因（懒）保留了原有项目，并将 readme 修改至新项目引导，目前只提供懒人包，升级包和精简包将会合并并且在下一个版本提供；

7. 调整了 CocoaInput ，默认为关闭状态，如果有 macOS 等系统的输入法问题的，请将其打开即可；

8. 部分调整了小地图，复查修正了小地图的标记点，现在有坐标点 474 个；

9. 删除了项目中大地图 png 文件，进一步缩减了包；

10. 调整了默认快捷键、默认小地图字体以及小地图坐标点的显示（默认为隐藏）；

11. 更新了材质包，现在客户端默认加载材质包 Faithful+1.12.2-rv4；

12. 更新了光影，在保留 BSL v7.0 和 SEUS-Renewed-1.0.0 的基础上，添加了较为轻量的三个光影 Sildurs Vibrant Shaders v1.22 High, Sildurs Vibrant Shaders v1.22 Medium, Sildurs Vibrant Shaders v1.22 Lite 。默认开启 Sildurs Vibrant Shaders v1.22 Lite ；

13. 删除了万神殿计划的相关内容；

14. 添加了 .gitignore 文件，解决了部分系统临时文件没有及时清理被上传的问题
