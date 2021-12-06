---
title: iOS错误构建、编译错误处理
date: 2021-12-07 01:05:33
tags:
  - iOS
---

## Flutter上传发布到应用商店的时候发生的错误
> ERROR ITMS-90208: "Invalid Bundle. The bundle Runner.app/Frameworks/Flutter.framework does not support the minimum OS Version specified in the Info.plist."

处理方法一：
修改`/ios/Flutter/AppframeworkInfo.plist`中的`MinimumOSVersion`到9.0，然后修改项目的iOS Deployment Target到9.0，对应Podfile的版本也修改，然后`flutter clean`后重新打包上传

处理方法二：
修改下面`flutter sdk`中对应的文件，把里面的`MinimumOSVersion`值改成9.0，然后`flutter clean`后重新打包上传
```
bin/cache/artifacts/engine/ios-release/Flutter.xcframework/ios-arm64_armv7/Flutter.framework/Info.plist
bin/cache/artifacts/engine/ios-release/Flutter.xcframework/ios-arm64_x86_64-simulator/Flutter.framework/Info.plist
```