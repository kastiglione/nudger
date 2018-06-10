# nudger
 Nudger: Example LLDB Python Command

At the 2018 WWDC, the [Advanced Debugging with Xcode and LLDB](https://developer.apple.com/videos/play/wwdc2018/412) talk demonstrated an lldb command called `nudge`. While the talk demonstrates the use of `nudge`, it doesn't cover any of its implementation, but the [source code for nudge](https://developer.apple.com/sample-code/wwdc/2018/UseScriptsToAddCustomCommandsToLLDB.zip) is provided.

Having maintained and written a number of [lldb commands](https://github.com/facebook/chisel), I have thoughts on how to get started writing lldb commands. This repo is not documentation on how to get started, but it provides a few simple and minimal versions, showing how to start a command like `nudge`, and then adding some features.

## Step 1: Core functionality, ObjC only

[The first version](https://github.com/kastiglione/nudger/blob/c623fa02c66df6ea86bac156c62306b42e66a7f5/nudger.py) is a small amount of code that does the basics, but supports ObjC only.

## Step 2: Add Swift support

[The second version](https://github.com/kastiglione/nudger/blob/3c49f34ecc3df9b96386a52468a1aaa517d2427f/nudger.py) adds support for Swift. ([diff](https://github.com/kastiglione/nudger/commit/3c49f34ecc3df9b96386a52468a1aaa517d2427f))

## Step 3: Remember and reuse last view

[The third version](https://github.com/kastiglione/nudger/blob/e66864601ec853b2883892dd2d8fdf465f2fcd76/nudger.py) adds the feature that remembers the last nudged view, and applies the nudge to it. For example, `nudger 0 -10` moves the last nudged view up by 10 points. ([diff](https://github.com/kastiglione/nudger/commit/e66864601ec853b2883892dd2d8fdf465f2fcd76))

