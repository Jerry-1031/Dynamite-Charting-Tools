# Dynamite-Tools
Some useful tools of the fanmade music game Dynamite.

# kps_plot

Script to parse a music game XML map file and plot the real-time Keys-Per-Second (KPS) curve.

绘制 Dynamite 谱面 KPS 图的工具。

## Usage

```bash
python kps_plot.py path/to/map.xml [--window 1.0] [--step 0.1] [--output kps.png] [--width 10] [--unicode]
```

```
Options:
    --window   Size of the sliding window in seconds (default: 1.0) (Unit: s)
    --step     Step size in seconds for sampling (default: 0.1) (Unit: s)
    --output   Path to save the output plot image (if omitted, displays interactively)
    --width    Width of the plot figure (default: 10)
    --unicode  Use SimHei font for Unicode character support (e.g., Chinese)
```

[] 内的内容为可选内容，不填为默认。

+ `--window` 参数为滑动窗口长度，表示每次取 `窗口长度` 内 note 个数的平均值，默认为 `1.0`；
+ `--step` 参数为采样间隔，表示每 `采样间隔` 秒计算一次，默认为 `0.1`；
+ `--output` 参数为输出图片名，如不填则直接显示绘图窗口；
+ `--width` 参数为图表宽度，对于稍长的歌曲可调大些，默认为 `10`；
+ `--unicode` 参数为是否为中文歌曲名提供支持，默认关闭。

## 实例

**Example 1** 不另存为图片，直接显示绘图窗口：
```bash
python kps_plot.py "Faded.xml"
```

**Example 2** 另存为 `scy.png`，滑动窗口长度调至 `2.0` 秒，绘图窗口宽度调至 `20`（适用于较长歌曲）：
```bash
python kps_plot.py "Little Seed, Arrival.xml" --window 2.0 --output scy.png --width 20
```

**Example 3** 另存为 `hajimi.png`，滑动窗口长度调至 `0.5` 秒，启用中文支持：
```bash
python kps_plot.py "Ten_Sides_Hachimi.xml" --window 0.5 --output hajimi.png --unicode
```

更多谱面见 `charts` 目录中内容。

# pez2dyn

Convert Phigros fanmade chart(.pez) to [Dynode](https://dyn.iorinn.moe/) file(.dyn).

将 Phigros 自制谱面（.pez）转换为 [Dynode](https://dyn.iorinn.moe/) 谱面（.dyn）的工具。

**Tested**:
+ 2024 April Fool's Day Chart
+ RinFall's Dan 1-3

**Features**:
+ Support multiple bpm (2024/8/17 updated)

**TODO**:
+ Support formatVersion 3

## Usage

+ Unzip .pez file, get .json file and .wav/.mp3/.ogg file;
+ Put .json, .wav/.mp3/.ogg and this `pez2dyn.py` file in a same directory;
+ Change input_file_name and output_file_name;
+ Choose which judgeline you want to convert;
+ Execute this Python file and get output;
+ Open the output with [Dynode](https://dyn.iorinn.moe/), press F5 to export .xml file.

## Special Thanks

[Dynode](https://dyn.iorinn.moe/)

# midi2xml

Convert midi files to Dynamite charts (.xml).

将 midi 文件按音高转换为 Dynamite 谱面的工具。

## Usage

+ 将 `midi2xml.py` 与 midi 文件放在同一目录下；
+ 修改 `midi2xml.py` 中的 `name` 修改为 midi 文件名，并对其它参数进行必要的修改；
+ 运行并获取谱面输出。
